# Quick Start Guide

!!! tip "`cssfinder` installation"

    This guide will help you get started with the `cssfinder` library. Before you
    begin, make sure you have `cssfinder` installed. If you haven't installed it
    yet, you can do so by following the instructions on the
    [official website](https://github.com/Argmaster/cssfinder#installation).

## Example #1

!!! warning "Prerequisites"

    This example relies on `cssfinder_backend_numpy`, please install it before continuing,
    to avoid problems with running the example.

=== "Linux - bash"

    ```bash
    pip install cssfinder[numpy]
    ```

=== "Windows - powershell"

    ```powershell
    cssfinder examples list
    ```

### Clone project

CSSFinder comes with a set of examples which can be used to get familiar with
the library. To list all available examples, use following command:

=== "Linux - bash"

    ```bash
    cssfinder examples list
    ```

=== "Windows - powershell"

    ```powershell
    cssfinder examples list
    ```

Output should look similar to this:

![image](https://github.com/Argmaster/CSSFinder/assets/56170852/4c7fee71-8dae-4808-8e89-f10f45ed5363)

We will use `5qubits_json` example in this tutorial. To clone this example to
current working directory, use following command:

=== "Linux - bash"

    ```bash
    cssfinder clone-example 5qubits_json
    ```

=== "Windows - powershell"

    ```powershell
    cssfinder clone-example 5qubits_json
    ```

Command output on Linux should look similar to this:

```log
Found example 'e5qubits_json', 'Krzysztof Wiśniewski; Marcin Wieśniak', 'c317ef12'
Cloned example to '/home/argmaster/dev/repos/cssfinder'
```

As result, you should find that `5qubits_json` directory have been created in
your current working directory. This directory contains project configuration
files which describe tasks to execute. Configuration also specifies how tasks
should be run.

Let's check it by listing content of `5qubits_json` directory:

=== "Linux - bash"

    ```bash
    ls -la
    ```

    Ouput should look similar to this:

    ```log
    total 16
    drwxrwxr-x  4 argmaster argmaster 4096 Apr 15 20:47 .
    drwxrwxr-x 14 argmaster argmaster 4096 Apr 15 20:47 ..
    drwxrwxr-x  2 argmaster argmaster 4096 Apr 15 20:47 5qubits_json
    drwxrwxr-x  2 argmaster argmaster 4096 Apr 15 20:47 log
    ```

=== "Windows - powershell"

    ```powershell
    ls
    ```

    Ouput should look similar to this:

    ```log
    total 16
    drwxrwxr-x  4 argmaster argmaster 4096 Apr 15 20:47 .
    drwxrwxr-x 14 argmaster argmaster 4096 Apr 15 20:47 ..
    drwxrwxr-x  2 argmaster argmaster 4096 Apr 15 20:47 5qubits_json
    drwxrwxr-x  2 argmaster argmaster 4096 Apr 15 20:47 log
    ```

### Inspect project

To check contents of the you can use following command:

=== "Linux - bash"

    ```bash
    cssfinder project list-tasks -l ./5qubits_json/
    ```

=== "Windows - powershell"

    ```bash
    cssfinder project list-tasks -l ./5qubits_json/
    ```

Output should look similar to this:

```log
main mode=FSnQd backend=numpy
test_fsnqd_5qubits mode=FSnQd backend=numpy
```

Output shows that there are two tasks defined within the project. You can get
more information about tasks using following command:

=== "Linux - bash"

    ```bash
    cssfinder project inspect-tasks ./5qubits_json/ main
    ```

=== "Windows - powershell"

    ```bash
    cssfinder project inspect-tasks ./5qubits_json/ main
    ```

Output should look similar to this:

```json
{
  "main": {
    "gilbert": {
      "mode": "FSnQd",
      "backend": {
        "name": "numpy",
        "precision": "single"
      },
      "state": {
        "file": "/home/argmaster/dev/repos/cssfinder/guide/5qubits_json/5qubits_in.mtx",
        "depth": null,
        "quantity": null
      },
      "runtime": {
        "visibility": 0.4,
        "max_epochs": 1000,
        "iters_per_epoch": 2000,
        "max_corrections": 1000
      },
      "resources": {
        "symmetries": null,
        "projection": null
      }
    }
  }
}
```

`"main"` is a task utilizing gilbert algorithm. It uses `numpy` backend with
`single` precision floating point numbers (32-bit). Path to matrix file is
expands to
`"/home/argmaster/dev/repos/cssfinder/guide/5qubits_json/5qubits_in.mtx"` on PC
of the author of this tutorial. You should see path to `5qubits_in.mtx` file in
your output too, likely preceded by different path.

### Run tasks

Now we can proceed with running tasks defined within the project. That can be
achieved with following command:

=== "Linux - bash"

    ```bash
    cssfinder project run-tasks ./5qubits_json/ -m main
    ```

=== "Windows - powershell"

    ```bash
    cssfinder project run-tasks ./5qubits_json/ -m main
    ```

This command will run task called `"main"`, which may take something in between
of few seconds and few minutes, depending on your hardware. On AMD Ryzen 9
7950X it takes approximately 30 seconds.

After the task is finished, we can check it output directory was created:

=== "Linux - bash"

    ```bash
    ls -la ./5qubits_json/
    ```

    As you can see `output` directory was indeed created:

    ```
    total 20
    drwxrwxr-x 3 argmaster argmaster 4096 Apr 15 22:20 .
    drwxrwxr-x 4 argmaster argmaster 4096 Apr 15 20:47 ..
    -rw-rw-r-- 1 argmaster argmaster 1192 Apr 15 20:47 5qubits_in.mtx
    -rw-rw-r-- 1 argmaster argmaster 1819 Apr 15 20:47 cssfproject.json
    drwxrwxr-x 3 argmaster argmaster 4096 Apr 15 22:20 output
    ```

=== "Windows - powershell"

    ```bash
    ls ./5qubits_json/
    ```

    As you can see `output` directory was indeed created:

    ```
    total 20
    drwxrwxr-x 3 argmaster argmaster 4096 Apr 15 22:20 .
    drwxrwxr-x 4 argmaster argmaster 4096 Apr 15 20:47 ..
    -rw-rw-r-- 1 argmaster argmaster 1192 Apr 15 20:47 5qubits_in.mtx
    -rw-rw-r-- 1 argmaster argmaster 1819 Apr 15 20:47 cssfproject.json
    drwxrwxr-x 3 argmaster argmaster 4096 Apr 15 22:20 output
    ```

Now we can check contents of the `output` directory:

=== "Linux - bash"

    ```bash
    ls -la ./5qubits_json/output/
    ```

    Within `output` directory you should find `main` directory (name will match
    name of the task):

    ```log
    total 12
    drwxrwxr-x 3 argmaster argmaster 4096 Apr 15 22:20 .
    drwxrwxr-x 3 argmaster argmaster 4096 Apr 15 22:20 ..
    drwxrwxr-x 2 argmaster argmaster 4096 Apr 15 22:20 main
    ```

=== "Windows - powershell"

    ```bash
    ls ./5qubits_json/output/
    ```

    Within `output` directory you should find `main` directory (name will match
    name of the task):

    ```log
    total 12
    drwxrwxr-x 3 argmaster argmaster 4096 Apr 15 22:20 .
    drwxrwxr-x 3 argmaster argmaster 4096 Apr 15 22:20 ..
    drwxrwxr-x 2 argmaster argmaster 4096 Apr 15 22:20 main
    ```

Let's now inspect contents of the `main` directory:

=== "Linux - bash"

    ```bash
    ls -la ./5qubits_json/output/main
    ```

    Within `main` directory you should find `corrections.json` file and `state.mtx`
    files.

    ```log
    total 92
    drwxrwxr-x 2 argmaster argmaster  4096 Apr 15 22:20 .
    drwxrwxr-x 3 argmaster argmaster  4096 Apr 15 22:20 ..
    -rw-rw-r-- 1 argmaster argmaster 34334 Apr 15 22:21 corrections.json
    -rwxrwxr-x 1 argmaster argmaster 48176 Apr 15 22:21 state.mtx
    ```

=== "Windows - powershell"

    ```bash
    ls ./5qubits_json/output/main
    ```

    Within `main` directory you should find `corrections.json` file and `state.mtx`
    files.

    ```log
    total 92
    drwxrwxr-x 2 argmaster argmaster  4096 Apr 15 22:20 .
    drwxrwxr-x 3 argmaster argmaster  4096 Apr 15 22:20 ..
    -rw-rw-r-- 1 argmaster argmaster 34334 Apr 15 22:21 corrections.json
    -rwxrwxr-x 1 argmaster argmaster 48176 Apr 15 22:21 state.mtx
    ```

Unfortunately contents of `corrections.json` and `state.mtx` files are too
large to be included in this tutorial.

Now depending on you needs you can proceed with interpretation of those files
with use of different software or use CSSFinder to generate report for you.

## Report generation

!!! warning "Continuation to Example #1"

    This section will be natural continuation to `Example #1` section and will
    assume that reader have successfully followed instructions from there.

CSSFinder provides a way to generate summary reports showing results of tasks
which were run. Those reports can be generated in HTML, PDF and JSON formats.
HTML and PDF are primarily intended for human consumption, while JSON is more
suitable for machine processing.

=== "Linux - bash"

    To generate report in PDF format and automatically open it, use following command:

    ```bash
    cssfinder project create-task-report ./5qubits_json/ task_0 --pdf --open
    ```

    After running this command, you should see report in your default PDF viewer.

=== "Windows - powershell"

    To generate report in HTML format and automatically open it, use following command:

    ```bash
    cssfinder project create-task-report ./5qubits_json/ task_0 --html --open
    ```

    !!! warning "PDF reports on Windows"

        Getting PDF reports to work on Windows can be troublesome. Please check out
        [Installation Guide](https://argmaster.github.io/CSSFinder/latest/usage/00_installation_guide.html)
        Windows installation for more information.

    After running this command, you should see report in your default HTML viewer.

Example report looks like this:

![image](https://github.com/Argmaster/CSSFinder/assets/56170852/5984b903-241a-447e-b9bf-8772ca3d2f02)
![image](https://github.com/Argmaster/CSSFinder/assets/56170852/b84dc7f1-271b-4272-a048-93970edff1f1)
