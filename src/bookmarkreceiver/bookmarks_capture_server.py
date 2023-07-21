"""bookmarks_capture_server.py  -- receive bookmarks publishing data.

Typically, this runs on port 38582.  But that's up for configuration.
"""

import argparse
import json
import logging
import os
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, HTTPServer

from bookmarkdata import commit_timestamped_entry, Config



class Config:
    def __init__(self, config_file):
        self.port = None
        self.output_logs_dir = None
        self.load_config(config_file)

    def load_config(self, config_file):
        if config_file is None:
            config_file = os.path.join(os.getcwd(), 'config.json')
        if os.path.isfile(config_file):
                with open(config_file, 'r') as f:
                    config_data = json.load(f)
                    self.port = config_data.get('port')
                    self.output_logs_dir = config_data.get('output_logs_dir')
        else:
            raise FileNotFoundError(f'Config file not found: {config_file}')

    def override_port(self, port):
        self.port = port


def commit_timestamped_entry(timestamp, title, url, output_logs_dir):
    log_date = datetime.fromtimestamp(timestamp, timezone.utc).strftime('%Y-%m-%d')
    log_file = os.path.join(output_logs_dir, f'{log_date}.json')
    log_entry = {'TIME': timestamp, 'TITLE': title, 'URL': url}
    with open(log_file, 'a') as f:
        f.write(json.dumps(log_entry) + '\n')


class RequestHandler(BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        self.config = server.config
        super().__init__(request, client_address, server)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        data = json.loads(post_data)

        url = data.get('url')
        title = data.get('title')

        # Process the received data as needed
        print(f'Received: {title} ({url})')
        
        # Store the data in the appropriate file
        commit_timestamped_entry(int(datetime.now().timestamp()),
                                 title, url,
                                 self.config.output_logs_dir)
        
        # Respond with a success status code
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        response = {'message': 'Data received successfully'}
        self.wfile.write(json.dumps(response).encode('utf-8'))

    def log_message(self, format, *args):
        """Override log_message to suppress logging output."""
        pass


def run(config_file=None, port=None):
    # Load configuration
    config = Config(config_file)

    # Override port if specified on the command line
    if port:
        config.override_port(port)

    # Disable logging of the http.server module
    logging.getLogger('http.server').disabled = True

    # Set up server address
    server_address = ('', config.port)
    httpd = HTTPServer(server_address, RequestHandler)
    httpd.config = config

    print('Starting server. Press Ctrl-C to terminate.')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('Server terminated by user.')


if __name__ == '__main__':
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='HTTP Server with Config')
    parser.add_argument('-c', '--config', help='Path to the config file')
    parser.add_argument('-p', '--port', type=int, help='Port to run the server on')
    args = parser.parse_args()

    # Start the server
    run(config_file=args.config, port=args.port)


