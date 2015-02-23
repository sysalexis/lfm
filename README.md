# lfm

[![Travis](https://img.shields.io/travis/willyg302/lfm.svg?style=flat-square)](https://travis-ci.org/willyg302/lfm)
[![license](http://img.shields.io/badge/license-MIT-red.svg?style=flat-square)](https://raw.githubusercontent.com/willyg302/lfm/master/LICENSE)

> The [AWS Lambda](http://aws.amazon.com/lambda/) Function Manager

## Hi There!

You're probably wondering what lfm is good for. Well, suppose you woke up one day and suddenly realized you needed a Lambda function for [AES encryption](http://en.wikipedia.org/wiki/Advanced_Encryption_Standard). You *could* roll your own solution, but ain't nobody got time for that. So you do a quick GitHub search and -- lo and behold -- there's [this beauty](https://github.com/willyg302/aws-lambda-aes).

Normally you'd have to clone the repo, install its dependencies, zip it up, and deploy it yourself. But with lfm, you can just do:

```bash
$ lfm deploy gh:willyg302/aws-lambda-aes --role execution_role_arn
```

## What?! No Way!

Yup, and it works with local directories too:

```bash
$ lfm deploy my-sweet-function/ --role execution_role_arn
$ lfm deploy --role execution_role_arn  # Will deploy working directory
```

In addition, you can override any of the usual config (see `lfm deploy -h` for options).

## So What's the Secret?

The magic of lfm is a special file called `.lambda.yml` at the root of a repo or directory. It looks something like this:

```yaml
config:
  FunctionName: my-awesome-sauce-function
  Handler: index.handler
  Mode: event
  Runtime: nodejs
  Description: This function will blow your mind
  Role: execution_role_arn  # Not recommended, especially in a public repo
install: npm install --production
ignore:
  - test/
  - README.md
```

`config` holds all that junk you're used to passing to `upload-function`, so you don't have to type it out any more. Note that any config you provide to `lfm deploy` will override the values in this file.

`install` is a single command for installing dependencies before zipping up the function. In this example, we want to install some production Node modules, but you could just as well use `make` and the like.

`ignore` is a list of paths that will not be added to the zip file.

**NOTE**: You don't *need* a `.lambda.yml` to be able to use lfm; it's just easier that way. Without the config file, you'll have to provide all the required config as command-line arguments.

## I Want Moar

Don't fret, we hear you! There are currently plans for the following features:

- **Single Files**: Currently you must provide a directory or Git repository, but it'd be nice to be able to deploy single files as well
- **GitHub Gists**: Give a Gist URL, get a running Lambda function
- **Webhooks**: A bit far-fetched, but wouldn't it be cool to `git push` and kick off a Lambda deploy?

## Testing

Call tests with `python setup.py test`.
