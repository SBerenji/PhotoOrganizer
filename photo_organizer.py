"""
    Libraries required to interact with the operatins system and organize the files
"""

import boto3
from botocore.exceptions import NoCredentialsError
# required for extracting data information from images files
from datetime import datetime
from PIL import Image
from PIL.ExifTags import TAGS
import io
from dotenv import load_dotenv  # to manege environmental variables
import os
import zipfile
# Load environment variables from .env file
load_dotenv()

# Get the values from the environment variables
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
S3_BUCKET = os.getenv("S3_BUCKET")
S3_REGION = os.getenv("S3_REGION")


# Validate that all required environment variables are set
if not AWS_ACCESS_KEY:
    raise ValueError(
        "AWS_ACCESS_KEY is not set. Make sure it's properly set in the .env file.")
elif not AWS_SECRET_KEY:
    raise ValueError(
        "AWS_SECRET_ACCESS_KEY is not set. Make sure it's properly set in the .env file.")
elif not S3_BUCKET:
    raise ValueError(
        "S3_BUCKET is not set. Make sure it's properly set in the .env file.")
elif not S3_REGION:
    raise ValueError(
        "S3_REGION is not set. Make sure it's properly set in the .env file.")


# Initialize S3 Client
s3_client = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=S3_REGION,
)


def generate_presigned_url(s3_key, expiration=3600):
    """Generate a presigned URL for the S3 object."""
    return s3_client.generate_presigned_url(
        'get_object',
        Params={'Bucket': S3_BUCKET, 'Key': s3_key},
        ExpiresIn=expiration
    )


def image_date_extractor(file):
    """
    Extracts the date the image was taken by reading the EXIF metadata.
    If EXIF data is not found, returns the current timestamp.
    """
    try:
        img = Image.open(file)
        exif_data = img._getexif()

        if exif_data:
            for tag_id, value in exif_data.items():
                tag_name = TAGS.get(tag_id, tag_id)
                if tag_name == "DateTimeOriginal":
                    return datetime.strptime(value, "%Y:%m:%d %H:%M:%S")

        # If no EXIF data or DateTimeOriginal tag is foind,
        # Fallback: return current time

        print(f"No EXIF date found for '{file_path}'. Modification date is provided instead.")
        return datetime.fromtimestamp(os.path.getmtime(file_path))

    except Exception as e:
        print(f"Error extracting date from image: {e}")
        return datetime.now()


async def zip_and_upload_to_s3(file_objects, folder_name):
    zip_buffer = io.BytesIO()

    try:
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for file_path, file_content in file_objects:

                # # Reset the pointer to the start after printing the size
                file_content.seek(0)

                # Writing the file content to the zip buffer
                # where the problem lies::
                zip_file.writestr(file_path, file_content.read())

        zip_buffer.seek(0)
        print("middle of the zip_and_upload_to_s3 function")
        s3_key = f"{folder_name}/organized_photos.zip"
        s3_client.upload_fileobj(zip_buffer, S3_BUCKET, s3_key)
        pre_signed_url = generate_presigned_url(s3_key)

        return pre_signed_url
    except Exception as e:
        print(f"An error occurred while zipping and uploading to S3: {e}")
        return None


async def organize_photos_in_s3(file_objects):
    """
    Organizes photos in S3 by year and month based on their EXIF data.
    """
    try:
        folder_name = "organized_photos"

        updated_files = []

        for file_obj in file_objects:
            # print(f"File_Objects Pointer -> {file_objects}")

            file_name = file_obj.filename
            file_content = file_obj.file

            # Read file content and keep it in memory
            content = await file_obj.read()

            # Extract the data from the image
            img_date = image_date_extractor(io.BytesIO(content))

            # Reset file pointer to the beginning for upload
            file_content.seek(0)

            # Extract year and month
            year = img_date.strftime("%Y")
            month = img_date.strftime("%B")

            # Create S3 key (path) for the file
            # This is like simulating the directory structure on local machine
            s3_key = f"{folder_name}/{year}/{month}/{file_name}"

            # Upload the file to S3
            # Each photo is uploaded to S3 with its corresponding key.
            # This creates the appearance of directories based on the year and month in the S3 console.
            s3_client.upload_fileobj(file_content, S3_BUCKET, s3_key)

            print(f"Uploaded '{file_name}' to '{s3_key}'")

            # Recreate file-like object for reuse
            updated_files.append((s3_key, io.BytesIO(content)))

        success_message = "Photos organized successfully!"

        return updated_files, success_message

    except Exception as e:
        print(f"An error occurred while organizing photos: {e}")

        return f"An error occurred while organizing photos: {e}"
