import threading
import uuid

request_id_storage = threading.local()
request_id_storage.request_id = uuid.uuid4()
