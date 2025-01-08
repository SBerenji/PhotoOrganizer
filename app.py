from fastapi import FastAPI, Form,  UploadFile, File, Request
from photo_organizer import organize_photos_in_s3, zip_and_upload_to_s3
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
async def organize_photos(request: Request, files: list[UploadFile] = File(...)):
    try:
        # Debug: Print file names to confirm receipt
        # file_names = [file.filename for file in files]
        # print(f"Received files: {file_names}")

        # Pass uploaded files to the script to organize in S3
        updated_files, result_message = await organize_photos_in_s3(files)

        download_link = await zip_and_upload_to_s3(updated_files, "organized_photos")

        return templates.TemplateResponse(
            "result.html",
            {"request": request, "result_message": result_message,
                "download_link": download_link}
        )
    except Exception as e:
        # In case of error, render the result page with an error message
        return templates.TemplateResponse("result.html", {"request": request, "result_message": f"Error: {str(e)}"})
