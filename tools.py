import os
import yaml
import json

from color import Color
from variable import Variable


def get_yml_file(box_name, key=None):
    with open(box_name, 'r') as f:
        yml_file = yaml.load(f, Loader=yaml.FullLoader)

        if key:
            if key in yml_file:
                return yml_file[key]
            else:
                return KeyError
        else:
            return yml_file


def manage_config_file(mode, key, value=None):
    if not os.path.exists(Variable.box_path + 'config.json'):
        with open(Variable.box_path + 'config.json', 'w+') as file:
            data = {'data': {}}
            json.dump(data, file)
    else:
        with open(Variable.box_path + 'config.json', 'r') as file:
            data = json.load(file)

    with open(Variable.box_path + 'config.json', 'w') as file:
        if mode == 'create':
            if not key in data['data']:
                data['data'][key] = str(value)
                json.dump(data, file)
            else:
                json.dump(data, file)
                exit(Color.ERROR + "Key already exist." + Color.DEFAULT)
        elif mode == 'remove':
            if key in data['data']:
                del data['data'][key]
                json.dump(data, file)
            else:
                json.dump(data, file)
                exit(Color.ERROR + "Key doesn't exist." + Color.DEFAULT)
        elif mode == 'get':
            if key in data['data']:
                json.dump(data, file)
                return data['data'][key]
            else:
                json.dump(data, file)
                return False
        else:
            json.dump(data, file)
            return False


def umount_directory(path_env):
    os.system("umount " + path_env + "/proc")
    os.system("umount " + path_env + "/sys")
    os.system("umount " + path_env + "/dev")


def mount_directory(path_env):
    os.system("mount -t proc /proc " + path_env + "/proc")
    os.system("mount -t sysfs /sys " + path_env + "/sys")
    os.system("mount --bind /dev " + path_env + "/dev")


def prepare_box(path_env):
    os.system("cp /etc/hosts " + path_env + "/etc/hosts")
    os.system("cp /etc/resolv.conf " + path_env + "/etc/resolv.conf")


def chroot_box(path_env):
    os.chroot(path_env)
    os.chdir('/')
    os.system("chmod 777 /tmp")
    os.system("mknod -m 666 /dev/null c 1 3")
    os.system("mknod -m 666 /dev/zero c 1 5")
    os.system("chown root:root /dev/null /dev/zero")
    os.system("apt-get update && apt-get upgrade")


def unchroot(root):
    # disable chroot
    os.fchdir(root)
    os.chroot(".")
    os.close(root)


def copy_base(base, env):
    os.system("cp -r " + base + "* " + env + '/')


def install_package(key, repo, req):
    os.system("apt-get install -y gnupg2 curl systemd")
    os.system("curl -fsSL " + key + " | apt-key add -")
    os.system("echo '" + repo + "' | tee /etc/apt/sources.list.d/" + req + ".list")
    os.system("apt update")
    os.system("apt install -y " + req)
    os.system("mkdir -p /data/db")


def create_user(username, uid):
    os.system("useradd -u " + str(uid) + " -p $(openssl passwd -1 password) " + username)
    os.system("adduser " + username + " sudo")


def switch_user(username, command):
    # Next line can return an exitCode 100, because user isn't in root
    #os.system("runuser -l " + username + " -c '" + command + "'")

    # Uncomment this line if the first doesn't work > start application in root
    os.system(command)
