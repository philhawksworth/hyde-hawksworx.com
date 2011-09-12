# Fabric fro deploying hawksworx.com

from fabric.api import *
import os
import fabric.contrib.project as project
import datetime
import ConfigParser
from fabric.colors import yellow

# from __future__ import with_statement
from fabric.contrib import console, django
from fabric.context_managers import cd



PROD = 'hawksworx.com'
DEST_PATH = '/var/www/hawksworx.com'
ROOT_PATH = os.path.abspath(os.path.dirname(__file__))
DEPLOY_PATH = os.path.join(ROOT_PATH, 'production_site')



# django.settings_module('ebay.config.europe.settings.local')
# from django.conf import settings

env.project = "hawksworx"

# SERVER
PRODUCTION = '46.51.184.117'

# PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
# here = lambda *x: os.path.join(PROJECT_ROOT, *x)
# 
# config = ConfigParser.ConfigParser()
# config.readfp(open('fabric.cfg'))
# 
# env.bucket = config.get('production', 'bucket')
# env.git_url = config.get('production', 'git_url')
# env.access_key = config.get('production', 'access_key')
# env.secret_key = config.get('production', 'secret_key')
# 
# tmp_time = datetime.datetime.now()
# env.time = tmp_time.strftime("%Y%m%d_%H%M%S")
# env.clone_path = here('tmp', env.time )
# env.htdocs = here('tmp', env.time, 'www')



# Hyde utilities

def clean():
    ''' remove the previoiusly generated dirs '''
    local('rm -rf ./deploy')
    local('rm -rf ./production_site')

def regen():
    ''' generate a new version of the site '''
    clean()
    local('hyde gen')
    local('chmod -R 777 ./deploy')

def serve():
    ''' run the local test server '''
    local('hyde serve')

def reserve():
    ''' rgenerate and serve the site '''
    regen()
    serve()

def genprod():
    ''' generate a version for production '''
    clean()
    local('hyde gen -c production.yaml -d ./production_site')
    local('chmod -R 777 ./production_site')


# Server utilities

def staging():
    """Staging site"""
    env.alias = "staging"
    env.hosts = [PRODUCTION]
    env.path = '/var/www/stage.hawksworx.com'
    env.user = 'ubuntu'
    env.key_filename  = '/Users/phil.hawksworth/.ssh/philhawksworth-aws.pem'
    env.apache = ['stage.hawksworx.com',]
    env.release_path = "/var/releases/hawksworx.com"

def production():
    """Production site"""
    env.alias = "production"
    env.hosts = [PRODUCTION]
    env.path = '/var/www/hawksworx.com'
    env.user = 'ubuntu'
    env.key_filename  = '/Users/phil.hawksworth/.ssh/philhawksworth-aws.pem'
    env.apache = ['hawksworx.com', ]
    env.release_path = "/var/releases/hawksworx.com"


def deploy():
    """Deployment actions"""
    export_release()
    # copy_settings_local()

def export_release():
    """Exports a release with the current time and date"""
    run('cd %s && git pull origin master' % env.release_path)
    run('cp -R %(release_path)s/deploy/ %(path)s' % env)


def symlink_release():
    """Removes the old release and symlinks latest release to current"""
    # remove current deployment
    run('rm %(path)s/current' % env)
    # symlink deployment
    run('ln -s %(path)s/releases/%(release_name)s/ %(path)s/current' % env)

def copy_apache():
    """Copies the apache file to the appropriate location."""
    command = 'cp %s/current/etc/apache2/%s /etc/apache2/sites-available/'
    for config in env.apache:
        sudo(command % (env.path, config))

def restart():
    """Restarts the apache server"""
    copy_apache()
    sudo('/etc/init.d/apache2 restart')

    # 
    # def uploadattachments():
    #     """Update the local copy of the attachment dir
    #     using alias since it is having issues with
    #     full username / server
    #     """
    #     if env.alias == 'staging':
    #         local('rsync -avz --rsh=\'ssh -p%(port)s\' %(media_root)s/ %(user)s@%(host)s:%(path)s/attachments/' % env)
    #     else:
    #         print 'Server %(alias)s is not allowed to upload attachments' % env

    # def clean():
    #     """Remove pyc files from the server."""
    #     run('find %s/current -iname \*pyc -delete' % env.path)











# 
# def deploy(version=None):
#     """Deployment actions into S3 using s3put"""
#     local('mkdir -p %(clone_path)s' % env)
#     local('git clone %(git_url)s  %(clone_path)s' % env)
#     if version:
#         env.version = version
#         local('cd %(clone_path)s && git checkout %(version)s' % env)
#     local('./s3put.py -a %(access_key)s -s %(secret_key)s -b %(bucket)s -p %(htdocs)s -g public-read %(htdocs)s' % env)
#     print yellow("Done?")