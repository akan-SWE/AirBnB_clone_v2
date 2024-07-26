#!/usr/bin/python3
"""
Module: 1-pack_web_static.py

This module contains a Fabric script that automates the archiving of
the 'web_static' directory.
"""
import os
from fabric.api import *


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
