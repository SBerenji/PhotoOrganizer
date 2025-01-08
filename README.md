
# Photo Organizer





## Project Overview

Photo Organizer is a web application designed to simplify photo organization by allowing users to upload, categorize, and download large collections of photos. The application organizes photos by year and month using AWS S3 for scalable storage and enables users to download their collections as a ZIP file.

Check it out live: https://photo-organizer.onrender.com/
## Packages & Tools Used

- AWS S3
- FastAPI
- Docker
- GitHub Actions
- boto3
- HTML
- CSS
- JavaScript
- Bootstrap

## Features
- **Bulk Uploads**: Upload thousands of photos seamlessly using AWS S3 for storage.
- **Photo Organization**: Automatically categorizes photos into folders by year and month.
- **Download as ZIP**: Retrieve organized photos as a downloadable ZIP file with one click.
- **Responsive Interface**: Provides a user-friendly interface for smooth uploads and downloads.
## Installation

- **Prerequisites**: Ensure you have the following installed:  
  - **Python 3.9**: Required for running the application.  
  - **Docker (optional)**: For containerized deployment.  
  - **AWS Account**: Set up with an S3 bucket for storage.  

- **Clone the Repository**:  
  Clone the project to your local machine:  

  ```bash
  git clone https://github.com/SBerenji/PhotoOrganizer.git
  cd photo-organizer

- **Create a virtual environment**:  
    ```bash
    python -m venv {name of your virtual environment}

- **Activate virtual environment (bash version)**:  
   ```bash
    source {name of your virtual environment} \ Scirpts \ Activate"


- **Install Dependencies**:  
    Install the necessary Python packages:

  ```bash
  pip install -r requirements.txt


- **Set Up Environment Variables**:  
      Create a .env file with your AWS credentials:

  ```bash
    AWS_ACCESS_KEY=your-aws-access-key
    AWS_SECRET_ACCESS_KEY=your-aws-secret-key
    S3_BUCKET=your-s3-bucket-name
    S3_REGION=your-s3-region


- **Run Locally**:  
   Start the application using Uvicorn:

  ```bash
  uvicorn app:app --reload


- **Run in Docker (Optional):**:  
  Build and run the application in a Docker container:
  ```bash
  docker build -t photo-organizer .
  docker run -p 8000:8000 photo-organizer
