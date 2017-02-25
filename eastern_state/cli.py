import yaml
import click

from .yaml_utils import Loader, Dumper
from .encryption import encrypt_data, decrypt_data

## TODO: create hit hooks to prevent unencrypted creds from being committed

## TODO: should a separate key be used for each environment? look at IAM

@click.group()
def main():
    pass

@main.command(help='Encrypts values tagged `!encrypt` and overwrites the file.')
@click.option('-f','--filename', default='env.yml', help='Environments YAML file path')
def encrypt(filename):
    with open(filename) as file:
        env_file = yaml.load(file, Loader)

    encrypt_data(env_file)

    print(env_file)

@main.command(help='Decrypts values tagged `!encrypted` and overwrites the file.')
@click.option('-f','--filename', default='env.yml', help='Environments YAML file path')
def decrypt(filename):
    with open(filename) as file:
        env_file = yaml.load(file, Loader)

    decrypt_data(env_file)

    print(env_file)

@main.command(help='Uploads environment files to S3')
@click.option('-f','--file', default='env.yml', help='Environments YAML file path')
def upload():
    ## TODO: upload into files <bucket>/<name>/<env>
    pass
