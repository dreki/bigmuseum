#!/bin/bash
pymongo-migrate migrate --migrations=migrations --uri "mongodb://$MONGO_USER:$MONGO_PASSWORD@$MONGO_HOST/?authSource=admin&readPreference=primary&directConnection=true&ssl=false"
