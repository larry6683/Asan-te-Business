echo "Running all services"

PYTHONPATH=src ./tools/parallel_commands.sh -q \
    "echo create_resource    && python -m features.resource.create_resource.server" \
    # "echo get_resource    && python -m features.resource.get_resource.server" \
    # "echo update_resource && python -m features.resource.update_resource.server" \
    # "echo delete_resource && python -m features.resource.delete_resource.server" \
    # \
    # other service categories go here

sleep 10