#!/bin/bash
set -o errexit #Exit when the command returns a non-zero exit status (failed).

if [ $APP_ENV_NAME == 'local' ];then
wait-for-it --service $HOST --timeout 20
fi

exec "$@" # make the entrypoint a pass through that then runs the docker command