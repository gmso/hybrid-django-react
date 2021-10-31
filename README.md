## Starter project template
# 🤠⚛️ Dockerized hybrid Django React app 
Starter project template using Docker to build a Django app that serves React apps statically (as JavaScript files)

## Tech stack
  - Django (with Rest framework, PostgreSQL, SMTP gmail backend, whitenoise, etc.)
  - React (bundled with webpack and transpiled with babel)
  - Docker
  - Deployment to Heroku

## Prerequisites
  - Docker
  - pip, poetry, pyenv or a similar tool to access [pypi](https://pypi.org/)

## Installation
Install with the following command
```
pip install hybrid-django-react
```

## Usage
Run the scripts with the following command:
```
create-django-react-app
```

You will be prompted for some information like project name, email, etc. This data is needed to change the configuration files accordingly

After the script has run, you don't need this tool anymore 😀

Simply start the docker container to start working:
```
docker-compose up -d
```

You can then work as usual on your Django project.

The entry point of the React render can be edited from the file `frontend/index.js`

## Debugging with Docker and VSCode

Support for debugging remotely with VSCode is supported out-of-the-box.

To debug with Docker:

1. Run your Docker containers as usual: `docker-compose up -d --build`

3. Start the debug session from VS Code for the `[django:docker] runserver` configuration (either from the Debugger menu or with `F5`)

   - Logs will redirect to your integrated terminal as well.

4. Set some breakpoints in functions or methods executed when needed. Usually it's Model methods or View functions

## Adding external libraries

It's better to install external libraries from from Docker directly

### Python libraries:
   - Production libraries
   ```
   docker-compose exec web poetry add [pip_package]
   ```
   - Development libraries
   ```
   docker-compose exec web poetry add [pip_package] --dev
   ```
### JavaScript libraries:
   - Production libraries
   ```
   docker-compose exec web npm install [npm_package]
   ```
   - Development libraries
   ```
   docker-compose exec web npm install -D [npm_package]
   ```

## Deploy to Heroku
### First setup
1. [Create an account](https://www.heroku.com) and [install Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)  
2. Create a new app on Heroku
   ```
   heroku create
   ```
   Your app will get a randomly generated name, like _lazy-beyond-52146_. Let's call this name _[APP_NAME]_
3. Add environment variables that Django needs to read:
   1. DJANGO_ENVIRONMENT:
      ```
      heroku config:set DJANGO_ENVIRONMENT=production
      ```
   2. DJANGO_SECRET_KEY:
      You can create a safe secret key [using this site](https://djecrety.ir/)
      ```
      heroku config:set DJANGO_SECRET_KEY=[secret_key]
      ```
   3. DJANGO_DEBUG:
      ```
      heroku config:set DJANGO_DEBUG=False
      ```
4. Set the stack to Docker containers using the app's name
   ```
   heroku stack:setcontainer -a [APP_NAME]
   ```
5. Create a managed postgresql database on Heroku
   ```
   heroku addons:create heroku-postgresql:hobby-dev -a [APP_NAME]
   ```
6. Create a heroku remote repository and push changes to it
   ```
   heroku git:remote -a [APP_NAME]
   git push heroku main
   ```
7. Migrate Database and create superuser
   ```
   heroku run python manage.py migrate
   heroku run python manage.py createsuperuser
   ```
8. After deployment, check that the site's [security audit shows no warnings](https://djcheckup.com/)

### Consecutive deployments to production
Deploy by pushing to Heroku git repository:
```
git push heroku main
```
