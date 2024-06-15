### Deps

The dependencies are in `requirements.txt` for now. Use venv to create virtual environment
for writing the code locally (for IDEs). Don't screw your system python :D. Later I'll
add pipenv or something that natively creates venv.

### Running the app

To run the app you need to run it inside container (if locally on your machine, you are on your
own with resolving dependencies, running all the services, etc). In the root of git repo, run:

```bash
# with make - this chooses podman on docker depending what's on ur system
$ make app-up
# or with compose - if you have docker then use docker-compose instead
$ podman-compose up -d
```

To shutdown app

```bash
$ make app-down
# or with compose - if you have docker then use docker-compose instead
$ podman-compose down
```

To enter running container with python API, run:

```bash
$ make enter-container
# or manually with docker/podman
$ podman exec -it brnoblend_web bash
```

Then you need to create tables inside container (this can be done in Containerfile...
still TODO) and then initialize database with data. Go to
the `src` directory inside container and run:

```bash
$ ./manage.py create-db  # run this only for the first time to create tables
$ ./manage.py refresh-events  # this populates/refreshes data in the db
```

### Accessing the app

Go to `localhost:5020` in your browser.

To see what's inside the database, you can use adminer. Go to `localhost:8080` in your
browser. Use the PostgreSQL and credentials needed to log into the database are
inside `files/env` file.

### Debugging and local development

The API should reload itself when you change the code. If this doesn't happen, you can
change the `command` inside compose file to `"/bin/bash"`, then run the containers again
and run the server manually:

```bash
$ uvicorn src/app/api:app --host 0.0.0.0 --port 5020 --reload
```
