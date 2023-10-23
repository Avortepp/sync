import os
import sys
import shutil
import hashlib
import time


def log_message(message, log_file):
    with open(log_file, "a") as log:
        log.write(message + "\n")
    print(message)


def sync_folders(source_folder, replica_folder, log_file):
    # create replica folder if it doesn't exist
    if not os.path.exists(replica_folder):
        os.makedirs(replica_folder)

    # iterate over files and subdirectories in the source folder
    for root, _, files in os.walk(source_folder):
        for file in files:
            source_path = os.path.join(root, file)
            relative_path = os.path.relpath(source_path, source_folder)
            replica_path = os.path.join(replica_folder, relative_path)

            # calculate MD5 checksum of the source file
            source_checksum = hashlib.md5(open(source_path, "rb").read()).hexdigest()

            # check if the file exists in the replica folder
            if os.path.exists(replica_path):
                # calculate MD5 checksum of the replica file
                replica_checksum = hashlib.md5(
                    open(replica_path, "rb").read()
                ).hexdigest()

                # if checksums match, the files are identical
                if source_checksum == replica_checksum:
                    continue

            # copy the source file to the replica folder
            shutil.copy2(source_path, replica_path)
            log_message(f"Copied: {relative_path}", log_file)

    # delete files that are not in the source folder
    for root, _, files in os.walk(replica_folder):
        for file in files:
            replica_path = os.path.join(root, file)
            relative_path = os.path.relpath(replica_path, replica_folder)
            source_path = os.path.join(source_folder, relative_path)

            if not os.path.exists(source_path):
                os.remove(replica_path)
                log_message(f"Deleted: {relative_path}", log_file)


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python sync_folders.py source_folder replica_folder log_file")
        sys.exit(1)

    source_folder = sys.argv[1]
    replica_folder = sys.argv[2]
    log_file = sys.argv[3]

    while True:
        sync_folders(source_folder, replica_folder, log_file)
        time.sleep(3600)  # Synchronize every hour
