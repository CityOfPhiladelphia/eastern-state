import yaml
import click

from .yaml_utils import Loader, Dumper
from .encryption import encrypt_file, decrypt_file

## TODO: create git hooks to prevent unencrypted creds from being committed

@click.group()
def main():
    pass

def output(file, env_file, save):
    output = yaml.dump(env_file, Dumper=Dumper)

    click.echo(output)

    if save:
        file.seek(0)
        file.truncate()
        file.write(output)

@main.command(help='Encrypts values tagged `!encrypt` and overwrites the file.')
@click.option('-f','--filename', default='env.yml', help='Environments YAML file path')
@click.option('--save', is_flag=True, default=False, help='Save, overwriting existing file')
def encrypt(filename, save):
    with open(filename, 'r+') as file:
        env_file = yaml.load(file, Loader)

        encrypt_file(env_file)

        output(file, env_file, save)

@main.command(help='Decrypts values tagged `!encrypted` and overwrites the file.')
@click.option('-f','--filename', default='env.yml', help='Environments YAML file path')
@click.option('--save', is_flag=True, default=False, help='Save, overwriting existing file')
def decrypt(filename, save):
   with open(filename, 'r+') as file:
        env_file = yaml.load(file, Loader)

        decrypt_file(env_file)

        output(file, env_file, save)

@main.command(help='Uploads environment files to S3')
@click.option('-f','--file', default='env.yml', help='Environments YAML file path')
def upload():
    ## TODO: upload into files <bucket>/<name>/<env>
    pass
