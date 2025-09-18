#!/bin/bash
echo "Running all user services"

PYTHONPATH=src ./tools/parallel_commands.sh -q \
    "echo get_user_by_email && python -m features.user.get_user_by_email.server" \
    "echo create_user && python -m features.user.create_user.server" \
    # Add more services here as they are implemented

sleep 10
