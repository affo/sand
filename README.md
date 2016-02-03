### Install

Install `python-virtualenv`:

```
$ sudo easy_install pip
$ sudo pip install virtualenv
```

Create a virtual environment and install requirements:

```
$ virtualenv venv
$ source sandrc
$ pip install -r requirements.txt # if you want to install both, use requirements-dev.txt
```

### Run tests

```
$ make test
```
### Push charts to Plotly
Before specifying `--push` while using the CLI, follow
the instructions here: https://plot.ly/python/user-guide/#Step-6.
