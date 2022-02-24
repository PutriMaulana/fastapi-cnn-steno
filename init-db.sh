#!/bin/sh -e

mysql -s --user=$MYSQL_USER --password=$MYSQL_PASSWORD $MYSQL_DATABASE <<QUERY_INPUT
    CREATE DATABASE IF NOT EXISTS db_tugas_akhir;
    SOURCE /tmp/db_tugas_akhir.sql;
QUERY_INPUT