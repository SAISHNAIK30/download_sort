import os
import time
import shutil
import logging

# Define paths
DOWNLOADS_FOLDER = os.path.expanduser("~/Downloads")
SORTED_FOLDER = os.path.expanduser("~/Sorted_Downloads")

# File type categories
FILE_TYPES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"],
    "Videos": [".mp4", ".mkv", ".avi", ".mov", ".flv"],
    "Documents": [".pdf", ".doc", ".docx", ".ppt", ".pptx", ".xls", ".xlsx", ".txt"],
    "Audio": [".mp3", ".wav", ".aac", ".flac"],
    "Compressed": [".zip", ".rar", ".tar", ".gz", ".7z"],
    "Executables": [".exe", ".msi"],
    "Others": []  # Any unknown file types
}

# Ensure sorted folders exist
os.makedirs(SORTED_FOLDER, exist_ok=True)
for category in FILE_TYPES.keys():
    os.makedirs(os.path.join(SORTED_FOLDER, category), exist_ok=True)

# Set up logging
log_file = os.path.join(SORTED_FOLDER, "download_sort.log")
logging.basicConfig(filename=log_file, level=logging.INFO, format="%(asctime)s - %(message)s")

def log_move(file_path, dest_folder):
    """Log file movements"""
    logging.info(f"Moved {file_path} to {dest_folder}")

def get_category(file_name):
    """Get category based on file extension"""
    _, ext = os.path.splitext(file_name)
    ext = ext.lower()
    for category, extensions in FILE_TYPES.items():
        if ext in extensions:
            return category
    return "Others"

def move_file(file_name):
    """Move file to the correct folder"""
    src_path = os.path.join(DOWNLOADS_FOLDER, file_name)
    if not os.path.isfile(src_path):
        return  # Skip if it's not a file

    category = get_category(file_name)
    dest_folder = os.path.join(SORTED_FOLDER, category)
    dest_path = os.path.join(dest_folder, file_name)

    shutil.move(src_path, dest_path)
    log_move(src_path, dest_path)
    print(f"Moved: {file_name} → {category}")

def monitor_downloads():
    """Monitor Downloads folder for new files"""
    print("📂 Monitoring Downloads folder...")
    existing_files = set(os.listdir(DOWNLOADS_FOLDER))

    while True:
        time.sleep(5)  # Check every 5 seconds
        new_files = set(os.listdir(DOWNLOADS_FOLDER)) - existing_files

        for file_name in new_files:
            move_file(file_name)

        existing_files = set(os.listdir(DOWNLOADS_FOLDER))

if __name__ == "__main__":
    monitor_downloads()
