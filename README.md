# **Ray Serve Model Multiplexing**

This repository illustrates about the end-to-end deployment of Ray Serve application that uses the model multiplexing API to serve model with different weights and has same input size. Serving the same varities of models with differentiated weights can be tedious and resource intensive. Ray uses LRU (Least Recently Used) approach that unloads the least recently model. It provides the feature of holding certain number of models within a single replica which reduces the loading time as it be cached in each replicas.


## Runtime configration

Python 3.9.0

Pip 24.2

Ray 2.34.0

## Folder structure

.                                   # Project Root Directory
├── README.md                       # Readme.md file
├── app                             # Directory contains Ray serve application python scripts
│   ├── model_multiplex_app.py      # Model multiplexer python script
│   └── test_app.py                 # A normal ray serve python script
├── format_yaml.py                  # A helper python script used to format yaml files
├── manifests                       # contains yaml manifest file
│   └── app-deploy-config.yaml      # Deployment configuration for the serve applications
│   └── app-build-config.yaml       # Build configuration created for the serve applications
├── release_notes.md                # Github release notes
├── requirements.txt                # Python dependencies for the ray serve deployments 
└── scripts                 
    └── check_build_files.sh        # shell script used in generating serve build configuration file

# Local setup

* Create a python virtual or conda environment with the above specified python, pip and Ray version.
* Ensure ray is started and running on your local system using the command `ray start --head`. Once started you can see the ray dasboard that is running on the port 8265.
* The 2.34.0 of Ray needs the Ray serve to be started manually everytime using the CLI command `serve start` where this will creates serve proxy and controller actors that helps in running the serve application on localhost. This command has to be executed multiple times as this will fail to start initially on it's first run. Check the ray dashboard to see whether the proxy and controller are running.
* Now run the serve application using the command `serve run -d app/ model_multiplex_app.app`
* The serve application will be running in port **8000** by default and by providing necessary flags it can run seamlessly and monitored within the Ray Dashboard.

# Build and Deploy

* Once the serve application successfully runs in the localhost , the build configuration has to be generated such that it can be used to deploy and serve the application.
* use the serve build command `serve build -d app/ model_multiplex.app -o manifests/app-build-config.yaml`
* Upon running this command it genertes the build configuration yaml file inside the manifests directory.
* This yaml will be used for deploying the Ray serve application.