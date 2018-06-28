import sys
import os
from dependencies import exiftool

if len(sys.argv) < 2:
    print("No directory argument provided!", file=sys.stderr)
    sys.exit(1)
elif not os.path.isdir(sys.argv[1]):
    print("Supplied path does not exist!", file=sys.stderr)
    sys.exit(1)
else:
    print("Yay!")
    sys.exit(0)