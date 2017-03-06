import sys

import yaml
import click
import boto3

from .yaml_utils import Loader, Dumper, UnencryptedTag, EncryptedTag
from .encryption import encrypt_file, decrypt_file

## TODO: create git hooks to prevent unencrypted creds from being committed
## TODO: prevent upload when !unencrypted values exist

@click.group()
def main():
    pass

@main.command(help='Encrypts values tagged `!encrypt` and overwrites the file.')
@click.option('-f','--filename', help='Environments YAML file path')
def encrypt(filename):
    if filename != None:
        file = open(filename)
    else:
        file = sys.stdin

    env_file = yaml.load(file, Loader)

    if filename != None:
        file.close()

    encrypt_file(env_file)

    output = yaml.dump(env_file, Dumper=Dumper)

    sys.stdout.write(output)

@main.command(help='Decrypts values tagged `!encrypted` and overwrites the file.')
@click.option('-f','--filename', help='Environments YAML file path')
def decrypt(filename):
    if filename != None:
        file = open(filename)
    else:
        file = sys.stdin

    env_file = yaml.load(file, Loader)

    if filename != None:
        file.close()

    decrypt_file(env_file)

    output = yaml.dump(env_file, Dumper=Dumper)

    sys.stdout.write(output)

@main.command(help='Uploads environment config file to S3')
@click.option('-f','--filename', help='Environments YAML file path')
def upload(filename):
    if filename != None:
        file = open(filename)
    else:
        file = sys.stdin

    raw_file = file.read().encode('utf-8')

    env_file = yaml.load(raw_file, Loader)

    client = boto3.client('s3')

    client.put_object(
        Bucket=env_file['bucket'],
        Key=env_file['name'],
        Body=raw_file)

    if filename != None:
        raw_file.close()

@main.command(help='Downloads environment config file from S3')
@click.argument('bucket')
@click.argument('name')
@click.option('-f','--filename', help='Path to save environments YAML')
def download(bucket, name, filename):
    client = boto3.client('s3')

    response = client.get_object(
        Bucket=bucket,
        Key=name)

    output = response['Body'].read().decode('utf-8')

    if filename != None:
        with open(filename, 'w+') as file:
            file.write(output)
    else:
        sys.stdout.write(output)

@main.command(help='Outputs bash environment exports')
@click.argument('env')
@click.option('-f','--filename', help='Environments YAML file path')
def exports(env, filename):
    if filename != None:
        file = open(filename)
    else:
        file = sys.stdin

    env_file = yaml.load(file, Loader)

    if filename != None:
        file.close()

    variables = env_file['environments'][env]['variables']

    def get_value(value):
        if isinstance(value, UnencryptedTag) or isinstance(value, EncryptedTag):
            return value.value
        return value

    output = ''
    for var in variables:
        output += 'export {}={}\n'.format(var, get_value(variables[var]))

    sys.stdout.write(output)
