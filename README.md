# Recruitment

### Overview
This project is a mockup of a recruitment website, allowing users to search and filter through different job listings.

(video demo)[https://youtu.be/8U7NlKIL6ZM]

### Features
- Search: returns all job listings where the query matches the title, description, loaction, company or job type.
- Filter: filter jobs according to salary, distance from an address, job type or date.
- Sort: orders the results based on salary, recency or proximity.


### Setup
1. GDAL:
    - Install with the following link: https://trac.osgeo.org/osgeo4w/
    - Edit the file path in `settings.py`:
    ```python
    # * Replace with the path to your GDAL library
    GDAL_LIBRARY_PATH = "C:/OSGeo4W/bin/gdal309.dll"
    ```
2. PostgreSQL:
    - Install with the following link: https://www.postgresql.org/download/
    - Edit the database configuration in `settings.py`:
    ```python
    DATABASES = {
        'default': {
            'ENGINE': 'django.contrib.gis.db.backends.postgis',
            # * Replace with your own database details
            'NAME': 'DATABASE_NAME', 
            'USER': 'DATABASE_USER',
            'PASSWORD': 'DATABASE_PASSWORD',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }
    ```
3. Run locally with the following command:
    ```bash
    $ ./run
    ```

    



