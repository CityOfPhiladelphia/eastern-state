# Eastern State (Penitentiary)

A secure place to store your environment secrets, using [AWS S3](https://aws.amazon.com/s3/) and [AWS KMS](https://aws.amazon.com/kms/).

## Usage

Eastern State uses a YAML to store environment variables in a file. Multiple environments, such as production and development can be stored in one file. Individual environment variables can be optionally encrypted using AWS KMS if they are sensitive, such as a database password. Environment variables are encrypted individually and are stored one per line, which means the file an be placed in a source control system, like GIT.

Example file:

```
name: my_app
bucket: eastern-state-test
environments:
  dev:
    kms_key: arn:aws:kms:us-east-1:676612114792:alias/eastern-state-test
    variables:
      FLASK_HTTP_PORT: 8080
      FLASK_HOST: localhost
      DB_HOST: localhost
      DB_PORT: 5432
      DB_USERNAME: app
      DB_PASSWORD: password
      DB_DATABASE: my_app
  prod:
    kms_key: arn:aws:kms:us-east-1:676612114792:alias/eastern-state-test
    variables:
      FLASK_HTTP_PORT: 80
      FLASK_HOST: app.example.com
      DB_HOST: db.example.com
      DB_PORT: 5432
      DB_USERNAME: app
      DB_PASSWORD: !unencrypted KT46?Ju?7#u?gTeY
      DB_DATABASE: my_app
```

Here, my_app has two environments, dev and prod. Each environment is has it's own KMS key. AWS policies can be used to control what users and roles can encrypt and decrupt using a KMS key.

In this example, we have an unencrypted password, marked with the `! unencrypted` YAML tag. If we run the encrypt command, eastern state will encrypt the password and flip the tag to `!encrypted`

```
cat example.yml | eastern_state encrypt
```

To use the environment file in AWS:

```
cat example.yml | eastern_state upload
```

Eastern state stores the file in \<bucket\>/\<name\>.


To load an environment:

```
eastern_state load_environment <bucket> <name> <env>
```

Example

```
eastern_state load_environment eastern-state my_app prod
```

`load_environment` outputs `export` statements that can be used in a Bash file. To load it in the current shell:

```
source <(eastern_state load_environment <bucket> <name> <env>)
```