##  README

### What is this repository for?

This is the core repo for the platypus-based methods. 
This repo serves as the main source for core method files: Dockerfile, bitbucket-pipelines.yml, environment.dev.yml, tasks.py, etc.

### Note: this repo tries to model the structure defined here:
https://docs.python-guide.org/writing/structure/

### How do I get set up?

* Installing miniconda:  
  Method here (https://python-poetry.org/docs/#installation)
  
* Installing the environment
  0. Get your JFROG password and username from https://happypackages.jfrog.io/ and set as env variables JFROG_USERNAME and JFROG_PASSWORD.
  1. Add the mims conda channel with your jfrog password and username:  
     `conda config --set custom_channels.mims-conda https://${JFROG_USERNAME}:${JFROG_PASSWORD}@happypackages.jfrog.io/artifactory/api/conda/`   
  2. Install environment:  
     `conda env create`  
  3. Add dev/test dependencies:  
     `conda env update --name platypus-core --file environment.dev.yml`  
     `conda env update --name platypus-core --file environment.docker.yml `
  
* Activating the environment:  
  `conda activate platypus-core`  

### Developer guide
 
* Generating the lock files (make sure to activate the conda env):  
  - run: `conda-lock --strip-auth -f environment.yml -p linux-64 --kind explicit`  
  - then commit the new lock file.

* Creating a new conda env from the lock file:
  `conda create --name platypus-core --file conda-linux-64.lock`
  
* How to run dev tasks: 
  - `inv list` for a list of the available commands
  - Tests: `inv test`  
  - Lint: `inv lint`  
  - Benchmark: `inv benchmark`  
  - Format: `inv format-code`  
  - Lock dependencies: `inv lock-dependencies`
  
* Benchmarks
  - Setup: To assess the relative performance of some functions of interest, do the following for each unit test you'd like to evaluate:
    - Add `@pytest.mark.benchmark` above the test
    - Pass the variable `benchmark` as an argument to your test
    - In the test, encapsulate the function of interest and its arguments inside `benchmark()`
    - For more info, see the documentation: https://pypi.org/project/pytest-benchmark/ 
  - If your repo wouldn't benefit from benchmarking, simply ignore this section and comment out the `inv benchmark` from the `bitbucket-pipelines.yml` to skip it altogether.
  - Compare against a specific benchmark version:  
    - `pytest-benchmark compare 0001 0002`
  - How to create new pytest benchmarks
    - `inv create-new-benchmarks` or `pytest --benchmark-save=platypus-core`
    - Commit the newly created benchmark file. Note new files will increment the version number automatically.

### Merging into another folder
0. Install meld on your machine
1. Make sure to git clone platypus-core locally
2. cd into the desired folder
3. then run: `meld . ../platypus-core/`


### TODO:
- Add parallel steps in bitbucket pipeline
- Investigate using this repo as a git submodule in other repos.
- Check if possible to upload CI artifacts to jfrog for faster build times
- Add common steps for docker build then use with tag argument (instead of duplicating)
- Investigate usage of this repo with [cookiecutter](https://github.com/cookiecutter/cookiecutter)