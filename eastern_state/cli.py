import yaml
import click

from .yaml_utils import Loader, Dumper
from .encryption import encrypt_file, decrypt_file

## TODO: create git hooks to prevent unencrypted creds from being committed

## TODO: should a separate key be used for each environment? look at IAM

@click.group()
def main():
    pass

@main.command(help='Encrypts values tagged `!encrypt` and overwrites the file.')
@click.option('-f','--filename', default='env.yml', help='Environments YAML file path')
def encrypt(filename):
    with open(filename, 'r+') as file:
        env_file = yaml.load(file, Loader)

        encrypt_file(env_file)

        file.seek(0)
        file.truncate()

        file.write(yaml.dump(env_file, Dumper=Dumper))

@main.command(help='Decrypts values tagged `!encrypted` and overwrites the file.')
@click.option('-f','--filename', default='env.yml', help='Environments YAML file path')
def decrypt(filename):
   with open(filename, 'r+') as file:
        env_file = yaml.load(file, Loader)

        decrypt_file(env_file)

        file.seek(0)
        file.truncate()

        file.write(yaml.dump(env_file, Dumper=Dumper))

@main.command(help='Uploads environment files to S3')
@click.option('-f','--file', default='env.yml', help='Environments YAML file path')
def upload():
    ## TODO: upload into files <bucket>/<name>/<env>
    pass
