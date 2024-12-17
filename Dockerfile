FROM python:3.8-slim

WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt /app/

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files into the container
COPY . /app/

EXPOSE 9696

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:9696", "app:app"]
