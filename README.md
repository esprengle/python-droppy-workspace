# droppy-workspace

![python](https://img.shields.io/badge/python-2.7%2C%203.6-brightgreen.svg)
![tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)
![license](https://img.shields.io/badge/license-MIT-blue.svg)
![platform](https://img.shields.io/badge/platform-macos-lightgrey.svg)

All the *Workflows*, *Tasks* and *Images* that come with the **DropPy** macOS app.

## Product page

[https://droppyapp.com](https://droppyapp.com)

## Tests

For simplicity the version of *droppy-workspace* that is bundled inside **DropPy** does not contain the tests themselves (`test_task.py` files in *Task* sub-directories) and the sample files needed by the tests (directory `Test`).

If you are interested in the tests check out this repository, extract it, and adjust *Preferences* - *Workspace* - *Workspace directory* in **DropPy** accordingly.

### Setup

Make sure the *pytest* package is installed for the Python interpreter you want to test with:

    python -m pytest --version
    > This is pytest version 3.2.3, imported from /Library/Python/2.7/site-packages/pytest.pyc
     
    python3 -m pytest --version
    > This is pytest version 3.2.3, imported from /Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages/pytest.py

Install it if it is not:

    pip install pytest
     
    pip3 install pytest

### Running

Change into the directory of the *Task* you want to test:

    cd ~/Development/droppy-workspace/Tasks/Filter.OnlyDirectories

Execute *pytest* using the interpreter of your choice here:

    python -B -m pytest -v
     
    python3 -B -m pytest -v

Running *pytest* over the complete `Tasks` directory at once is not possible because for **DropPy** all modules need to have the same filename `task.py`.
This is a structure *pytest* doesn't get along with. The tests need to be run for each *Task* separately.

To automate this two scripts are provided:

    cd ~/Development/droppy-workspace/Test
     
    . run_all_py27.sh
     
    . run_all_py36.sh

### Resources

- [pytest](https://docs.pytest.org/en/latest/)
- [py.path](http://py.readthedocs.io/en/latest/path.html)
- [Collection of sample files](http://techslides.com/sample-files-for-development)
