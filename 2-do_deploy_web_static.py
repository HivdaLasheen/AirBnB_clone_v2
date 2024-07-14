#!/usr/bin/env bash
from fabric import task
import os
from datetime import datetime

# Define your web server IP addresses here
env.hosts = ['<IP web-01>', '<IP web-02>']
# Define your SSH key and username here
env.key_filename = ['/path/to/your/ssh/key']
env.user = 'ubuntu'

@task
def do_deploy(c, archive_path):
    """Deploy archive to web servers"""
    if not os.path.exists(archive_path):
        return False

    try:
        # Upload the archive to /tmp/ directory on the server
        archive_name = os.path.basename(archive_path)
        tmp_path = '/tmp/{}'.format(archive_name)
        c.put(archive_path, tmp_path)

        # Create directory to uncompress the archive
        archive_no_ext = archive_name.replace('.tgz', '').replace('.tar.gz', '')
        release_path = '/data/web_static/releases/{}/'.format(archive_no_ext)
        c.run('mkdir -p {}'.format(release_path))

        # Uncompress the archive into the release path
        c.run('tar -xzf {} -C {}'.format(tmp_path, release_path))

        # Remove the uploaded archive from /tmp/
        c.run('rm {}'.format(tmp_path))

        # Move contents from extracted folder to release path
        c.run('mv {}web_static/* {}'.format(release_path, release_path))

        # Remove the empty web_static folder
        c.run('rm -rf {}web_static'.format(release_path))

        # Delete the symbolic link /data/web_static/current
        current_path = '/data/web_static/current'
        c.run('rm -rf {}'.format(current_path))

        # Create new symbolic link /data/web_static/current linked to the new version
        c.run('ln -s {} {}'.format(release_path, current_path))

        print('New version deployed!')
        return True

    except Exception as e:
        print(e)
        return False

