# Recruitment

### Overview
This project is a mockup of a recruitment website, allowing users to search and filter through different job listings.

[video demo](https://youtu.be/8U7NlKIL6ZM)

[Website hosted on AWS](https://tinyurl.com/recruitmentmockup)

### Features
- Web Scraping: Job listings are scraped from [SCIENTE International](https://www.sciente.com/business-technology-jobs/). The data is then processed by the Gemini API, which fills in the missing fields.
- Search: returns all job listings where the query matches the title, description, loaction, company or job type.
- Filter: filter jobs according to salary, distance from an address, job type or date.
- Sort: orders the results based on salary, recency or proximity.


### Running Locally
1. Edit database configuration in `settings.py`:
    ```python
    DATABASES = {
        'default': {
            'ENGINE': 'django.contrib.gis.db.backends.postgis',
            'NAME': 'postgres', 
            'USER': 'postgres',
            # Ensure you enter a postgres password into your environment variables
            'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
            # Change HOST to 'db'
            'HOST': 'db',
            'PORT': '5432',
        }
    }
    ```
2. Docker:
    - Ensure [Docker](https://docs.docker.com/engine/install/) is installed and running in the background.
3. Run locally with the following command:
    ```bash
    $ docker-compose up --build
    ```
    The website should run at 127.0.0.1:8000

    



