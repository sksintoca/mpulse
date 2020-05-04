#!/usr/bin/env bash
curl -i -X POST -H "Content-Type: multipart/form-data" -F "file=@member_data.csv" http://localhost:5000/upload
