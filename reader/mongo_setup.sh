#!/bin/bash
sleep 10

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