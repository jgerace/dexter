import urllib.parse
from django.urls import reverse


def get_url_with_query_params(url_name: str, query_params: dict, *args) -> str:
    base_url = reverse(url_name, args=args)
    query_string = urllib.parse.urlencode(query_params)
    url = "{}?{}".format(base_url, query_string)
    return url
