#!/bin/bash
echo "Running CreateUser Service"

PYTHONPATH=src python -m features.user.create_user.server

sleep 10
