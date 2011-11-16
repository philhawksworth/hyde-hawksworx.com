# Fabric fro deploying hawksworx.com

from fabric.api import *
import os

PROD = 'hawksworx.com'
DEST_PATH = '/var/www/hawksworx.com'
ROOT_PATH = os.path.abspath(os.path.dirname(__file__))
DEPLOY_PATH = os.path.join(ROOT_PATH, 'production_site')


# django.settings_module('ebay.config.europe.settings.local')
# from django.conf import settings
env.project = "hawksworx"


# SERVER
PRODUCTION = '46.51.184.117'


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
    env.key_filename = '/Users/phil.hawksworth/.ssh/philhawksworth-aws.pem'
    env.apache = ['stage.hawksworx.com', ]
    env.release_path = "/var/releases/hawksworx.com"


def production():
    """Production site"""
    env.alias = "production"
    env.hosts = [PRODUCTION]
    env.path = '/var/www/hawksworx.com'
    env.user = 'ubuntu'
    env.key_filename = '/Users/phil.hawksworth/.ssh/philhawksworth-aws.pem'
    env.apache = ['hawksworx.com', ]
    env.release_path = "/var/releases/hawksworx.com"


def deploy():
    """Deployment actions"""
    export_release()


def export_release():
    """Exports a release with the current time and date"""
    run('cd %s && git pull origin master' % env.release_path)
    run('cp -R %(release_path)s/deploy/* %(path)s' % env)


def copy_apache():
    """Copies the apache file to the appropriate location."""
    command = 'cp %s/current/etc/apache2/%s /etc/apache2/sites-available/'
    for config in env.apache:
        sudo(command % (env.path, config))


def restart():
    """Restarts the apache server"""
    copy_apache()
    sudo('/etc/init.d/apache2 restart')


# from boto.s3.connection import S3Connection
# from boto.s3.key import Key
# from stat import *
# import time

# def deploy_media():
#     """Deploy the media files to S3 """
#     conn = S3Connection('ACCESS KEY ID', 'SECRET ACCESS KEY')
#     bucket = conn.get_bucket('bucketname')
#     #upload files
#     for root, dirs, files in os.walk('media'):
#         for f in files:
#             if f.endswith('.swp') or f.startswith('.') :
#                 continue
#             filename = root + '/' + f
#             modify_time = os.stat(filename)[ST_MTIME]
#             key = bucket.get_key(filename)
#             if key is None:
#                 key = Key(bucket)
#                 key.key = filename
#             if key.last_modified is None or time.localtime(modify_time) > time.strptime(key.last_modified, '%a, %d %b %Y %H:%M:%S %Z'):
#                 print filename
#                 fid = file(filename, 'r')
#                 key.set_contents_from_file(fid)
#                 key.set_acl('public-read')
#                 print 'file uploaded'

#   Read more: http://www.halotis.com/2011/03/04/django-media-on-amazon-s3-fabric-deploy-script/#ixzz1XkvzoZ3O