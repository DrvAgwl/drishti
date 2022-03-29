#!/bin/bash

hostname=$1

DIR=/opt/udaan/drishti/
rsync -avz --omit-dir-times ./src ./bin ./conf requirements.txt .env pi@"$hostname":${DIR} ;
ssh pi@$hostname "sudo pip3 install -r $DIR/src/requirements.txt"
