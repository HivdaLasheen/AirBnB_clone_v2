from fabric import task
from datetime import datetime
import os

@task
def do_pack(c):
    """Create a .tgz archive from the contents of the web_static folder"""
    # Create the versions directory if it doesn't exist
    if not os.path.exists('versions'):
        os.makedirs('versions')

    # Generate the file name using the current timestamp
    now = datetime.now().strftime('%Y%m%d%H%M%S')
    archive_path = f'versions/web_static_{now}.tgz'

    # Create the .tgz archive using tar command
    result = c.local('tar -cvzf {} web_static'.format(archive_path))

    if result.failed:
        return None
    else:
        return archive_path
