# droppy-workspace

![python](https://img.shields.io/badge/python-2.7%2C%203.6-brightgreen.svg)
![tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)
![license](https://img.shields.io/badge/license-MIT-blue.svg)
![platform](https://img.shields.io/badge/platform-macos-lightgrey.svg)

All the _Workflows_, _Tasks_ and _Images_ that come with the **DropPy** macOS app.

## Product page

[https://droppy.eberl.se](https://droppy.eberl.se) (currently offline)

## Requirements via Pipenv

There is no `requirements.txt` included here, although some of the _Tasks_ require non-standard packagres to be present.

Instead [Pipenv](https://pipenv.readthedocs.io/en/latest/) is used: Pipenv uses `Pipfile` and `Pipfile.lock` to separate abstract dependency declarations from the last tested combination. And it creates a virtual environment per project, to not mess up the Python configuration on your system.

### Install pipenv

```bash
# Check environment
$ python3 --version
> Python 3.7.3

$ pip3 --version
> pip 19.0.3 from /usr/local/lib/python3.7/site-packages/pip (python 3.7)

# Install pipenv (via Homebrew)
$ brew update
$ brew install pipenv
```

### Install requirements

```bash
# Install requirements as defined in the Pipfile/Pipfile.lock files in the project root dir
cd droppy-workspace
pipenv install

# The output shows that pipenv created a virtual environment for example at ...
# /Users/guenther/.local/share/virtualenvs/droppy-workspace-G-iHlOv2
# Take note of that path for the next step
```

### Setup DropPy

In **DropPy** this new virtual environment has to be set up in _Preferences_ - _Interpreter_:

- Click "Add" Button
- Executable `/Users/guenther/.local/share/virtualenvs/droppy-workspace-G-iHlOv2/bin/python` (or whatever your output was)
- Arguments `-B`
- Name `Python 3.7 Pipenv`

### Setup Workflows

All _Workflows_ that should be interpreted through this virtual environment need the property `"interpreterName": "Python 3.7 Pipenv"`.

As for example is already set in `Workflows/image_rotate_by_90deg.json`. And all other _Workflows_ that won't run otherwise.

### Add more packages

This adds `some-other-package` to the Pipenv managed virtualenv for this project.

```bash
cd droppy-workspace
pipenv install some-other-package
```

## Tests

For simplicity the version of _droppy-workspace_ that is bundled inside **DropPy** does not contain the tests themselves (`test_task.py` files in _Task_ sub-directories) and the sample files needed by the tests (directory `Test`).

If you are interested in the tests check out this repository, extract it, and adjust _Preferences_ - _Workspace_ - _Workspace directory_ in **DropPy** accordingly.

### Setup

Make sure the _pytest_ package is installed for the Python interpreter you want to test with:

```bash
$ python -m pytest --version
> This is pytest version 3.2.3, imported from /Library/Python/2.7/site-packages/pytest.pyc

$ python3 -m pytest --version
> This is pytest version 3.2.3, imported from /Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages/pytest.py
```

Install it if it is not:

```bash
$ pip install pytest
$ pip3 install pytest
```

### Running

Change into the directory of the _Task_ you want to test:

```bash
$ cd droppy-workspace/Tasks/Filter.OnlyDirectories
```

Execute _pytest_ using the interpreter of your choice here:

```bash
$ python -B -m pytest -v
$ python3 -B -m pytest -v
```

Running _pytest_ over the complete `Tasks` directory at once is not possible because for **DropPy** all modules need to have the same filename `task.py`.
This is a structure _pytest_ doesn't get along with. The tests need to be run for each _Task_ separately.

To automate this two scripts are provided:

```bash
$ cd droppy-workspace/Test
$ . run_all_py27.sh
$ . run_all_py36.sh
```

### Resources

- [pytest](https://docs.pytest.org/en/latest/)
- [py.path](http://py.readthedocs.io/en/latest/path.html)
- [Collection of sample files](http://techslides.com/sample-files-for-development)
