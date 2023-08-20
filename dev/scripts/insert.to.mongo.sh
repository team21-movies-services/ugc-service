#!/usr/bin/env bash

action_time=`date +'%s'`

mongosh --host localhost --port 27017 <<EOF
use film_events;
db.film_events.insertOne(
  {
    "action_type": "favorite",
    "action_time": "$action_time",
    "user_id": "32207c69-1917-4d8c-8a11-69eb52122495",
    "film_id": "32207c69-1917-4d8c-8a11-69eb52122495"
  }
)
EOF


# mongosh --host localhost --port 27017 <<EOF
# use film_events;
# db.film_events.insertOne(
#   {
#     "action_type": "favorite",
#     "action_time": "$action_time",
#     "user_id": "32207c69-1917-4d8c-8a11-69eb52122495",
#     "film_id": "32207c69-1917-4d8c-8a11-69eb52122495"
#   }
# )
# EOF


# mongosh --host localhost --port 27017 <<EOF
# use film_events;
# db.film_events.findOne(ObjectId("64dfb8711d3df9c5a1324d16"))
# EOF