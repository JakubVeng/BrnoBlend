### Deps

The dependencies are in `requirements.txt` for now. Use venv to create virtual environment
for local development. Don't screw your system python :D. Later I'll add pipenv or something
that natively creates venv.

### Running the app

In the root of git repo, run:

```bash
$ podman-compose up -d
```

Then you need to initialize database with data. Go to
the `src` directory inside container and run:

```bash
$ ./manage.py refresh-events
```

### Accessing the app

Go to `localhost:5020` in your browser.

### Debugging and local development

The API should reload itself when you change the code. If this doesn't happen, you can
change the command inside compose file to `"/bin/bash"`, then run the containers again
and run the server manually:

```bash
$ uvicorn src/app/api:app --host 0.0.0.0 --port 5020 --reload
```

To enter running container with python API, run:

```bash
$ make enter-container
```
