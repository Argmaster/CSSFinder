# Installation Guide

Make sure you have Python installed. CSSFinder is compatible with Python 3.8 up
to 3.11. Python release files can be found on the official
[Python website](https://www.python.org/downloads/).

!!! tip "Add Python to Path"

    Make sure to  select `Add Python to PATH` during installation of Python interpreter.
    After installation is complete, to check if Python was correctly added to system
    Path, open a new terminal and run following command:

    ```bash
    python --version
    ```

    Output should look similar to this:

    ```bash
    Python 3.X.Y
    ```

    Where `3.X.Y` is the version of Python you have installed.

## Global installation (quick)

=== "Linux"

    To install CSSFinder globally, run following command:

    ```bash
    pip install cssfinder
    ```

    !!! tip

        On some Linux distributions, especially older ones, you may need to use `pip3`
        instead of `pip`.

=== "Windows"

    To install CSSFinder globally, run following command:

    ```powershell
    pip install cssfinder
    ```

## Virtual environment installation (recommended)

=== "Linux"

    To create a new virtual environment, `venv` module must be available for your Python
    interpreter. Some of linux distributions may require to install additional package
    to make this module available.

    After `venv` module is available, create a new virtual environment by running:

    ```bash
    python -m venv cssfinder-env
    ```

    !!! tip

        On some Linux distributions, especially older ones, you may need to use `python3`
        instead of `python`.

    Activate the virtual environment:

    ```bash
    source cssfinder-env/bin/activate
    ```

    Install CSSFinder:

    ```bash
    pip install cssfinder
    ```

=== "Windows"

    To create a new virtual environment, run following command:

    ```powershell
    python -m venv cssfinder-env
    ```

    Activate the virtual environment:

    ```powershell
    .\cssfinder-env\scripts\activate
    ```

    Install CSSFinder:

    ```powershell
    pip install cssfinder
    ```

    !!! warning "PDF export on Windows"

        CSSFinder can export PDF reports (and other formats too), but it uses
        `weasyprint` for that and `weasyprint` relies on `GTK3`. Unfortunately it is
        quite hard to get `GTK3` going on windows and `weasyprint` requires it to work.
        Therefore you must handle installation yourself.
        [Here](https://doc.courtbouillon.org/weasyprint/stable/first_steps.html#windows)
        you can find official guidelines from `weasyprint`.
        [This repository](https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer)
        may also help. Alternatively you can use WSL to install and run CSSFinder, as
        its seamless to do that.

        Its worth mentioning that other formats are not affected by this issue.

With virtual environment approach you will have to activate it every time you
open new terminal and want to use CSSFinder, as packages installed are not
available outside of virtual environment. This approach allows you to avoid
conflicts with other software.

## Backend installation

`cssfinder` package itself does not contain implementations of algorithms.
Those are shipped in packages called backends. Currently `cssfinder` supports
two backend packages: `cssfinder-backend-numpy` and `cssfinder-backend-rust`.
Those can be installed both as extras of `cssfinder` package and as standalone
modules. Both approaches yield the same result.

=== "Linux"

    To install CSSFinder backends, run following commands:

    ```bash
    pip install cssfinder[numpy]
    pip install cssfinder[rust]
    ```

=== "Windows"

    To install CSSFinder backends, run following commands:

    ```powershell
    pip install cssfinder[numpy]
    pip install cssfinder[rust]
    ```

You don't need both `cssfinder[numpy]` and `cssfinder[rust]`, one will be
perfectly fine for most use cases. You can specify backend to use in project
settings. Unfortunately if you want to run task which was configured to use
backend X and you don't have backend X installed, task will fail.

If you are unsure which one to choose, install both. This will spare you from
unexpected failures caused by missing backend.

As an alternative to installing `cssfinder` extras (`cssfinder[numpy]` and
`cssfinder[rust]`) you may install `cssfinder-backend-numpy` and
`cssfinder-backend-rust` packages, which are exactly the same.

Backends are dynamically detected from all locations from where Python can
import modules, thus any valid way of making backend code reachable for
interpreter will work.

### Development version

To install development version of CSSFinder, following command:

```
pip install git+https://github.com/Argmaster/pygerber
```

This will install latest semi-stable version of CSSFinder from GitHub
repository.
