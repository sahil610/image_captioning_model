
# ENV NAME World
# # Run app.py when the container launches
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]





FROM python:3.9-slim-buster
# FROM python:3.9

WORKDIR /app


COPY main.py ./
COPY inference.py ./
COPY utils.py ./
COPY requirements.txt ./
# RUN pip install -r requirements.txt  -t .
RUN pip install --no-cache-dir -r requirements.txt


COPY checkpoints /app/checkpoints
COPY configs  /app/configs
COPY models /app/models

# ENV NAME World


EXPOSE 8080  

# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]

# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
ENTRYPOINT ["python3", "main.py"]




# Run gunicorn with uvicorn worker class
# CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "main:app", "--workers", "4", "--bind", "0.0.0.0:8080"]
