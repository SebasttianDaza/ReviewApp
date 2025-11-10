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
  use reader;
  db.createUser(
    {
        user: "root",
        pwd: "root",
        roles:[
            {
                role: "readWrite",
                db:   "reader"
            }
        ]
    }
  );
  db.createUser(
    {
        user: "reader",
        pwd: "reader",
        roles:[
            {
                role: "readWrite",
                db:   "reader"
            }
        ]
    }
  );
  db.createCollection("reader_review", {
    validator: {
      "$jsonSchema": {
        bsonType: "object",
        title: "Student Object Validation",
        required: [ "title", "subtitle", "body", "date_created", "date_update" ],
        properties: {
          title: {
            bsonType: "string",
            description: "'title' must be a string and is required"
          },
          subtitle: {
            bsonType: "string",
            description: "'subtitle' must be a string and is required"
          },
          date_created: {
            bsonType: "date",
            description: "'date_created' must be a date and is requires"
          },
          date_update: {
            bsonType: "date",
            description: "'date_update' must be a date and is requires"
          }
        }
      }
    }
  });
  db.createCollection("reader_video");
  db.createCollection("reader_image");
EOF