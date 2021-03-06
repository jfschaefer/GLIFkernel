GLIF Kernel
===========

This repository contains the code for a re-implementation of the [GLIF kernel](https://github.com/kwarc/glif) for Jupyter.

## Online Demo
TODO

## What is GLIF?
TODO

## Running the Kernel Locally with Docker
TODO

## Installing the Kernel
Installing the kernel directly on your machine has several advantages and is recommended
for serious users.
Some of the reasons are:
* You can develop components in specialized IDEs (e.g. for MMT) rather than in the notebooks,
    which is particularly useful for larger projects
* You can work with your own build of GF/MMT/ELPI
* You can develop demos with custom code [GLIF python package](https://github.com/jfschaefer/glif)

### Prerequisites
* A recent Python version (at least 3.7, you can check with `python3 --version`)
* git (currently required for the installation with pip from Github)
**Optional:**
* [GF](https://www.grammaticalframework.org/), [MMT](https://uniformal.github.io/) and [ELPI](https://github.com/lpcic/elpi), which GLIF is based on.
    Note that you only need to install the frameworks you actually want to use (i.e. you can e.g. not install ELPI if you don't plan to use it).
    To help GLIF find MMT, you should set the `MMT_JAR` environment variable to the installation destination (`export MMT_JAR=/path/to/mmt.jar` on unix).
* [Graphviz](https://www.graphviz.org/), specifically `dot`, if you want to  visualize ASTs.


### Actual Installation
```
python3 -m pip install git+https://github.com/jfschaefer/GLIFkernel.git#egg=glif_kernel
python3 -m glif_kernel.install
```

### Running the Kernel
Simply start Jupyter with
```
python3 -m jupyter notebook
```
and open an existing notebook or make a new one with the kernel *GLIF*.

TODO: Jupyter lab
