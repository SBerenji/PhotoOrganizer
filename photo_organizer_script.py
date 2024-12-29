"""
    Libraries required to interact with the operatins system and organize the files
"""

import os  # required for interacting with the operating system
import shutil  # required for moving files around
# required for extracting data information from images files
from datetime import datetime
from PIL import Image
from PIL.ExifTags import TAGS


def check_external_device(directory_path):
    """
    Checks if the provided path is an external device like a phone or camera.
    """
    if "This PC" in directory_path or any(keyword in directory_path.lower() for keyword in ['mtp', 'phone', 'samsung', 'android']):
        print(
            f"The path '{directory_path}' appears to be on an external device.")
        print(
            "Please copy the files to your computer and provide the local directory path.")
        return True
    return False


def image_date_extractor(file_path):
    """
    Extracts the date the image was taken by extracting the EXIF metadata
    If date taken is not available, the function returns the date 
    that the last time the image was modified
    """
    try:
        with Image.open(file_path) as img:  # Securely opens and closes the file
            exif_data = img._getexif()

            if exif_data is not None:
                for tag_id, value in exif_data.items():
                    tag_name = TAGS.get(tag_id, tag_id)
                    if tag_name == "DateTimeOriginal":
                        # If the tag is found, convert it to the appropriate format
                        return datetime.strptime(value, "%Y:%m:%d %H:%M:%S")

        # If no EXIF data or DateTimeOriginal tag is foind,
        # return the last modified date
        print(
            f"No EXIF date found for '{file_path}'. Modification date is provided instead.")
        return datetime.fromtimestamp(os.path.getmtime(file_path))

    except Exception as e:
        print(f"Error reading data for file located in '{file_path}' : {e}")
        return None


def organize_photos(directory_path):
    """
    Organizes photos into directories based on the year the image was taken
    """
    try:
        # Iterate through all files in the directory
        for file_name in os.listdir(directory_path):
            file_path = os.path.join(directory_path, file_name)

            # Skip if the content is not a file
            if not os.path.isfile(file_path):
                continue

            # Skip if the file is not an image (jpg, jpeg, png)
            if not (file_name.lower().endswith(('.jpg', '.jpeg', 'png'))):
                print(f"Skipping non-image file {file_name}")
                continue

            # Extraction the creation date of the image file
            img_date = image_date_extractor(file_path)
            if not img_date:
                print(f"Could not determine date for '{file_name}'. Skipping.")
                continue

            # Extracting the year and month from the date
            year = img_date.strftime("%Y")

            # Create folders
            year_folder = os.path.join(directory_path, year)

            if not os.path.exists(year_folder):
                os.makedirs(year_folder)

            # Move the file to the appropriate directory
            shutil.move(file_path, os.path.join(year_folder, file_name))
            print(f"Moved '{file_name}' to '{year_folder}'")

            # Next organize the images into months inside the year directory

            month = img_date.strftime("%B")
            month_folder = os.path.join(year_folder, month)

            if not os.path.exists(month_folder):
                os.makedirs(month_folder)

            # Move the file to the appropriate directory
            shutil.move(os.path.join(year_folder, file_name),
                        os.path.join(month_folder, file_name))
            print(f"Moved '{file_name}' to '{month_folder}'")

    except Exception as e:
        print(f"An error occurred while organizing photos: {e}")
        return f"An error occurred: {e}"  # Returning the message to FastAPI


def main(directory_path):

    # Check if the path is an external device
    if check_external_device(directory_path):
        return "External device detected, please provide a local path"

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

        # Organizing the content
        organize_photos(directory_path)

    # If not permissioned to read the file
    except PermissionError:
        print(
            f"Permission denied: Unable to access the contents of '{directory_path}'")

    # If there is another error:
    except Exception as e:
        print(f"An error occured: {e}")

    return f"Success! Your photos from {directory_path} have been organized successfully!"


# if __name__ == "__main__":
#     main()
