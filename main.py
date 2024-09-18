from fastapi import FastAPI, UploadFile, File, Request
import tempfile
import shutil 
import json , os
from fastapi.middleware.cors import CORSMiddleware
from inference import img_to_caption, download_s3_image_without_boto3
import uvicorn

app = FastAPI()





@app.get("/")
def read_root():
    return {"message": "Hello, World!"}


@app.post("/get_url_content/")
async def get_url_content(request: Request):
    try:
        data = await request.json()
        url = data.get("url")
        if not url:
            return {"error": "URL parameter is missing"}
        
        local_path = url.split('/')
        download_s3_image_without_boto3(url, local_path[-1])
        response = img_to_caption([local_path[-1]])
        os.remove(local_path[-1])
        
        return {"success": True,  "response": response}

    except Exception as e:
        return {"error": str(e)}
    


@app.post("/upload_pdf/")
async def upload_pdf(file: UploadFile = File(...)):

    with tempfile.NamedTemporaryFile(delete=True) as tmp:
        tmp.write(await file.read())
        tmp.seek(0)
        print(file.filename)
        image = convert_tempfile_to_pdf(tmp.name,output_path=file.filename)
        # print(image, type(image))
        response = img_to_caption([image])
        

        return {"success": True,  "response": response}
    # except Exception as e:
    #     return {"success": False, "error": str(e)}


def convert_tempfile_to_pdf(tempfile_path, output_path):
    # Copy the temporary file to the output path with a .pdf extension
    shutil.copyfile(tempfile_path, output_path)
    return output_path


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080)