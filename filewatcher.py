import os
import sys
import shutil
import time
from fsevents import Observer, Stream

def copy(FileEvent):
    src = FileEvent.name
    if(os.path.isfile(src)):
        fn = os.path.split(src)[-1:][0]
        path = os.path.split(src)[:-1][0]
        dest_path = path.replace(SRC_PATH, DEST_PATH)
        print "[INFO] Copying %s to %s" % (src, os.path.join(dest_path, fn))
        shutil.copy2(src, os.path.join(dest_path, fn))

if __name__ == '__main__':
    try:
        SRC_PATH=sys.argv[1]
    except IndexError:
        print "[ERR] Usage: filewatcher.py SRC DEST"
        sys.exit(1)

    try:
        DEST_PATH=sys.argv[2]
    except IndexError:
        print "[ERR] Usage: filewatcher.py SRC DEST"
        sys.exit(1)

    if(not os.path.isdir(SRC_PATH) or not os.path.isdir(DEST_PATH)):
        print "[ERR] SRC: %s" % SRC_PATH
        print "[ERR] DEST: %s" % DEST_PATH
        print "[ERR] SRC and DEST must both be valid paths"
        sys.exit(2)

    observer = Observer()
    try:
        observer.start()
        stream = Stream(copy, SRC_PATH, file_events=True)
        observer.schedule(stream)
        print "[INFO] Monitoring %s and copying to %s" % (SRC_PATH, DEST_PATH)
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        observer.unschedule(stream)
        observer.stop()
    
