import os
import shutil
import tempfile

import boto3
import clip
import frontmatter
import git
from giturl import *

import utils


def upload(zipfile, params):
	client = boto3.client('lambda')
	with open(zipfile + ".zip", 'rb') as f:
		params['FunctionZip'] = f
		try:
			response = client.upload_function(**params)
		except Exception as e:
			clip.exit(e, err=True)

def deploy_dir(path, kwargs):
	with utils.directory(path):
		config = utils.load_config()
		config['config'].update(kwargs)
		if 'FunctionName' not in config['config']:
			clip.exit('You must provide a function name', err=True)
		# Remove ignore paths
		for e in config['ignore'] + ['.git/', '.gitignore']:
			utils.delete_resource(e)
		# Run install command
		if 'install' in config:
			utils.shell(config['install'])
		# Zip up directory
		utils.make_zip(config['config']['FunctionName'])
		# Upload!
		params = config['config']
		upload(params['FunctionName'], params)

def deploy_file(path, kwargs, config):
	with utils.directory(os.path.dirname(path)):
		config.update(kwargs)
		if 'FunctionName' not in config:
			clip.exit('You must provide a function name', err=True)
		# Zip up directory
		utils.make_zip(config['FunctionName'])
		# Upload!
		upload(config['FunctionName'], config)

def run(path, kwargs):
	# Create a temporary working directory
	tmpdir = None
	try:
		tmpdir = tempfile.mkdtemp()
		g = GitURL(path)
		if g.valid:
			# Git repo
			url = g.to_ssh()
			dest = os.path.join(tmpdir, g.repo)
			clip.echo('Cloning git repo "{}" to "{}"...'.format(url, dest))
			git.Repo.clone_from(url, dest)
			deploy_dir(dest, kwargs)
		elif os.path.isdir(path):
			# Directory
			dest = os.path.join(tmpdir, os.path.basename(path))
			clip.echo('Copying directory "{}" to "{}"...'.format(path, dest))
			shutil.copytree(path, dest)
			deploy_dir(dest, kwargs)
		else:
			# File
			dest = os.path.join(tmpdir, os.path.basename(path))
			parsed = frontmatter.load(path)
			clip.echo('Copying file "{}" to "{}"...'.format(path, dest))
			with open(dest, 'w') as f:
				f.write(parsed.content)
			deploy_file(dest, kwargs, parsed.metadata)
	finally:
		# Clean up our temporary working directory
		if tmpdir:
			utils.delete_resource(tmpdir)
