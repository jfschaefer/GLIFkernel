GLIF Kernel
===========

This repository contains the code for a re-implementation of the [GLIF kernel](https://github.com/kwarc/glif) for Jupyter.

## Online Demo
You can try out GLIF online at
[https://mybinder.org/v2/gh/jfschaefer/GlifBinder/version2](https://mybinder.org/v2/gh/jfschaefer/GlifBinder/version2).


## What is GLIF?
TODO


## Running the Kernel Locally with Docker
If you have [docker](https://www.docker.com/) installed,
you should be able to simply run
```shell
docker run -p 8888:8888 jfschaefer/glif:2.1.0
```
Note that running the command again will create a new container,
i.e. your changes won't persist.
However, you can "link" (mount) a folder of your file system
into the container, which will allow you to keep files stored there:
```shell
docker run -v "/path/to/my/folder:/home/worker/glifkernel/notebooks/persistent" -p 8888:8888 jfschaefer/glif:2.1.0
```
`/path/to/my/folder` should be a folder on your local file system.
It will be synchronized with the `persistent` folder.

## Installing the Kernel locally
The local installation is a bit tricky as GLIF combines multiple systems, all of which have to be installed.
It is therefore not recommended for casual users.
However, a local installation has certain advantages:
* You can develop components in specialized IDEs (e.g. for MMT) rather than in the notebooks,
    which is particularly useful for larger projects
* You can work with your own build of GF/MMT/ELPI
* You can develop demos with custom code using the [GLIF python package](https://github.com/jfschaefer/glifcore)

### Prerequisites
* A recent Python version (at least 3.9, you can check with `python3 --version`)
* git (currently required for the installation with pip from Github)
**Optional:**
* [GF](https://www.grammaticalframework.org/), [MMT](https://uniformal.github.io/) and [ELPI](https://github.com/lpcic/elpi), which GLIF is based on.
    Note that you only need to install the frameworks you actually want to use (i.e. you can e.g. not install ELPI if you don't plan to use it).
    To help GLIF find MMT, you should set the `MMT_JAR` environment variable to the installation destination (`export MMT_JAR=/path/to/mmt.jar` on unix).
* [Graphviz](https://www.graphviz.org/), specifically `dot`, if you want to  visualize ASTs.


### Actual Installation
```shell
python3 -m pip install git+https://github.com/jfschaefer/glifcore.git#egg=glif
python3 -m pip install git+https://github.com/jfschaefer/GLIFkernel.git#egg=glif_kernel
python3 -m glif_kernel.install
```

### Running the Kernel
Simply start Jupyter with
```
python3 -m jupyter notebook
```
and open an existing notebook or make a new one with the kernel *GLIF*.
