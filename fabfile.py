from fabric.api import *
import os
import fabric.contrib.project as project

PROD = 'hawksworx.com'
DEST_PATH = '/home/sjl/webapps/slc/'
ROOT_PATH = os.path.abspath(os.path.dirname(__file__))
DEPLOY_PATH = os.path.join(ROOT_PATH, 'deploy')

def clean():
    local('rm -rf ./deploy')

def regen():
    clean()
    local('hyde gen')
    local('chmod -R 777 ./deploy')

def serve():
    local('hyde serve')

def reserve():
    regen()
    serve()


@hosts(PROD)
def publish():
    regen()
    project.rsync_project(
        remote_dir=DEST_PATH,
        local_dir=DEPLOY_PATH.rstrip('/') + '/',
        delete=True
    )