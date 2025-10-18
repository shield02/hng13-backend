# Backend - Stage 0 Task

## Task - Profile Endpoint

In this task, I build a simple RESTful API endpoint that 
returns my profile information along with a dynamic cat fact 
fetched from an external API. This task validates my ability 
to consume third-party APIs, format JSON responses, and return 
dynamic data.

The endpoint:
- is `/me`
- returns JSON data with Content-Type: `application/json
- integrate with the [Cats Facts API](https://catfact.ninja/)

## How to Run the App Locally

`make setup`: create venv, install deps, create .env

`make run`: start Flask app

`make test`: run all tests in /test

`make deploy` push to Heroku and open app in default browser

`make clean`: cleanup things
