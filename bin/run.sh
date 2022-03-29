#!/bin/bash

test=$1

export PYTHONPATH=$PYTHONPATH:/opt/udaan/drishti/:/home/pi/.local/bin/

cd /opt/udaan/drishti/src || exit

case $test in
  test)
    python3 test/test.py --verbose
    ;;

  main)
    python3 main/drishti/main.py
    ;;

  camera)
    python3 main/commons/hal/camera.py --verbose
    ;;

  web)
    python3 main/drishti/api/web.py
    ;;

  *)
    python3 test/test.py --verbose
    ;;
esac