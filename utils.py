import json
import requests

import settings


class HttpError(Exception):
    pass


def get(**kwargs):
    return query(method="GET", **kwargs)


def delete(**kwargs):
    return query(method="DELETE", **kwargs)


def post(**kwargs):
    return query(method="POST", **kwargs)


def put(**kwargs):
    return query(method="PUT", **kwargs)


def query(json_page=None, action=None, instance_id=None, method="GET", **kwargs):
    if instance_id is None:
        url = "https://{}/{}.json".format(settings.HOST, json_page)
    else:
        url = "https://{}/{}/{}.json".format(settings.HOST, json_page, instance_id)

    if method == "GET":
        req_method = requests.get
    elif method == "POST":
        req_method = requests.post
    elif method == "DELETE":
        req_method = requests.delete
    elif method == "PUT":
        req_method = requests.put

    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
    }

    # Creating the passed data as json
    data = json.dumps({"api_token": settings.API_TOKEN, action: kwargs})

    response = req_method(url=url, headers=headers, data=data)

    right_responses = {'GET': [200, 204, 205], 'POST': [201], 'DELETE': [200], 'PUT': [200]}
    if response.status_code in right_responses[method]:
        return response.json()

    error_msg = "Error {} during the query process for {} ({}). Data : {}, response : {}"
    raise HttpError(error_msg.format(response.status_code, url, method, data, response.json()))
