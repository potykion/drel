import threading
import uuid

from elasticsearch import Elasticsearch

request_id_storage = threading.local()
request_id_storage.request_id = str(uuid.uuid4())

es = Elasticsearch()

APPLICATION = "default"
