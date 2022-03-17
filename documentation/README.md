# Documentation
Below listed all the devops technologies tested. 

## Local Development
To develop locally on Windows work on the code. To test open command prompt `cd` to the folder and run:

`set FLASK_APP=app.py && flask run`

![Local Development](local.jpg)

## Github Actions
I am using `pytest` and Github Actions (see also the workflow file `fundmapper-webapp/.github/workflows/python-app2.yml`). Tests execute fine and are set to 
be run on every push to `main` or pull request to `main`.
![Github Actions](github_actions.jpg)

This is really useful! When I updated `numpy` to avoid, the tests failed showing me that I need a different version of `pandas` now as well:
![Github Actions](github_actions2.jpg)


## Docker
To create the docker image:

`docker build --tag fundmapper .`

To run it:

`docker run -d -p 8000:5000 fundmapper` 

![Docker](docker.jpg)



## Kubernetes


## Deployment / Serving on AWS
