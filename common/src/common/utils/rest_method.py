"""
Rest Methods
"""
import requests


def post_method(url: str,
                request_body=None,
                query_params=None,
                data=None,
                files=None,
                token=None) -> dict:
  """
    Function for API test POST method
    Parameters
    ----------
    url: str
    request_body: dict
    query_params: dict
    data: dict
    files: File
    token: token
    Returns
    -------
    Json Object
    """

  return requests.post(
      url=f"{url}",
      json=request_body,
      params=query_params,
      data=data,
      files=files,
      headers={"Authorization": token},
      timeout=10
      )


def get_method(url: str, query_params=None, token=None) -> dict:
  """
    Function for API test GET method
    Parameters
    ----------
    url: str
    query_params: dict
    token: token
    Returns
    -------
    JSON Object
    """

  return requests.get(
      url=f"{url}",
      params=query_params,
      headers={"Authorization": token},
      allow_redirects=False,
      timeout=10
      )


def put_method(url: str,
               request_body: dict,
               query_params=None,
               token=None) -> dict:
  """
    Function for API test PUT method
    Parameters
    ----------
    url: str
    request_body: dict
    query_params: dict
    token: token
    Returns
    -------
    JSON Object
    """

  return requests.put(
      url=f"{url}",
      json=request_body,
      params=query_params,
      headers={"Authorization": token},
      timeout=10
      )


def delete_method(url: str, query_params=None, token=None) -> dict:
  """
    Function for API test DELETE method
    Parameters
    ----------
    url: str
    query_params: dict
    token: token
    Returns
    -------
    JSON Object
    """

  return requests.delete(
      url=f"{url}", params=query_params, headers={"Authorization": token},
      timeout=10
      )
