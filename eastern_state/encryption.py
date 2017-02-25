from collections import OrderedDict

import boto3

from .yaml_utils import UnencryptedTag, EncryptedTag

## encrypt

## TODO: use `name` and `env` name in encryption context

def encrypt_value(client, value):
    ## TODO: actually encrypt
    return EncryptedTag(value.value)

def encrypt_recursive(client, data):
    if isinstance(data, OrderedDict):
        for key in data:
            data[key] = encrypt_recursive(client, data[key])
    elif isinstance(data, UnencryptedTag):
        return encrypt_value(client, data)

    return data

def encrypt_data(data):
    client = boto3.client('kms')

    return encrypt_recursive(client, data)

## decrypt

## TODO: use `name` and `env` name in encryption context

def decrypt_value(client, value):
    ## TODO: actually decrypt
    return UnencryptedTag(value.value)

def decrypt_recursive(client, data):
    if isinstance(data, OrderedDict):
        for key in data:
            data[key] = decrypt_recursive(client, data[key])
    elif isinstance(data, EncryptedTag):
        return decrypt_value(client, data)

    return data

def decrypt_data(data):
    client = boto3.client('kms')

    return decrypt_recursive(client, data)
