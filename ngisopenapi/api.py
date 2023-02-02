import requests
import re
import itertools

def get_link(headers): 
  if "Link" in headers:
    return re.search(r'\<(.*?)>; rel=\"next\"', headers["Link"]).group(1)
  return None

def merge_lists(lists):
  return list(itertools.chain.from_iterable(lists))

def merge_dicts(dict1, dict2=None):
    if dict2:
      return {**dict1, **dict2}
    return dict1

def get_query(objectType=None):
  if objectType is None:
    return None
  return f'eq(*,{objectType})'

class NgisOpenApi:
    def __init__(self, url, user, password, client_product_version):
        self.url = url
        self.user = user
        self.password = password
        self.client_product_version = client_product_version

    def get_datasets(self):
      return self._send_request(f'/datasets')[0]

    def get_dataset_info(self, dataset_id):
        return self._send_request(f'/datasets/{dataset_id}')[0]

    def get_features(self, dataset_id, bounds, objectType=None):
        return {
            "type": "FeatureCollection",
            "features": merge_lists(self._get_features_paginated(f'/datasets/{dataset_id}/features', {"bbox": bounds, "query": get_query(objectType)}))
        }

    def _get_features_paginated(self, path, params=None):
      t = self._send_request(path, params, {"accept": "application/vnd.kartverket.sosi+json; version=1.0"})
      if t[1] is not None:
        return [t[0]["features"], self._get_features_paginated(t[1])[0]]
      return [t[0]["features"]]

    def _send_request(self, path, params=None, extra_headers=None):
        r = requests.get(
          f'{self.url}{path}',
          auth=(self.user, self.password),
          params=params,
          headers=merge_dicts({"X-Client-Product-Version": self.client_product_version}, extra_headers)
        )
        if r.ok:
            next_link = get_link(r.headers)
            return (r.json(), next_link.replace(self.url, "") if next_link is not None else None)
        return (None, None)