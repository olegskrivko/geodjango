FROM python:3.11-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal

# Add these environment variables here:
ENV USE_GEOS=1
ENV USE_PROJ=1
ENV USE_STATS=1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    binutils libproj-dev gdal-bin libgdal-dev \
    gcc libc6-dev g++ make python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Match Python GDAL to system GDAL
RUN GDAL_VERSION=$(gdal-config --version) && \
    echo "Installing GDAL Python bindings version: $GDAL_VERSION" && \
    pip install "GDAL==$GDAL_VERSION"

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput || true

#LOCAL
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
#PROD
CMD ["gunicorn", "backend.wsgi:application", "--bind", "0.0.0.0:8000"]