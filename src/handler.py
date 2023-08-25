

import json

import chassis2023.util as util
import chassis2023.config as config
import chassis2023.jsonwebservice as jweb


# A question for the package system --
# how is data included?
# OK, and now I get back to the package system code...
#  -- ok, but the package system itself needs this capability.
#  Chicken and egg.
#
# Demands on chassis2023, JSONWEBSERVICE system:
#
# chassis2023.jsonwebservice
# - assumptions:
#  -- receives POST data as UTF-8 encoded JSON
# * jweb.jsondata -- "<RequestHandler>.rfile" UTF-8 decoded JSON content
# * calls handler.POST()
#
# utility functions:
# * timestamp()  -- now, GMT, seconds since epoch
# * write_json(path, content)
# * read_json(path)
#
# CONFIG values are read, and used when the program is started,
# to check that the session configuration is valid, and if it isn't,
# to require that values are defined at the invocation
#
# config values are read into config.values[...]


g = {
    "T":  None,  # timestamp of recording
    "URL": None,  # url of recording
    "TITLE": None  # title of recording
}


def str_summary():
    return f"""recv: {g["TITLE"]} - {g["URL"]} @ T:{g["T"]}"""


def commit_timestamped_entry():
    log_file = config.values["outputdir"] / config.values["outputfile"]
    log_entry = {'T': g["T"], 'TITLE': g["TITLE"], 'URL': g["URL"]}
    with open(log_file, 'a') as f:
        f.write(json.dumps(log_entry) + '\n')


def POST():
    # retrieve information from received data
    D = jweb.jsondata
    
    g["T"] = util.timestamp()
    g["URL"] = D.get("url")
    g["TITLE"] = D.get("title")

    # Debug note
    print(str_summary())
    
    # Store the data in the appropriate file
    commit_timestamped_entry()

    return (200, {"message": "Data received successfully."})

