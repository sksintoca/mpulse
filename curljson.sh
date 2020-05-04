#!/usr/bin/env bash
curl -d "@data.json" -H "Content-Type: application/json" -X POST http://localhost:5000/member
