import json

def read(bucket, file_name):
    blob_input = bucket.blob(file_name)
    contents = blob_input.download_as_string()
    batch = [json.loads(record) for record in contents.split(b'\n')]
    return batch