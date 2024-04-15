# Code quality

To ensure that all code follow same style guidelines and code quality rules,
multiple static analysis tools are used. For simplicity, all of them are
configured as `pre-commit` ([learn about pre-commit](https://pre-commit.com/))
hooks. Most of them however are listed as development dependencies.

- `autocopyright`: This hook automatically adds copyright headers to files. It
  is used to ensure that all files in the repository have a consistent
  copyright notice.

- `autoflake`: This hook automatically removes unused imports from Python code.
  It is used to help keep code clean and maintainable by removing unnecessary
  code.

- `docformatter`: This hook automatically formats docstrings in Python code. It
  is used to ensure that docstrings are consistent and easy to read.

- `prettier`: This hook automatically formats code in a variety of languages,
  including JavaScript, HTML, CSS, and Markdown. It is used to ensure that code
  is consistently formatted and easy to read.

- `isort`: This hook automatically sorts Python imports. It is used to ensure
  that imports are organized in a consistent and readable way.

- `black`: This hook automatically formats Python code. It is used to ensure
  that code is consistently formatted and easy to read.

- `check-merge-conflict`: This hook checks for merge conflicts. It is used to
  ensure that code changes do not conflict with other changes in the
  repository.

- `check-case-conflict`: This hook checks for case conflicts in file names. It
  is used to ensure that file names are consistent and do not cause issues on
  case-sensitive file systems.

- `trailing-whitespace`: This hook checks for trailing whitespace in files. It
  is used to ensure that files do not contain unnecessary whitespace.

- `end-of-file-fixer`: This hook adds a newline to the end of files if one is
  missing. It is used to ensure that files end with a newline character.

- `debug-statements`: This hook checks for the presence of debugging statements
  (e.g., print statements) in code. It is used to ensure that code changes do
  not contain unnecessary debugging code.

- `check-added-large-files`: This hook checks for large files that have been
  added to the repository. It is used to ensure that large files are not
  accidentally committed to the repository.

- `check-toml`: This hook checks for syntax errors in TOML files. It is used to
  ensure that TOML files are well-formed.

- `mixed-line-ending`: This hook checks for mixed line endings (e.g., a mix of
  Windows and Unix line endings) in text files. It is used to ensure that text
  files have consistent line endings.

To run all checks, you must install hooks first with poe

```
poe install-hooks
```

After you have once used this command, you wont have to use it in this
environment. Then you can use

```
poe run-hooks
```

To run checks and automatic fixing. Not all issues can be automatically fixed,
some of them will require your intervention.

Successful hooks run should leave no Failed tasks:

![run_hooks_output](https://user-images.githubusercontent.com/56170852/223247968-8333e9ee-c0f0-4cce-afe1-a8e7917d9b0a.png)

Example of failed task:

![failed_task](https://user-images.githubusercontent.com/56170852/223249222-113a1269-fb3c-4d2c-b2ba-3d26e8ac090a.png)

Those hooks will be run also while you try to commit anything. If any tasks
fails, no commit will be created, instead you will be expected to fix errors
and add stage fixes. Then you may retry running `git commit`.
