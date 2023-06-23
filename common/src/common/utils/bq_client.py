'''
Bigquery Client
'''
from google.cloud import bigquery

client = bigquery.Client()


def bq_client():
  return client
