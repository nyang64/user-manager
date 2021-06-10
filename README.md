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
  1. Global setup:
        1. Pre-commit needs to be added to your machine's global packages.
        1. MacOS: Run: `brew install pre-commit`
        1. Other operating systems, see [pre-commit](https://pre-commit.com/) website.
  1. Local setup:
    1. Pre-commit needs to be added to your local .git directory within each project.
    1. Once "pre-commit" is installed globally on your machine, you need to set it up locally for each project.
      1. From /user-manager run `pre-commit install`.
  1. Pre-commit hooks are linter tests that run each time you attempt to commit. If the tests pass, the commit will be made, otherwise:
    1. Black may make syntax changes may be made on your behalf.
      1. The files that were changes will be taken off of git's "stage" and you will need to add them back.
    1. Read the message from "pre-commit" carefully, you may need to manually remove an unused dependency. Once, you have done this, add the file back to git's "stage" and try committing again.
    1. Code style has been implemented using [Black](https://github.com/psf/black).
      1. Black is a PEP 8 compliant opinionated formatter. Black reformats entire files in place. It is not configurable. It doesn't take previous formatting into account.
      1. [Black's opinions](https://github.com/psf/black/blob/master/docs/the_black_code_style.md)
      1. See configuration files: and Flake8. See configuration files: .isort.cfg, .pre-commit-config.yaml, pyproject.toml  and setup.cfg.
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


 ## To Run Test Case

 1. Set the env variable mentioned below(For window replace export with set)
  export POSTGRES_DB_PORT=5432
  export POSTGRES_DB_USER_KEY=avilash
  export POSTGRES_DB_PASSWORD_KEY=avilashjha
  export POSTGRES_DB_HOST=localhost
  export POSTGRES_TEST_DB_NAME=user_test_db
  export ACCESS_TOKEN_KEY=C718D5FDDEC279567385BE3E52894
  export REFRESH_TOKEN_KEY=9EA72AD96C39A87A1AFF153983592
  export DEVICE_BASE_URL=http:/fake.com
  export SECRET_MANAGER_ARN=value
  export OTP_EXPIRATION_TIME_HOURS=1
  export OTP_EXPIRATION_TIME_MINUTES=20
  export OTP_LIMIT=1
  export OTP_LIMIT_HOURS=1
  export OTP_LIMIT_MINUTES=20
2. Run command:
    - pytest
3. To run particular file test case
    - pytest <file_path>

## To get the code coverage

1. set the env variables
2. coverage run -m pytest
3. coverage html (Create a html dir -> htmlcov)
4. coverage report (Show report in console)
