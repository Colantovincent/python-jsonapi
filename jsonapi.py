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
    """
    err: dict[str, str | dict] = {"status": str(status_code), "title": title, "detail": detail}
    if source:
        err["source"] = source
    return json.dumps({"errors": [err]})


def success_response(
    resource_type: str,
    resource_link: str,
    id_field: str | None,
    attributes: dict | list[dict] | None = None,
    metadata: dict[str, str | int] | None = None,
) -> str:
    """
    Generate a JSON:API-compliant success response. If ``attributes`` is a dictionary, returns data as a single object, otherwise as a list of dictionaries.
    :param resource_type: The type of the resource (e.g., ``"user"``, ``"device"``).
    :param resource_link: URL endpoint linking to the resource (for a list of resources, use the base endpoint).
    :param id_field: Key for the identifier's id in the resource's attributes dictionary.
    :param attributes: Attributes describing the resource. Can be a dictionary or
        a list of dictionaries. Defaults to ``None``.
    :param metadata: Additional metadata in dictionary format for the resource. Defaults to ``None``.
    :return: JSON-formatted string representing the JSON:API success response.
    """
    metadata = dict(metadata or {})
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
            "meta": {
                #to be filled
            }
        }
    elif isinstance(attributes, (list, tuple)):
        doc = {
            "jsonapi": {"version": "1.1"},
            "data": [],
            "meta": {
                "page": {
                    "total": metadata.get("total"),
                    "count": metadata.get("page_count", len(attributes)),
                    "number": metadata.get("page_number", 1),
                    "size": metadata.get("size", 30),
                }
            }
        }
        for el in attributes:
            resource_id = el[id_field]
            attrs = {k: v for k, v in el.items() if k != id_field}
            doc["data"].append(
                {
                    "type": resource_type,
                    "id": resource_id,
                    "attributes": attrs,
                    "links": {
                        "self": f"{resource_link}/{resource_id}",
                    },
                }
            )
    else:
        doc = {"jsonapi": {"version": "1.1"},}
    return json.dumps(doc)