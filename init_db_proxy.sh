#!/usr/bin/env bash
./cloud_sql_proxy -instances "healthy-zone-266815:us-central1:iot-rfid-test"=tcp:5432
