# Setup

This project uses `Python` programming language and requires at least python
`3.8` for development and distribution. Development dependencies
[`poetry`](https://pypi.org/project/poetry/) for managing dependencies and
distribution building. It is necessary to perform any operations in development
environment.

To install poetry globally (preferred way) use `pip` in terminal:

```
pip install poetry
```

Then use

```
poetry shell
```

to spawn new shell with virtual environment activated. Virtual environment will
be indicated by terminal prompt prefix `(cssfinder-py3.10)`, version indicated
in prefix depends on used version of Python interpreter. It is not necessary to
use Python 3.10, however at least 3.8 is required.

Within shell with active virtual environment use:

```
poetry install --sync
```

To install all dependencies. Every time you perform a `git pull` or change a
branch, you should call this command to make sure you have the correct versions
of dependencies.

Last line should contain something like:

```
Installing the current project: cssfinder (0.1.0)
```

If no error messages are shown, You are good to go.
