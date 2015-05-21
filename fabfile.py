from fabric.api import *
from fabric_ec2 import EC2TagManager
import re
from fab_config import *
#
# TODO create a fab_config.py file with these set to you correct values
#

# amazon_key = 'asdf'
# amazon_secret = 'asdf'
# amazon_regions = ['us-west-1']
# keypair_location = '/home/david/dliukeypair.pem'
# mesos_master_host = '50.18.130.73'

def testing_instances():
	tags = EC2TagManager(amazon_key, amazon_secret, regions= amazon_regions, common_tags={'Name': 'testing'})
	return tags.get_instances()

def staging_instances():
	tags = EC2TagManager(amazon_key, amazon_secret, regions= amazon_regions, common_tags={'Name': 'staging'})
	return tags.get_instances()

def production_instances():
	tags = EC2TagManager(amazon_key, amazon_secret, regions= amazon_regions, common_tags={'Name': 'production'})
	return tags.get_instances()

# def ec2_master_instances():
# 	tags = EC2TagManager(amazon_key, amazon_secret, regions = amazon_regions, common_tags = {'Name':'mesos-master'})
# 	return tags.get_instances()

#
# setup which hosts to install on
#
def testing():
	testing_hosts = testing_instances()
	env.hosts = testing_hosts
	env.user = 'ubuntu'
	env.key_filename = [keypair_location]
	print 'these nodes will be affected'+str(len(testing_hosts))
def staging():
	staging_hosts = staging_instance()
	env.hosts = staging_hosts
	env.user = 'ubuntu'
	env.key_filename = [keypair_location]
	print 'these nodes will be affected'+str(len(staging_instances))
	
@parallel
def setup_host():
	print("Executing on %(host)s as %(user)s" % env)
	sudo('export DEBIAN_FRONTEND=noninteractive')
	sudo('apt-get -y update')
	sudo('apt-get -y install curl') 
	sudo('apt-get -y install git') 
	sudo('apt-get -y install python-setuptools') 
	sudo('apt-get -y install python-pip') 
	sudo('apt-get -y install python-dev')
	sudo('apt-get -y install python-protobuf')

	#
	# install flask stuff
	#
	sudo('pip install Flask')
	sudo('pip install git+https://github.com/dgrtwo/ParsePy.git')
	sudo('pip install google-api-python-client')
	sudo("pip install rauth")
	sudo("pip install Flask-Login")
	sudo('pip install django-jsonify')
	sudo('pip install fabric')
	sudo('pip install boto')
	sudo('apt-get -y install python-numpy')

	#
	# pull the project and start it
	#
	sudo('git clone https://github.com/kzhang22/pbl_portal.git')

@parallel
def kill():
	print("Executing on %(host)s as %(user)s" % env)
	sudo('fuser -k 5000/tcp')

@parallel
def deploy():
	print("Executing on %(host)s as %(user)s" % env)

	#
	# kill process running on port 5000
	#
	# cd('pbl_portal')
	# kill()
	sudo('python pbl_portal/app.py')





