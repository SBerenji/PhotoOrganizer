from fastapi import FastAPI, Form,  UploadFile, File, Request
from photo_organizer import organize_photos_in_s3
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

# Initialize FastAPI app
app = FastAPI()


# Telling FastAPI where to look for the static files (CSS and JS) /  Mounting static files
app.mount("/static/CSS", StaticFiles(directory="static/CSS"), name="staticCSS")
app.mount("/static/JS", StaticFiles(directory="static/JS"), name="staticJS")

# Load templates directory for HTML files
templates = Jinja2Templates(directory="./templates")


# Route to render the main page
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# Route to process the form submission and display the result
@app.post("/organize-photos")
async def organize_photos(files: list[UploadFile] = File(...)):
    try:
        # Debug: Print file names to confirm receipt
        file_names = [file.filename for file in files]
        print(f"Received files: {file_names}")

        # Pass uploaded files to the script to organize in S3
        result_message = organize_photos_in_s3(files)
        return {"message": result_message}

    except Exception as e:
        return {"error": str(e)}

    #     return templates.TemplateResponse("result.html", {"request": request, "result_message": result_message})
    # except Exception as e:
    #     # In case of error, render the result page with an error message
    #     return templates.TemplateResponse("result.html", {"request": request, "result_message": f"Error: {str(e)}"})


# app.post("/upload-photos")
# async def upload_photos(files: list[UploadFile] = File(...)):
#     uploaded_files = []

#     try:
#         # Iterate through all uploaded files
#         for file in files:
#             # Generate a unique path for each file in the S3 bucket
#             s3_key = f"/photos{file.filename}"

#             # Upload the file to S3
#             s3_client.upload_fileobj(file.file, S3_BUCKET, s3_key)

#             # Append the S3 file URL to the list
#             uploaded_files.append(
#                 f"https://{S3_BUCKET}.s3.{S3_REGION}.amazonaws.com/{s3_key}")

#             return {"message": "Files uploaded successfully!", "files": uploaded_files}

#     except NoCredentialsError:
#         return {"error": "AWS credentials are missing or incorrect."}

#     except Exception as e:
#         return {"error": str(e)}
