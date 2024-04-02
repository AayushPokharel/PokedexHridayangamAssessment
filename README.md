# Pokedex | FastApi App
## Assessment Project

Pokedex is the a fast api based application that queries the endpoint [pokeapi.co](https://beta.pokeapi.co/graphql/v1beta) to seed the database at application startup and serves a `HTTPResponse` at `/api/v1/pokemons`.

The `HTMLResponse` is created with `Jinja2` Template and uses `tailwindcss` for styling. The html page has embeded js script that dynamically filters the list of pokemon based on types and/or name.

## Table of Contents

- [Pokedex | FastApi App](#pokedex--fastapi-app)
  - [Assessment Project](#assessment-project)
  - [Table of Contents](#table-of-contents)
  - [Usage](#usage)
    - [Running Locally](#running-locally)


## Usage
Instructions on how to use the project, including how to run the code locally and how to compile it.

### Running Locally

Create the virtual environment with the fillowing command.
`python3 -m venv env`

Activate the virtual environment.
`source env/bin/activate`

Install dependencies required for the project.
`pip install -r requirements.txt`

Run the Postgres server locally with docker compose with the following command.
`cd .devcontainer`
`docker compose up`

Run the server with 
`uvicorn main:app --reload`
