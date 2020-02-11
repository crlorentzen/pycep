# Welcome to pycep Documentation!

## CEP Unit Testing

### CEP 2000
-   Unit testing for "Learning Objectives:" with 3 list items to follow using regex.
-   Regex runs against markdown format generated from a package export

### CEP 2006
-   Unit testing for "Toolkit:" with 1 list items to follow using regex.
-   Regex runs against markdown format generated from a package export

### CEP 2007
-   Unit testing for image contained in a module.
-   Regex runs against string format generated from a package content dict value


## Docker Usage

### Docker build instructions

    git clone https://github.com/simspace/pycep/
    cd pycep
    docker build . -t pycep 

#### pycep Docker image size 

    REPOSITORY   TAG     IMAGE ID       CREATED         SIZE
    pycep        latest  f1c8852bff90   2 minutes ago   107MB


### Run basic command with Docker 

    docker run -v /home/ubuntu/Desktop/:/opt/pycep/ pycep -f ExamplePackage.tar.gz -p linter