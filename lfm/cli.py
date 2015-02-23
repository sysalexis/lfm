import os

import clip

import deploy
import utils


__version__ = '0.1.0'


########################################
# COMMAND LINE APP
########################################

app = clip.App()

def print_version(value):
	clip.exit('lfm version {}'.format(__version__))

@app.main(description='The AWS Lambda Function Manager')
@clip.flag('--version', callback=print_version, hidden=True, help='Print the version')
def lfm():
	pass

@lfm.subcommand(name='deploy', description='Deploy a Lambda function')
@clip.arg('path', default=os.getcwd(), help='Path to the function')
@clip.opt('-n', '--name', name='FunctionName', help='Name of the function')
@clip.opt('-r', '--role', name='Role', help='ARN of the function\'s IAM role')
@clip.opt('-x', '--handler', name='Handler', help='Function that Lambda calls to begin execution')
@clip.opt('-m', '--mode', name='Mode', help='How the Lambda function will be invoked')
@clip.opt('-d', '--description', name='Description', help='A short, user-defined function description')
@clip.opt('-t', '--runtime', name='Runtime', help='Runtime environment for the Lambda function')
@clip.opt('-o', '--timeout', name='Timeout', type=int, help='Function execution time')
@clip.opt('-s', '--size', name='MemorySize', type=int, help='Function memory (MB)')
def lfm_deploy(path, **kwargs):
	deploy.run(path, {k: v for k, v in utils.iteritems(kwargs) if v})


########################################
# MAIN METHOD
########################################

def main(args=None):
	err = None
	try:
		app.run(args)
	except clip.ClipExit:
		# Parser-level exception, such as help/version or unrecognized argument
		pass
	except Exception as e:
		err = e
		clip.echo(e, err=True)
	finally:
		# Do any last-minute cleanup
		pass

if __name__ == '__main__':
	main()
