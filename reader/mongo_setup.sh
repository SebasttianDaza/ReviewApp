#!/bin/bash
set -e

wait_for_mongo () {
  until mongosh --host "$1" --eval "db.runCommand({ ping: 1 })" >/dev/null 2>&1; do
    echo "Waiting a $1..."
    sleep 2
  done
}

wait_for_mongo review_reader_db:27017
wait_for_mongo review_reader_db_1:27017
wait_for_mongo review_reader_db_2:27017

echo "Starting replicat set...."
mongosh --host review_reader_db:27017 <<EOF
  var cfg = {
    "_id": "myReplicaSet",
    "version": 1,
    "members": [
      {
        "_id": 0,
        "host": "review_reader_db:27017",
        "priority": 2
      },
      {
        "_id": 1,
        "host": "review_reader_db_1:27017",
        "priority": 0
      },
      {
        "_id": 2,
        "host": "review_reader_db_2:27017",
        "priority": 0
      }
    ]
  };
  rs.initiate(cfg);
EOF

echo "Waiting to the primary node is available"
until mongosh --host review_reader_db:27017 --eval "rs.isMaster().ismaster" | grep "true" >/dev/null; do
  echo "Waiting that  review_reader_db would be PRIMARY..."
  sleep 2
done

mongosh --host review_reader_db:27017 <<EOF
use reader;

db.createUser({
  user: "root",
  pwd: "root",
  roles: [{ role: "readWrite", db: "reader" }]
});

db.createUser({
  user: "reader",
  pwd: "reader",
  roles: [{ role: "readWrite", db: "reader" }]
});

db.createCollection("reader_review", {
  validator: {
    "\$jsonSchema": {
      bsonType: "object",
      required: ["title", "subtitle", "body", "date_created", "date_update"],
      properties: {
        title: { bsonType: "string" },
        subtitle: { bsonType: "string" },
        body: { bsonType: "string" },
        date_created: { bsonType: "date" },
        date_update: { bsonType: "date" }
      }
    }
  }
});

db.createCollection("reader_video");
db.createCollection("reader_image");
EOF

echo "MongoDB ReplicaSet configure right ✅"