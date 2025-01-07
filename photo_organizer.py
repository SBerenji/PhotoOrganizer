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

    except Exception as e:
        print(f"Error extracting date from image: {e}")
        return datetime.now()


def organize_photos_in_s3(file_objects):
    """
    Organizes photos in S3 by year and month based on their EXIF data.
    """
    try:
        for file_obj in file_objects:
            file_name = file_obj.filename
            file_content = file_obj.file

            # Extract the data from the image
            img_date = image_date_extractor(file_content)

            # Rest file pointer to the beginning for upload
            file_content.seek(0)

            # Extract year and month
            year = img_date.strftime("%Y")
            month = img_date.strftime("%B")

            # Create S3 key (path) for the file
            # This is like simulating the directory structure on local machine
            s3_key = f"photos/{year}/{month}/{file_name}"

            # Upload the file to S3
            # Each photo is uploaded to S3 with its corresponding key.
            # This creates the appearance of directories based on the year and month in the S3 console.
            s3_client.upload_fileobj(file_content, S3_BUCKET, s3_key)

            print(f"Uploaded '{file_name}' to '{s3_key}'")

        return f"Photos organized successfully! Please download the organized folders from the link below."

    # except NoCredentialsError:
    #     return "AWS credentials are missing or incorrect."

    except Exception as e:
        return f"An error occurred while organizing photos: {e}"
