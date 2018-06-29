import sys
import os
from pathlib import Path

source_directory = ""
destination_directory = ""
extra_directory = ""

def get_month(month: str) -> str:
    if month == "01":
        return "jan"
    elif month == "02":
        return "feb"
    elif month == "03":
        return "mar"
    elif month == "04":
        return "apr"
    elif month == "05":
        return "may"
    elif month == "06":
        return "jun"
    elif month == "07":
        return "jul"
    elif month == "08":
        return "aug"
    elif month == "09":
        return "sep"
    elif month == "10":
        return "oct"
    elif month == "11":
        return "nov"
    elif month == "12":
        return "dec"
    return None

if len(sys.argv) < 3:
    print("Not enough arguments provided! Please provide a source and a destination folder and optionally an additional folder to move media to.", file=sys.stderr)
    sys.exit(1)
elif not Path(sys.argv[1]).is_dir():
    print("Source directory does not exist!", file=sys.stderr)
    sys.exit(1)
elif not Path(sys.argv[2]).is_dir():
    print("Destination directory does not exist!", file=sys.stderr)
    sys.exit(1)
else:
    source_directory = sys.argv[1]
    destination_directory = sys.argv[2]
    if len(sys.argv) > 3:
        extra_directory = sys.argv[3]
    all_files = os.listdir(source_directory)
    files_to_move = []
    file_dirs = {}
    for file in all_files:
        ext = Path(file).suffix.lower()
        if ext == ".png" or ext == ".jpg" or ext == ".gif" or ext == ".avi" or ext == ".mp4" or ext == ".mov":
            files_to_move.append(Path(source_directory).joinpath(file))
    if len(files_to_move) == 0:
        print("No acceptable media found.")
    else:
        print(f"Found {len(files_to_move)} photos and/or videos.")
    
    for file in files_to_move:
        year = file.name[:4]
        month = get_month(file.name[5:7])
        move_to = Path(destination_directory).joinpath(year).joinpath(month)
        if extra_directory:
            move_to = move_to.joinpath(extra_directory)
        move_to = move_to.joinpath(file.name)
        file_dirs[file] = move_to

    print("The files will be moved as follows:")
    for old_dir, new_dir in file_dirs.items():
        print(f"{old_dir} -> {new_dir}")
    
    print("Would you like to continue? (y/n)")
    choice = ""
    while True:
        choice = sys.stdin.read(1)
        if choice.lower() != 'y' and choice != 'n':
            continue
        else:
            break
    
    if choice == 'y':
        for old_dir, new_dir in file_dirs.items():
            os.makedirs(str(new_dir.parent), exist_ok=True)
            os.rename(old_dir, new_dir)
        print("Done.")
        print("\a")

    sys.exit(0)