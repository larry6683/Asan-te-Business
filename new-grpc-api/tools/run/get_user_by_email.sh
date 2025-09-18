#!/bin/bash
echo "Running GetUserByEmail Service"

PYTHONPATH=src python -m features.user.get_user_by_email.server

sleep 10
