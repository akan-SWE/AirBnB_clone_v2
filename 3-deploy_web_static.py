#!/usr/bin/python3
"""
Module: 2-do_deploy_web_static.py

This module contains Fabric scripts that automate the deployment
of the 'web_static' directory to web servers.

Functions:
    do_deploy: Distributes an archive to the web servers.
"""
import os
from fabric.api import put, run, env, local


env.hosts = ['54.237.96.155', '54.90.51.255']
env.user = 'ubuntu'


def do_pack():
    """Generates a .tgz archive from the content of the web_static."""
    from datetime import datetime

    # Ensure directory exists.
    os.makedirs('versions', exist_ok=True)
    # Get current datetime to create a unique archive name.
    archive = f'web_static_{datetime.now().strftime("%Y%m%d%H%M%S")}.tgz'

    archive_path = f'versions/{archive}'
    print(f'Packing web_static to {archive_path}')

    local(f'tar -czvf {archive_path} web_static')  # create web_static archive

    file_size = os.path.getsize(archive_path)
    print(f'web_static packed: {archive_path} -> {file_size}Bytes')

    return os.path.abspath(archive_path)


def do_deploy(archive_path):
    """
    Distributes an archive to the web servers.

    Args:
        archive_path (str): The path to the archive to be deployed.

    Returns:
        bool: True if the deployment was successful, False otherwise.
    """
    # Check if the archive file exists
    if not os.path.exists(archive_path):
        return False

    archive_name = os.path.basename(archive_path)
    current_path = '/data/web_static/current'
    tmp_archive_path = f'/tmp/{archive_name}'
    destination_dir = f"/data/web_static/releases/{archive_name.split('.')[0]}"

    try:
        # Upload the archive to the temporary directory on the server
        put(archive_path, tmp_archive_path)
        # Create the destination directory
        run(f'mkdir -p {destination_dir}')
        # Uncompress the archive to the destination directory
        run(f'tar -xzf {tmp_archive_path} -C {destination_dir}')
        # Remove the uploaded archive from the temporary directory
        run(f'rm {tmp_archive_path}')
        # Move uncompressed web_static contents to destination.
        run(f'mv {destination_dir}/web_static/* {destination_dir}')
        # Remove the now-empty web_static directory
        run(f'rm -rf {destination_dir}/web_static')
        # Remove the current symbolic link
        run(f'rm -rf {current_path}')
        # Create a new symbolic link to the destination directory
        run(f'ln -s {destination_dir} {current_path}')
        # Print a message indicating a successful deployment
        print('New version deployed!')
        return True
    except Exception as e:
        print("Error: ", e)
        return False


def deploy():
    """
    Packs and deploys the web_static content to web servers.

    Returns:
        bool: True if deployment was successful, False otherwise.
    """
    try:
        archive_path = do_pack()
    except Exception as e:
        print("Error: ", e)
        return False

    return do_deploy(archive_path)


def delete():
    """
    """
    run("rm -r /data/web_static/releases/web_static_*")
    run("rm -r /data/web_static/current")
