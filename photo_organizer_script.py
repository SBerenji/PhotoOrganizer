"""
    Libraries required to interact with the operatins system and organize the files
"""

import os  # required for interacting with the operating system
import shutil  # required for moving files around
# required for extracting data information from images files
from datetime import datetime


def organize_photos():
    pass


def main():
    directory_path = input("Please enter the file path of the images: ")

    # Check if the directory exists and is accessible
    if not os.path.isdir(directory_path):
        print(
            f"Cannnot open file path '{directory_path}'.\nAre you sure the file path is correct?")
        return

    print(f"Successfully accessed the directory: {directory_path}")

    # List the content of the directory, if there is any
    try:
        files = os.listdir(directory_path)
        if not files:
            print("The directory is empty.")
            return

        print("Directory contains:", files)

        # Organizing the content

    # If not permissioned to read the file
    except PermissionError:
        print(
            f"Permission denied: Unable to access the contents of '{directory_path}'")

    # If there is another error:
    except Exception as e:
        print(f"An error occured: {e}")


if __name__ == "__main__":
    main()
