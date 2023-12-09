#!/usr/bin/python3
"""
Fabric script that generates a .tgz archive from the contents of the web_static
folder of your AirBnB Clone repo, using the function do_pack.
"""

from fabric.api import local
from datetime import datetime


def do_pack():
    """
    Creates a compressed archive of the web_static folder.

    Returns:
        str: Path to the created archive, None on failure.
    """
    try:
        # Create the 'versions' folder if it doesn't exist
        local("mkdir -p versions")

        # Generate the archive filename (web_static_<year><month><day><hour><minute><second>.tgz)
        now = datetime.utcnow()
        archive_name = "web_static_{}.tgz".format(
            now.strftime("%Y%m%d%H%M%S"))

        # Create the compressed archive
        local("tar -cvzf versions/{} web_static".format(archive_name))

        # Return the path to the created archive
        return "versions/{}".format(archive_name)

    except Exception as e:
        return None
