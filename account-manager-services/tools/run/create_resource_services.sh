echo "Running Resource Services"

PYTHONPATH=src ./tools/parallel_commands.sh \
    "python -m features.resource.create_resource.server" # \
    # "python -m features.resource.get_resource.server" \
    # "python -m features.resource.update_resource.server"
    
sleep 10