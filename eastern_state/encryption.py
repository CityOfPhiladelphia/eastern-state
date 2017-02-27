import base64
from collections import OrderedDict

import boto3

from .yaml_utils import UnencryptedTag, EncryptedTag

## encrypt

def encrypt_value(client, config, value):
    config['Plaintext'] = str(value.value).encode('utf-8')
    response = client.encrypt(**config)
    config['Plaintext'] = None

    return EncryptedTag(base64.b64encode(response['CiphertextBlob']).decode('utf-8'))

def encrypt_file(env_file):
    client = boto3.client('kms')

    for env in env_file['environments']:
        config = {
            'KeyId': env_file['environments'][env]['kms_key'],
            'EncryptionContext': {
                'name': env_file['name'],
                'env': env
            }
        }

        for variable in env_file['environments'][env]['variables']:
            value = env_file['environments'][env]['variables'][variable]
            if isinstance(value, UnencryptedTag):
                env_file['environments'][env]['variables'][variable] = encrypt_value(client, config, value)

## decrypt

def decrypt_value(client, config, value):
    config['CiphertextBlob'] = base64.b64decode(value.value)
    response = client.decrypt(**config)
    config['CiphertextBlob'] = None

    return UnencryptedTag(response['Plaintext'].decode('utf-8'))

def decrypt_file(env_file):
    client = boto3.client('kms')

    for env in env_file['environments']:
        config = {
            'EncryptionContext': {
                'name': env_file['name'],
                'env': env
            }
        }

        for variable in env_file['environments'][env]['variables']:
            value = env_file['environments'][env]['variables'][variable]
            if isinstance(value, EncryptedTag):
                env_file['environments'][env]['variables'][variable] = decrypt_value(client, config, value)
