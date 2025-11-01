# DJANGO PROJECT TEMPLATE

This repository's purpose is to help newcomers get their first Django project
ready for development as soon as possible. It includes a minimal set of
dependencies, a pre-configured Django project structure, and supporting
services via Docker containers.

## Repository Creation

The main document is here:
[ref](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-repository-from-a-template).

In short, hit the "Use this template" button and select the "Create a new
repository" option. This will create your own repository using this template.
After that, you're free to do whatever you want with your OWN repository.

## Setting Up Virtual Environment

Virtual environment
: A cooperatively isolated runtime environment that allows Python users and
applications to install and upgrade Python distribution packages without
interfering with the behavior of other Python applications running on the same
system.

The easiest way to start using virtual environments is to use the built-in
[venv](https://docs.python.org/3/library/venv.html) library.

To create a new virtual environment, pass the path where you want to place the
environment to the `venv` package from the standard library:

```shell
python -m venv ${ENVIRONMENT_NAME}
```

This will create a new environment ready to use with your project. To activate
it:

```shell
source ${ENVIRONMENT_NAME}/bin/activate  # if you are on macOS or Linux
${ENVIRONMENT_NAME}\Scripts\activate     # if you are using Windows
```

To deactivate, type `deactivate` in your terminal and hit Enter.

## Installing Dependencies

This project uses modern Python packaging standards with `pyproject.toml`. You
can install dependencies using pip or uv (recommended for faster installs).

### Using pip

```shell
pip install -e .
```

### Using uv (recommended)

First, install uv if you haven't already:

```shell
# On macOS and Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# On Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Or with pip
pip install uv
```

Then create a virtual environment and install dependencies:

```shell
uv venv
source .venv/bin/activate  # On macOS/Linux
# or
.venv\Scripts\activate     # On Windows
uv pip install setuptools
uv sync
```

The `uv sync` command will automatically install all dependencies from the lock
file.

### Development Dependencies Only

If you've already installed dependencies and want to add development tools:

```shell
uv sync --extra dev
```

Or to install without development dependencies:

```shell
uv sync --no-dev
```

This project comes with a minimal list of dependencies:

| Package       | Version | Package homepage           |
|:--------------|:-------:|:---------------------------|
| Django        | ≥5.2.7  | https://djangoproject.com/ |
| psycopg       | latest  | https://www.psycopg.org/   |
| pytest-django | latest  | (dev only)                 |
| black         | ≥25.9.0 | (dev only)                 |

Django
: Django is a high-level Python web framework that encourages rapid development
and clean, pragmatic design. Built by experienced developers, it takes care of
much of the hassle of web development, so you can focus on writing your app
without needing to reinvent the wheel. It's free and open source.

psycopg
: Psycopg 3 is the modern PostgreSQL adapter for Python. It provides a complete
implementation of the Python DB API 2.0 specifications with async support and
improved performance. The `psycopg[binary]` package includes pre-compiled
binaries suitable for development.

## Django Project Structure

This template comes with a pre-configured Django project located in the `src/`
directory:

```
src/
├── manage.py              # Django management script
└── project_core/          # Main project package
    ├── __init__.py
    ├── settings.py        # Project settings (PostgreSQL configured)
    ├── urls.py            # URL routing
    ├── asgi.py            # ASGI entry point
    └── wsgi.py            # WSGI entry point
```

You can start development immediately without running
`django-admin startproject`.

## Database Configuration

The project is pre-configured to use PostgreSQL. The default settings in
`src/project_core/settings.py` are:

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": "localhost",
        "PORT": "5432",
        "NAME": "django",
        "USER": "django",
        "PASSWORD": "django",
        "TEST": {
            "NAME": "django_test",
        },
    },
}
```

Make sure you have PostgreSQL running with a database named `django` and a user
`django` with password `django`. Or use the Docker Compose setup described
below.

## Using Docker Compose

Prerequisites:

* Docker and Docker Compose installed

This project includes a Docker Compose configuration to deploy recommended
services for Django development. If you're not familiar with Docker Compose,
it's a tool for defining and running multi-container Docker applications.
([Learn more](https://docs.docker.com/compose/)).

The installation process is described
[here](https://docs.docker.com/compose/install/).

The compose file defines a set of services for development:

* **PostgreSQL** - Database server
* **pgAdmin** - PostgreSQL administration web interface
* **MailHog** - Email testing tool with web interface
* **Caddy** - Web server for serving static files

Default mapped ports:

* 5432 for PostgreSQL
* 8032 for pgAdmin web interface
* 1025 for SMTP (MailHog)
* 8025 for MailHog web interface
* 8888 for static files (Caddy)

You can change these values by setting environment variables (see below).

Container management:

```shell
cd containers
docker compose up -d  # start all containers
docker compose down   # stop all containers
docker compose logs   # view logs
```

### Setting Up Environment Variables

Some settings in the compose file can be overridden using environment
variables. If you're not familiar with them, here's a
[Wiki article](https://en.wikipedia.org/wiki/Environment_variable).

Set environment variables in your terminal:

```shell
export VARIABLE=value  # for Unix users (Linux and macOS)
set VARIABLE=value     # for Windows users (Command Prompt)
$env:VARIABLE="value"  # for Windows users (PowerShell)
```

### PostgreSQL

The `database` service runs a PostgreSQL 16.10 Alpine container. It exposes
port 5432 to the host machine, so you can use it as if PostgreSQL were running
natively on your system.

The default port mapping is "5432:5432". If port 5432 is already occupied, you
can set a different port using the `POSTGRES_PORT` environment variable.

Pre-defined credentials:

| Role      | Username | Password |
|:----------|:---------|:---------|
| Superuser | postgres | postgres |
| App User  | django   | django   |

The `django` user and database are automatically created on first startup via
the initialization script in `containers/postgres/initdb.sql`.

You can run this service separately:

```shell
cd containers
docker compose up -d database
```

### pgAdmin

pgAdmin is a feature-rich PostgreSQL administration and development platform.
It provides a web-based interface for managing your PostgreSQL databases.

The pgAdmin container exposes port 80, mapped to port 8032 on the host by
default. You can change this using the `PGADMIN_PORT` environment variable.

Pre-defined credentials for pgAdmin web interface:

| Email                 | Password |
|:----------------------|:---------|
| pgadmin@devsforge.org | pgadmin  |

After running pgAdmin, visit http://localhost:8032 in your web browser (adjust
the port number if needed).

The connection to the PostgreSQL server is pre-configured via the
`containers/pgadmin/servers.json` file. When you log in, you'll see the "
PostgresSQL Server" already configured and connected to the `database` service.

You can run this service separately:

```shell
cd containers
docker compose up -d pgadmin
```

### MailHog

MailHog is an email testing tool for developers. It captures emails sent by
your Django application and provides a web interface to view them.

The MailHog container exposes two ports:

* Port 1025 for SMTP (configure this in your Django settings)
* Port 8025 for the web interface

Default port mappings: "1025:1025" and "8025:8025". You can customize these
using the `SMTP_PORT` and `SMTP_WEB_PORT` environment variables.

After running MailHog, visit http://localhost:8025 in your web browser to view
captured emails.

To configure Django to use MailHog, add this to your settings.py:

```python
# Email configuration for development
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025
EMAIL_USE_TLS = False
EMAIL_USE_SSL = False
```

### Caddy

Caddy is a modern, production-ready web server with automatic HTTPS. In this
setup, it's used to serve static files during development.

The container exposes port 80, mapped to port 8888 on the host by default. You
can change this using the `STATIC_PORT` environment variable.

Local storage for static files is the `staticfiles/` directory. Place your
content there, and it will be available at http://localhost:8888/path/to/file.

This directory is configured as `STATIC_ROOT` in settings:

```python
STATIC_ROOT = BASE_DIR.parent / "staticfiles"
```

After running the container, visit http://localhost:8888 in your browser (
adjust the port number if needed).

You can run this service separately:

```shell
cd containers
docker compose up -d staticfiles
```

## Running Django

Once dependencies are installed and PostgreSQL is running, you can use standard
Django management commands:

```shell
cd src

# Run migrations
python manage.py migrate

# Create a superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver

# Collect static files
python manage.py collectstatic
```

The development server will be available at http://localhost:8000.

## Code Quality Tools

This project includes configuration for maintaining code quality:

### EditorConfig

The `.editorconfig` file ensures consistent coding styles across different
editors and IDEs. Most modern editors support EditorConfig automatically or via
plugins.

### Black

Black is an opinionated code formatter included in the dev dependencies:

```shell
# Format all Python files
black src/

# Check formatting without making changes
black --check src/
```

### Running Tests

The project includes pytest-django for testing:

```shell
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test file
pytest src/tests/test_example.py
```

## Check Lists

So far and don't know how to start? Here's a simple checklist to help you with
your first steps learning the Django framework.

### Project Setup

- [ ] Create a local virtual environment
- [ ] Install base dependencies using pip or uv
- [ ] Start Docker containers for database and supporting services
- [ ] Run Django migrations (`python manage.py migrate`)
- [ ] Create a superuser (`python manage.py createsuperuser`)
- [ ] Update README file with information relevant to your project

## Migration from Previous Versions

If you're migrating from an older version of this template:

### From Poetry to uv/pip

1. Remove `poetry.lock` if it exists
2. Install dependencies using pip or uv as described above
3. Update your CI/CD pipelines to use the new dependency management

### Docker Compose Changes

1. Use `containers/compose.yaml` instead of `docker-compose.yml`
2. Update database credentials from `postgres/postgres` to `django/django`
3. Update static files path from `static/` to `staticfiles/`
4. pgAdmin is now included (port 8032 by default)
5. Update port references (static files now on 8888 instead of 8080)

### Database Adapter Changes

The project now uses `psycopg` (version 3) instead of `psycopg2-binary`. The
API
is similar, but there are some differences. See the
[psycopg 3 documentation](https://www.psycopg.org/psycopg3/docs/) for details.

## Project Structure

```
.
├── .editorconfig              # Editor configuration
├── .github/                   # GitHub Actions and configuration
│   ├── workflows/            # CI/CD workflows
│   └── auto-assign.yml       # Auto-assign PR reviewers
├── .gitignore                # Git ignore rules
├── .python-version           # Python version for pyenv
├── containers/               # Docker container configurations
│   ├── compose.yaml         # Docker Compose file
│   ├── caddy/               # Caddy web server config
│   └── postgres/            # PostgreSQL initialization scripts
├── src/                      # Django project source
│   ├── manage.py            # Django management script
│   └── project_core/        # Main project package
├── staticfiles/              # Static files directory
├── pyproject.toml           # Project metadata and dependencies
├── uv.lock                  # Locked dependencies (uv)
├── LICENSE                  # MIT License
└── README.md                # This file
```

## Troubleshooting

### Port Already in Use

If you see errors about ports being in use, you can change the default ports
using environment variables:

```shell
export POSTGRES_PORT=5433
export PGADMIN_PORT=8033
export SMTP_PORT=1026
export SMTP_WEB_PORT=8026
export STATIC_PORT=8889
```

### Database Connection Errors

Make sure the PostgreSQL container is running:

```shell
cd containers
docker compose ps
```

If the database service isn't running, start it:

```shell
docker compose up -d database
```

### Permission Issues with Static Files

If you encounter permission issues with the `staticfiles/` directory, ensure
your user has write permissions:

```shell
chmod -R 755 staticfiles/
```

## Additional Resources

* [Django Documentation](https://docs.djangoproject.com/)
* [Django Tutorial](https://docs.djangoproject.com/en/stable/intro/tutorial01/)
* [Python Packaging User Guide](https://packaging.python.org/)
* [Docker Compose Documentation](https://docs.docker.com/compose/)
* [PostgreSQL Documentation](https://www.postgresql.org/docs/)

## Contributing

This is a template repository. If you want to contribute improvements to the
template itself, please submit issues and pull requests to the original
repository.

## License

MIT License - see [LICENSE](LICENSE) file for details.

Copyright (c) 2025 Python training course authors and contributors
