#!/bin/bash

# find /
# pwd



yarn run clean
# if test -f "/app/dist/bundle.js"; then
#   # npm run-script clean
#   yarn run clean
# fi
# npm run-script start
yarn run start &

python3 /app/main.py &

wait