import os
import shutil
import tempfile
from datetime import datetime, timedelta, timezone
from unittest import TestCase

from server import commit_timestamped_entry

class CommitTimestampedEntryTests(TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp(prefix='runtime_testdata')
        self.output_logs_dir = os.path.join(self.test_dir, 'logs')
        os.makedirs(self.output_logs_dir)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_commit_timestamped_entry(self):
        start_date = datetime(2023, 7, 1, tzinfo=timezone.utc)
        for i in range(12):
            timestamp = int((start_date + timedelta(days=i // 4)).timestamp())
            title = f"Entry {i+1}"
            url = f"http://example.com/{i+1}"
            commit_timestamped_entry(timestamp, title, url, self.output_logs_dir)

        # Verify the files were created in the appropriate directories
        log_files = os.listdir(self.output_logs_dir)
        self.assertEqual(len(log_files), 3)  # Expecting three log files

        for file in log_files:
            file_path = os.path.join(self.output_logs_dir, file)
            with open(file_path, 'r') as f:
                entries = f.readlines()
                self.assertEqual(len(entries), 4)  # Expecting four entries per log file

        print("Unit tests completed successfully.")

if __name__ == '__main__':
    unittest.main()
