# nvmconverter
Converts the VisualSFM .nvm (N-View Match) filetype to the OpenSFM .json (JavaScript Object Notation) file type. The NVM file type is discribed here: [vsfm nvm](http://ccwu.me/vsfm/doc.html#nvm)

# OpenSfM
There is a Docker image of OpenSfM available by searching 
`docker search awkbr549/opensfm'

To run the image, it is advised to run with the following options:
`-it'		--> used with the `run' command, creates an interactive and pseudo-tty connection to the container
`-ai'		--> used with the `start' command to allow interaction with an already existing Docker container
`-p 8000:8000'		--> maps Docker container port 8000 to localhost 8000
`-v dir/on/local/computer:dir/on/container' 	--> maps local files to the container

On Windows, Docker's option to map local files to the container doesn't work (at least for me). In order to get around this, you can just use the `scp' file transfer command to move files from your local machine to a server, then also in your Docker container use `scp' to transfer files from the server to the container. Though cumbersome, this is the only workaround I've found.

Example command:
`docker run -it -p 8000:8000 awkbr549/opensfm:v2' //for new containers (!!! should only run once)
`docker start -ai <container_id>' //for existing containers

# convert.py
To run the conversion program, do
`./convert.py'

You will be prompted for an input file and an output file. Currently, the only supported conversion is NVM to JSON. In order to do this, an extra file is needed from OpenSfM since NVM doesn't gather camera data but JSON does. In order to get this extra file, you will need to modify your OpenSfM/bin/run_all file. It should normally read:

#!/usr/bin/env bash

set -e

DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

$DIR/opensfm extract_metadata $1
$DIR/opensfm detect_features $1
$DIR/opensfm match_features $1
$DIR/opensfm create_tracks $1
$DIR/opensfm reconstruct $1
$DIR/opensfm mesh $1


Change this file to contain only the following:

#!/usr/bin/env bash

set -e

DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

$DIR/opensfm extract_metadata $1

After this, run OpenSfM on the desired data to get a file called 'camera_models.json'. Transfer this new file to where you are going to run the conversion program.