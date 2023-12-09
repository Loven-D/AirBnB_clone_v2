#!/usr/bin/python3
"""A module for web application deployment with Fabric."""
import os
from datetime import datetime
from fabric import task, Connection, Config

env = Config(overrides={'sudo': {'password': 'your_sudo_password'}}).from_envvars()

@task
def do_pack(c):
    """Archives the static files."""
    if not os.path.isdir("versions"):
        os.mkdir("versions")
    cur_time = datetime.now()
    output = "versions/web_static_{}{}{}{}{}{}.tgz".format(
        cur_time.year,
        cur_time.month,
        cur_time.day,
        cur_time.hour,
        cur_time.minute,
        cur_time.second
    )
    try:
        print("Packing web_static to {}".format(output))
        c.local("tar -cvzf {} web_static".format(output))
        archize_size = os.stat(output).st_size
        print("web_static packed: {} -> {} Bytes".format(output, archize_size))
    except Exception:
        output = None
    return output

@task
def do_deploy(c, archive_path):
    """Deploys the static files to the host servers.
    Args:
        archive_path (str): The path to the archived static files.
    """
    if not os.path.exists(archive_path):
        return False
    file_name = os.path.basename(archive_path)
    folder_name = file_name.replace(".tgz", "")
    folder_path = "/data/web_static/releases/{}/".format(folder_name)
    success = False
    try:
        c.put(archive_path, "/tmp/{}".format(file_name))
        c.run("mkdir -p {}".format(folder_path))
        c.run("tar -xzf /tmp/{} -C {}".format(file_name, folder_path))
        c.run("rm -rf /tmp/{}".format(file_name))
        c.run("mv {}web_static/* {}".format(folder_path, folder_path))
        c.run("rm -rf {}web_static".format(folder_path))
        c.run("rm -rf /data/web_static/current")
        c.run("ln -s {} /data/web_static/current".format(folder_path))
        print('New version deployed!')
        success = True
    except Exception:
        success = False
    return success
