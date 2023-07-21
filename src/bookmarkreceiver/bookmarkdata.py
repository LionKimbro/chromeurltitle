"""bookmarkdata.py  -- back-end systems for storing data in the filesystem

There are two systems that call this:

  bookmarks_capture_server.py  -- an http.server.HTTPServer instance
  bookmarks_recent_updater.py  -- a process that is dedicated to updating
                                  RECENT.json, once per 5 minutes

The reason RECENT.json needs to be updated every five minutes, is
because it keeps RECENT.json populated with data from the last 24
hours.

Note that, running every 5 minutes, that data could be incorrect by
five minutes.  But even that level of accuracy is basically more than
is needed.
"""

import fsmutex


