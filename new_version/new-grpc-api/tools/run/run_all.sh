#!/bin/bash
echo "Running all user services"

PYTHONPATH=src ./tools/parallel_commands.sh -q \
    "echo get_user_by_email && python -m features.user.get_user_by_email.server" \
    "echo create_user && python -m features.user.create_user.server" \
    # Add more services here as they are implemented

sleep 10
#!/bin/bash
echo "Running all user and business services"
echo "======================================"

# Set PYTHONPATH for all services
export PYTHONPATH=src

# Run all services in parallel using the parallel_commands.sh script
./tools/parallel_commands.sh -q \
    "echo '[USER] get_user_by_email starting on port 61000...' && python -m features.user.get_user_by_email.server" \
    "echo '[USER] create_user starting on port 62000...' && python -m features.user.create_user.server" \
    "echo '[BUSINESS] create_business starting on port 63000...' && python -m features.business.create_business.server"

echo
echo "All services have been started!"
echo "Services running on:"
echo "  - GetUserByEmail:   localhost:61000"
echo "  - CreateUser:       localhost:62000" 
echo "  - CreateBusiness:   localhost:63000"
echo
echo "Press Ctrl+C to stop all services"

sleep 10