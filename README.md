# User Manager

## Generate and Run Database Migrations

1. Generate a new migration
  1. `flask db migrate -m "message"`
1. Apply migration to database
  1. `flask db upgrade`

## Seed database

1. After running migrations, setup seed data
  1. `flask seed run`
1. Add the roles in this format(Admin, Provider, Patient, User)

## Run "user_manager" application

1. from /user-manager/user_manager
  1. Install dependencies using [Pipenv](https://pipenv-fork.readthedocs.io/en/latest/basics.html)
    1. `pip install pipenv`
    1. `pipenv install`
    1. `pipenv shell`
  1. Run application
    1. `python app.py`
      1. If you get a path error "No such file or directory for app.py"
      1. Start app with: `python -m flask run` OR include the full path (eg  `python /Users/laura/workspace/user-manager/user_manager/app.py`)

## Environment Variables

1. Create a file called ".env"
  1. See ".env.example" for the required environment variables

## Contributing
1. Ensure your syntax is cleaned up before you commit, install [pre-commit](https://pre-commit.com/)
    1. MacOS: Run: `brew install pre-commit`, other operating systems, see link above.
1. Commit message format:

- Format:

        [STORY ID] COMMIT TITLE

        - ITEM COMPLETED
        - ANOTHER ITEM COMPLETED

- Example:

        ESSW-66 add endpoint for getting patients

        - add test coverage to Patients resource
        - update Patient schema to show nested attributes

## Docker

1. build image (name it something short a sweet with `-t` flag)
    1. run `docker build -t um .`
    1. note: be sure that you are in the same directory as your Dockerfile (eg user-manager/user_manager)
1. run docker image
   1. run `docker run -p 5000:5000 um`
   1. "um" below refers to the tag we created in the previous step
