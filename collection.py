import weaviate

def setup(client: weaviate.WeaviateClient, name: str, **kwargs) -> None:
    """Create a collection with specified name and parameters or re-create an existing one."""
    if not client.collections.exists(name):
        client.collections.create(name, **kwargs)
        return

    client.collections.delete(name)
    setup(client, name, **kwargs)

    count = sum(1 for _ in client.collections.get(name).iterator())
    assert count == 0