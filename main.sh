#!/bin/bash

# find /
# pwd
if test -f "/app/dist/bundle.js"; then
  npm run-script clean
fi
npm run-script start