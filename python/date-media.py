import sys
import os
from pathlib import Path
from datetime import datetime
from dependencies import exiftool

directory = ""

def format_date(date: str) -> datetime:
    return datetime.strptime(date, "%Y:%m:%d %H:%M:%S")

def format_date_utc(date: str) -> datetime:
    date = date[:-5] + date[-5:].replace(':', '')
    return datetime.strptime(date, "%Y:%m:%d %H:%M:%S%z")

def process_photos(photos: list) -> dict:
    new_names = {}
    for photo in photos:
        create_date = et.get_tag("EXIF:CreateDate", str(photo))
        date_to_use = ""
        if create_date is not None:
            date_to_use = format_date(create_date).strftime("%Y-%m-%d_%H-%M-%S")
        else:
            file_modify_date = format_date_utc(et.get_tag("File:FileModifyDate", str(photo)))
            file_create_date = format_date_utc(et.get_tag("File:FileCreateDate", str(photo)))
            earliest_date = file_modify_date if file_modify_date < file_create_date else file_create_date
            date_to_use = earliest_date.strftime("%Y-%m-%d_%H-%M-%S")
        new_names[photo] = Path(directory).joinpath(date_to_use + photo.suffix)
    return new_names

def process_videos(videos: list) -> dict:
    new_names = {}
    for video in videos:
        create_date = et.get_tag("CreateDate", str(video))
        create_date = format_date(create_date).strftime("%Y-%m-%d_%H-%M-%S")
        new_names[video] = Path(directory).joinpath(create_date + video.suffix)
    return new_names


if len(sys.argv) < 2:
    print("No directory argument provided!", file=sys.stderr)
    sys.exit(1)
elif not Path(sys.argv[1]).is_dir():
    print("Supplied path does not exist!", file=sys.stderr)
    sys.exit(1)
else:
    directory = sys.argv[1]
    all_files = os.listdir(directory)
    photo_files = []
    video_files = []
    file_names = {}
    for file in all_files:
        ext = Path(file).suffix.lower()
        if ext == ".png" or ext == ".jpg" or ext == ".gif":
            photo_files.append(Path(directory).joinpath(file))
        elif ext == ".avi" or ext == ".mp4" or ext == ".mov":
            video_files.append(Path(directory).joinpath(file))
    if len(photo_files) == 0 and len(video_files) == 0:
        print("No photos or videos found.")
    else:
        print(f"Found {len(photo_files)} photos and {len(video_files)} videos.")

        with exiftool.ExifTool() as et:
            if len(photo_files) > 0:
                file_names.update(process_photos(photo_files))
            if len(video_files) > 0:
                file_names.update(process_videos(video_files))
        
        print("The files will be renamed as follows:")
        for old_name, new_name in file_names.items():
            print(f"{old_name.name} -> {new_name.name}")
        
        print("Would you like to continue? (y/n)")
        choice = ""
        while True:
            choice = sys.stdin.read(1)
            if choice.lower() != 'y' and choice != 'n':
                continue
            else:
                break

        if choice == 'y':
            for old_name, new_name in file_names.items():
                os.rename(old_name, new_name)
            print("Done.")
            print("\a")

    sys.exit(0)