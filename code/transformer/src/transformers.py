import time

def feature_to_concept_score(feature):
    return {
        'metadata': {
            'consumed_at': feature['metadata']['consumed_at'],
            'transformed_at': int(time.time() * 1000)
        },
        'key': {
            'concept_id': feature['key']['accommodation_feature_id'],
            'concept_ns': feature['key']['accommodation_feature_ns'],
            'accommodation_id': feature['key']['accommodation_id'],
            'accommodation_ns': feature['key']['accommodation_ns']
        },
        'value': {
            'key': {
                'concept_id': feature['value']['key']['accommodation_feature_id'],
                'concept_ns': feature['value']['key']['accommodation_feature_ns'],
                'accommodation_id': feature['value']['key']['accommodation_id'],
                'accommodation_ns': feature['value']['key']['accommodation_ns']
            },
            'score': feature['value']['score']
        } if feature['value'] is not None else None
    }