import json

def store(batch, bucket, batch_id, folder):
    if not batch:
        return
    file_name = f'concept-scores/{folder}/{batch_id}.json'
    contents = '\n'.join([json.dumps(b) for b in batch])
    blob_output = bucket.blob(file_name)
    blob_output.upload_from_string(contents)
    return file_name

def read(bucket, file_name):
    blob_input = bucket.blob(file_name)
    contents = blob_input.download_as_string()
    batch = [json.loads(record) for record in contents.split(b'\n')]
    return batch