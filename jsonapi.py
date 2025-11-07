import json

def error_response(
    status_code: int,
    title: str,
    detail: str,
    source: dict | None = None
) -> str:
    """
    Generate a JSON:API-compliant error response.

    :param status_code: HTTP status code for the error.
    :param title: Short, human-readable summary of the error.
    :param detail: Detailed description of the error.
    :param source: Information about the source of the error
        (e.g., pointer to a specific field in the request). Defaults to ``None``.
    :return: JSON-formatted string representing the JSON:API error response.

    :example:
        >>> error_response(400, "Invalid Request", "Missing 'email' field", {"pointer": "/data/attributes/email"})
        '{"errors": [{"status": "400", "title": "Invalid Request", "detail": "Missing \'email\' field", "source": {"pointer": "/data/attributes/email"}}]}'
    """
    err: dict[str, str | dict] = {"status": str(status_code), "title": title, "detail": detail}
    if source:
        err["source"] = source
    return json.dumps({"errors": [err]})


def success_response(
    resource_type: str,
    resource_link: str,
    id_field: str | None,
    attributes: dict | list[dict] | None = None
) -> str:
    """
    Generate a JSON:API-compliant success response. If ``attributes`` is a dictionary, returns data as a single object, otherwise as a list of dictionaries.

    :param resource_type: The type of the resource (e.g., ``"user"``, ``"device"``).
    :param resource_link: URL endpoint linking to the resource (for a list of resources, use the base endpoint).
    :param id_field: Key for the identifier's id in the resource's attributes dictionary.
    :param attributes: Attributes describing the resource. Can be a dictionary or
        a list of dictionaries. Defaults to ``None``.
    :return: JSON-formatted string representing the JSON:API success response.

    :example:
        >>> success_response("user", "/api/users/42", "42", {"name": "Alice", "email": "alice@example.com"})
        '{"jsonapi": {"version": "1.1"}, "data": {"type": "user", "id": "42", "attributes": {"name": "Alice", "email": "alice@example.com"}, "links": {"self": "/api/users/42"}}}'
    """
    if isinstance(attributes, dict):
        doc = {
            "jsonapi": {"version": "1.1"},
            "data": {
                "type": resource_type,
                "id": attributes.pop(id_field),
                "attributes": attributes,
                "links": {
                    "self": resource_link,
                },
            },
        }
    elif isinstance(attributes, list):
        doc = {
            "jsonapi": {"version": "1.1"},
            "data": []
        }
        for el in attributes:
            element_id = el.pop(id_field)
            temp = {
                "type": resource_type,
                "id": element_id,
                "attributes": el,
                "links": {
                    "self": f"{resource_link}/{element_id}",
                }
            }
    else:
        doc = {"jsonapi": {"version": "1.1"},}
    return json.dumps(doc)