# Starter project template: Dockerized hybrid Django React app 
Starter project template using docker to build a Django app that serves React apps statically (as JavaScript files)

Stack:
  - Django (with Rest framework, PostgreSQL, SMTP gmail backend, whitenoise, etc.)
  - React (bundled with webpack and transpiled with babel)
  - Docker
  - Deployment to Heroku

## First Setup

1. Make sure poetry is installed `pip install poetry`
2. Execute `python setup/run.py` or `py setup\run.py`
3. After the project is setup, start the docker container to start working `docker-compose up -d`. The "setup" folder will delete itself after setting up the project, as to leave a cleaner project.

## Debugging with Docker and VSCode

Support for debugging remotely if you're running with Docker is supported out-of-the-box.

To debug with Docker:

1. Rebuild and run your Docker containers as usual: `docker-compose up --build`

3. Start the debug session from VS Code for the `[django:docker] runserver` configuration

   1. Select `[django:docker] runserver` from the dropdown near the Play button in the top left.

   3. Hit the Play button or hit `F5` to start debugging

      - Logs will redirect to your integrated terminal as well.

4. Set some breakpoints in functions or methods executed when needed. Usually it's Model methods or View functions

## Adding external libraries

It's better to install external libraries from from Docker directly

1. Python libraries:
   1. `docker-compose exec web poetry add [pip_package]` for production libraries
      - Example: `docker-compose exec web poetry add django-extensions`
   2. `docker-compose exec web poetry add [pip_package] --dev` for development libraries
      - Example: `docker-compose exec web poetry add --dev selenium`
2. JavaScript libraries:
   1. `docker-compose exec web npm install [npm_package]` for production libraries
      - Example: `docker-compose exec web npm install lodash`
   2. `docker-compose exec web npm install -D [npm_package] --dev` for development libraries
      - Example: `docker-compose exec web npm install --dev jest`

## Deploy to Heroku
### First setup
Followed guide of "Django for professionals" book

### Consecutive deployments to production
Deploy by pushing to Heroku git repository:
```git push heroku main```
