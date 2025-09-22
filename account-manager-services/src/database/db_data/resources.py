from database.models.resource import ResourceDbo, ResourceCategoryCode

def get_resource_by_id(resource_id: str) -> ResourceDbo:
    return next((
        resource for resource in resources
        if resource.resource_id == resource_id
    ), 
    None
)

def query_resource_by_name(name: str) -> list[ResourceDbo]:
    return [
        resource for resource in resources
        if resource.name == name
    ]

resources = [
    ResourceDbo(
        resource_id="f491daf6-4560-447f-be55-e0ca9e2dcb76",
        name="Laptop",
        description="A high-end laptop",
        category=ResourceCategoryCode.HARDWARE,
    ),
    ResourceDbo(
        resource_id="39d57588-bf2f-4042-ad28-e6f60bc64ca4",
        name="Antivirus Software",
        description="Protects against malware",
        category=ResourceCategoryCode.SOFTWARE,
    ),
    ResourceDbo(
        resource_id="f9d960bf-7888-4b3f-8043-030d60dc09f8",
        name="Cloud Storage Service",
        description="Provides scalable storage solutions",
        category=ResourceCategoryCode.SERVICE,
    ),
]