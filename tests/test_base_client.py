import sys
print sys.path
from abiosgaming.base_client import BaseAbiosClient
import vcr

client = None

def get_client():
    if not client:
        client = BaseAbiosClient()
    return client

