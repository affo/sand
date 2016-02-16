# README for `sand` Project
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

Before specifying `--plot` while using the CLI, follow
the instructions here: https://plot.ly/python/user-guide/#Step-6.


# README for `page_rank` Project

Every line of code listed below supposes that you `cd page_rank`.

### Install

Install `python-virtualenv`:

```
$ sudo easy_install pip
$ sudo pip install virtualenv
```

Create a virtual environment and install requirements:

```
$ virtualenv venv
$ source pagerankrc
$ pip install -r requirements.txt
```

Install [maven](https://maven.apache.org/install.html) and
[docker](https://docs.docker.com/engine/installation/) and run `make it_build`
to install the requirements for the iterative version of PageRank.

### The Makefile
You can:

* Generate the dataset from _re.public@polimi_: `make dataset`
* Launch the stochastic PageRank: `make stochastic`
* Launch the iterative PageRank: `make iterative`
