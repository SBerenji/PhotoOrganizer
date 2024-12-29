from fastapi import FastAPI, Form
from fastapi.responses import JSONResponse
from photo_organizer_script import main
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
# BaseModel from Pydantic is a class used to
# define data models that automatically validate, parse, and serialize input data in FastAPI.
from pydantic import BaseModel
from fastapi import Request

app = FastAPI()

# Initialize Jinja2Templates for HTML rendering
templates = Jinja2Templates(directory="templates")

# Telling FastAPI where to look for the static files (CSS and JS)
app.mount("/static", StaticFiles(directory="static"), name="static")


# Pydantic model for the file path request which helps with validation
class FilePathRequest(BaseModel):
    file_path: str


# Route to render the main page
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# Route to process the form submission and display the result
@app.post("/organize-photos", response_class=HTMLResponse)
async def organize_photos(request: Request, filePath: str = Form(...)):
    try:
        # Call the photo organizing script with the file path
        result_message = main(filePath)
        # Render result.html page with the result message passed to the template
        return templates.TemplateResponse("result.html", {"request": request, "result_message": result_message})
    except Exception as e:
        # In case of error, render the result page with an error message
        return templates.TemplateResponse("result.html", {"request": request, "result_message": f"Error: {str(e)}"})
