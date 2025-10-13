class ApiUtils:
    @staticmethod
    def get_included_resources(included_param: str) -> list[str]:
        resource_types = []
        if included_param:
            for resource_type in included_param.split(','):
                resource_types.append(resource_type)
        return resource_types