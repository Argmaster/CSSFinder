# Project Guide

## Introduction

In CSSFinder, computations are described in special `cssfproject.*` files
within dedicated directories. Such directory with all files within it is called
a `project`. Project must contain either `cssfproject.json` or `cssfproject.py`
file which describe list of tasks which can be executed with cssfinder.

`JSON` file is purely declarative, but with special `$ref` substitution
support, while python scripts (`cssfproject.py`) allow for dynamic behaviors.

Tasks are smallest possible unit of work which can be scheduled for execution
by CSSFinder. They can be automatically executed in parallel with automatic
queues to speed up calculations.

## Project file

=== "JSON"

    Example of project based on `cssfproject.json` is shipped with cssfinder and can be
    cloned with:

    ```bash
    cssfinder clone-example 5qubits_json
    ```

    Afterwards you can either open `./5qubits_json/cssfproject.json` file in your favorite
    editor or use following command to print it to the console:

    ```bash
    cssfinder project inspect ./5qubits_json/
    ```

    Here is the output:

    ```json
    {
        "version": "1.0.0",
        "meta": {
            "author": "Krzysztof Wiśniewski; Marcin Wieśniak",
            "email": "argmaster.world@gmail.com",
            "name": "5qubits",
            "description": "Example of project configuration for 'Full separability of an n-quDit state' mode.",
            "version": "1.0.0"
        },
        "tasks": {
            "main": {
                "gilbert": {
                    "mode": "FSnQd",
                    "backend": {
                        "name": "numpy",
                        "precision": "single"
                    },
                    "runtime": {
                        "visibility": 0.4,
                        "max_epochs": 1000,
                        "iters_per_epoch": 2000,
                        "max_corrections": 1000
                    },
                    "state": {
                        "file": "{project.project_directory}/5qubits_in.mtx",
                        "depth": null,
                        "quantity": null
                    },
                    "resources": {
                        "symmetries": null,
                        "projection": null
                    }
                }
            },
            "test_fsnqd_5qubits": {
                "gilbert": {
                    "mode": {
                        "$ref": "#/tasks/main/gilbert/mode"
                    },
                    "backend": {
                        "$ref": "#/tasks/main/gilbert/backend"
                    },
                    "runtime": {
                        "visibility": 0.4,
                        "max_epochs": 10,
                        "iters_per_epoch": 1000,
                        "max_corrections": 100
                    },
                    "state": {
                        "$ref": "#/tasks/main/gilbert/state"
                    },
                    "resources": {
                        "$ref": "#/tasks/main/gilbert/resources"
                    }
                }
            }
        }
    }
    ```

=== "Python"

    Example of project based on `cssfproject.py` is shipped with cssfinder and can be
    cloned with:

    ```bash
    cssfinder clone-example 5qubits_py
    ```

    Afterwards you can either open `./5qubits_json/cssfproject.py` file in your favorite
    editor or use `cat` to display it in console:

    ```bash
    cat ./5qubits_py/cssfproject.py
    ```

    Here is the output:

    ```python
    from __future__ import annotations

    from pathlib import Path

    from pydantic import EmailStr

    from cssfinder.api import run_project
    from cssfinder.cssfproject import (
        AlgoMode,
        BackendCfg,
        CSSFProject,
        GilbertCfg,
        Meta,
        Precision,
        RuntimeCfg,
        SemVerStr,
        State,
        Task,
    )

    TASKS = [
        Task(
            gilbert=GilbertCfg(
                mode=AlgoMode.FSnQd,
                backend=BackendCfg(
                    name="numpy",
                    precision=Precision.SINGLE,
                ),
                state=State(file=path.as_posix()),
                runtime=RuntimeCfg(
                    visibility=0.4,
                    max_epochs=1000,
                    iters_per_epoch=1000,
                    max_corrections=1000,
                ),
            ),
        )
        for path in Path(__file__).parent.glob("*_in.mtx")
    ]

    __project__ = CSSFProject(
        meta=Meta(
            author="Krzysztof Wiśniewski; Marcin Wieśniak",
            email=EmailStr("argmaster.world@gmail.com"),
            name="5qubits",
            description="Example of project configuration for 'Full separability of an "
            "n-quDit state' mode.",
            version=SemVerStr("1.0.0"),
        ),
        tasks=TASKS,
        project_path=__file__,
    )

    if __name__ == "__main__":
        run_project(__project__)
    ```

    CSSFinder can also evaluate Python project file and output equivalent JSON:

    ```bash
    cssfinder project inspect ./5qubits_json/
    ```

    Output should be similar to:

    ```json
    {
        "meta": {
            "author": "Krzysztof Wiśniewski; Marcin Wieśniak",
            "email": "argmaster.world@gmail.com",
            "name": "5qubits",
            "description": "Example of project configuration for 'Full separability of an n-quDit state' mode.",
            "version": "1.0.0"
        },
        "tasks": {
            "0": {
                "gilbert": {
                    "mode": "FSnQd",
                    "backend": {
                        "name": "numpy",
                        "precision": "single"
                    },
                    "state": {
                        "file": "/home/argmaster/dev/repos/cssfinder/guide/5qubits_py/5qubits_in.mtx",
                        "depth": null,
                        "quantity": null
                    },
                    "runtime": {
                        "visibility": 0.4,
                        "max_epochs": 1000,
                        "iters_per_epoch": 1000,
                        "max_corrections": 1000
                    },
                    "resources": {
                        "symmetries": null,
                        "projection": null
                    }
                }
            }
        }
    }
    ```

## Project from scratch

=== "JSON - `cssfproject.json`"

    To create new project from scratch you can use following command:

    ```bash
    cssfinder create-new-json-project --no-interactive
    ```

    This will create new directory `new_project` with `cssfproject.json` file
    inside. You can edit this file with your favorite editor or use `cssfinder`
    commands to add task configuration (described in next section).

    `cssfinder create-new-json-project` command accepts options matching metadata fields
    like `--author`, `--email` etc. Additionally you can omit `--no-interactive` flag
    to be asked for metadata interactively with text user interface.
    For more information about this command use:

    ```bash
    cssfinder create-new-json-project --help
    ```

    Let's inspect the created project:

    === "Linux"

        ```bash
        ls -la ./new_project/
        ```

        Output should be similar to:

        ```log
        total 16
        drwxrwxr-x 2 argmaster argmaster 4096 Apr 16 01:05 .
        drwxrwxr-x 7 argmaster argmaster 4096 Apr 16 00:38 ..
        -rwxrwxr-x 1 argmaster argmaster  215 Apr 16 01:16 cssfproject.json
        ```

    === "Windows"

        ```bash
        ls ./new_project/
        ```

        Output should be similar to:

        ```log
        total 16
        drwxrwxr-x 2 argmaster argmaster 4096 Apr 16 01:05 .
        drwxrwxr-x 7 argmaster argmaster 4096 Apr 16 00:38 ..
        -rwxrwxr-x 1 argmaster argmaster  215 Apr 16 01:16 cssfproject.json
        ```

=== "Python - `cssfproject.py`"

    To create new project from scratch you can use following command:

    ```cmd
    cssfinder create-new-python-project --no-interactive
    ```

    This will create new directory `new_project` with `cssfproject.py` file
    inside. You can edit this file with your favorite editor. CSSFinder does not
    provide a way to edit Python project files as there are barely any rules for how
    those files should be structured.

    `cssfinder create-new-python-project` command accepts options matching metadata fields
    like `--author`, `--email` etc. Additionally you can omit `--no-interactive` flag
    to be asked for metadata interactively with text user interface.
    For more information about this command use:

    ```bash
    cssfinder create-new-python-project --help
    ```

    Let's inspect the created project:

    === "Linux"

        ```bash
        ls -la ./new_project/
        ```

        Output should be similar to:

        ```log
        total 16
        drwxrwxr-x 2 argmaster argmaster 4096 Apr 16 01:05 .
        drwxrwxr-x 7 argmaster argmaster 4096 Apr 16 00:38 ..
        -rwxrwxr-x 1 argmaster argmaster  215 Apr 16 01:16 cssfproject.py
        ```

    === "Windows"

        ```bash
        ls ./new_project/
        ```

        Output should be similar to:

        ```log
        total 16
        drwxrwxr-x 2 argmaster argmaster 4096 Apr 16 01:05 .
        drwxrwxr-x 7 argmaster argmaster 4096 Apr 16 00:38 ..
        -rwxrwxr-x 1 argmaster argmaster  215 Apr 16 01:16 cssfproject.py
        ```

!!! warning "Project file precedence"

    If both `cssfproject.json` and `cssfproject.py` files are present in the same
    directory, `cssfproject.json` will be used and `cssfproject.py` will be ignored.
    There is no particular reason to prefer one over the other, but some loading order
    must be established, so `cssfproject.json` was chosen to be first.

## Adding tasks (JSON only)

!!! warning

    This section is a continuation to the previous one. If you haven't created a
    project yet, please refer to the previous section.

    Current working directory should contain `new_project` project directory.

!!! warning

    This section is only applicable to `cssfproject.json` projects.

Main purpose of a project is to be a container for "tasks". Each task is just a
dictionary containing configuration for CSSFinder, describing what to do, with
what algorithm, what data to use and possibly some additional parameters
describing how PC resources should be used. They can be added either manually,
by editing `cssfproject.json` file, or by using `cssfinder` commands.

We will continue with task utilizing Gilbert algorithm, as it is currently only
one implemented. To run this algorithm we need to provide a state matrix in
form of a file.

To create `state.mtx` file you can use following command:

=== "Linux"

    ```bash
    echo '"%%MatrixMarket matrix array real symmetric
    %Created with the Wolfram Language : www.wolfram.com
    8 8
    2.5000000000000000E-01
    0.0000000000000000E+00
    0.0000000000000000E+00
    -2.5000000000000000E-01
    0.0000000000000000E+00
    -2.5000000000000000E-01
    -2.5000000000000000E-01
    0.0000000000000000E+00
    0.0000000000000000E+00
    0.0000000000000000E+00
    0.0000000000000000E+00
    0.0000000000000000E+00
    0.0000000000000000E+00
    0.0000000000000000E+00
    0.0000000000000000E+00
    0.0000000000000000E+00
    0.0000000000000000E+00
    0.0000000000000000E+00
    0.0000000000000000E+00
    0.0000000000000000E+00
    0.0000000000000000E+00
    2.5000000000000000E-01
    0.0000000000000000E+00
    2.5000000000000000E-01
    2.5000000000000000E-01
    0.0000000000000000E+00
    0.0000000000000000E+00
    0.0000000000000000E+00
    0.0000000000000000E+00
    0.0000000000000000E+00
    2.5000000000000000E-01
    2.5000000000000000E-01
    0.0000000000000000E+00
    2.5000000000000000E-01
    0.0000000000000000E+00
    0.0000000000000000E+00
    ' > ./new_project/state.mtx
    ```

=== "Windows"

    ```powershell
    echo '%%MatrixMarket matrix array real symmetric
    %Created with the Wolfram Language : www.wolfram.com
    8 8
    2.5000000000000000E-01
    0.0000000000000000E+00
    0.0000000000000000E+00
    -2.5000000000000000E-01
    0.0000000000000000E+00
    -2.5000000000000000E-01
    -2.5000000000000000E-01
    0.0000000000000000E+00
    0.0000000000000000E+00
    0.0000000000000000E+00
    0.0000000000000000E+00
    0.0000000000000000E+00
    0.0000000000000000E+00
    0.0000000000000000E+00
    0.0000000000000000E+00
    0.0000000000000000E+00
    0.0000000000000000E+00
    0.0000000000000000E+00
    0.0000000000000000E+00
    0.0000000000000000E+00
    0.0000000000000000E+00
    2.5000000000000000E-01
    0.0000000000000000E+00
    2.5000000000000000E-01
    2.5000000000000000E-01
    0.0000000000000000E+00
    0.0000000000000000E+00
    0.0000000000000000E+00
    0.0000000000000000E+00
    0.0000000000000000E+00
    2.5000000000000000E-01
    2.5000000000000000E-01
    0.0000000000000000E+00
    2.5000000000000000E-01
    0.0000000000000000E+00
    0.0000000000000000E+00
    ' > ./new_project/state.mtx
    ```

Although you can also copy-paste the matrix into a file with any text editor.

After creating matrix file, we can add task to the project. Following command
should do exactly that:

```bash
cssfinder project add-gilbert-task ./new_project/ --no-interactive --state "{project.project_directory}/state.mtx"
```

Now we can check if task was correctly added by using following command:

```bash
cssfinder project list-tasks -l ./new_project/
```

Here is the output:

```log
task_0 mode=FSnQd backend=numpy_jit
```

Now we can run this task to make sure it works:

```bash
cssfinder project run-tasks ./new_project/ -m task_0
```

Here is the expected output:

```log
╭──────────────────────╮
│ Task task_0 started. │
╰──────────────────────╯
╭───────────────────────╮
│ Task task_0 finished. │
╰───────────────────────╯
```

Now you can utilize the output data to, for example, create HTML report. See
[Quick Start Guide - Report Generation](https://argmaster.github.io/CSSFinder/latest/usage/01_quick_start.html#report-generation)
for more information.

## JSON to Python conversion

CSSFinder can convert JSON project file to Python project file. To do this use:

```bash
cssfinder project to-python ./new_project/
```

If project is already a Python project using this command will fail. Because of
loading order, if project contains both `cssfproject.json` and
`cssfproject.py`, `cssfproject.json` will be loaded first and `cssfproject.py`
will be ignored. Therefore project containing both is not considered a Python
project and won't trigger
`'JSON_PROJECT_PATH': Provided path is not a valid JSON project path.` error.
However, it will complain about `cssfproject.py` being present in the
directory.
