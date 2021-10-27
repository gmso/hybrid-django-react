# Template: Dockerized hybrid Django React app 
Template using docker to build a Django app that serves React apps statically (as JavaScript files)

Stack:
  - Django (with Rest framework)
  - React
  - Docker
  - Deployment to Heroku

## First Setup

Make sure poetry is installed `pip install poetry`
Execute `py template-setup.py`

## Debugging with Docker and VSCode

Support for debugging remotely if you're running with Docker is supported out-of-the-box.

To debug with Docker:

1. Rebuild and run your Docker containers as usual: `docker-compose up --build`

3. Start the debug session from VS Code for the `[django:docker] runserver` configuration

   1. Select `[django:docker] runserver` from the dropdown near the Play button in the top left.

   3. Hit the Play button or hit `F5` to start debugging

      - Logs will redirect to your integrated terminal as well.

4. Set some breakpoints in functions or methods executed when needed. Usually it's Model methods or View functions

## Deploy to Heroku
Followed guide of "Django for professionals" book

Deploy by pushing to Heroku git repository:
```git push heroku main```