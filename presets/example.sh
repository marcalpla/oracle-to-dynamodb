#!/bin/bash

cd $(dirname "$(realpath "$0")")/..
poetry run oracle-to-dynamodb \
    --oracle-dsn "host:port/service" \
    --oracle-user "user" \
    --oracle-password "password" \
    --select-query "SELECT col1, col2 FROM table" \
    --dynamodb-table-name "MyDynamoDBTable" \
    --dynamodb-attributes '["Attribute1", "Attribute2"]'    