import os
import shutil
import tools

from color import Color
from variable import Variable


def create_env(yml_file):
    if os.path.exists(Variable.env_path + yml_file['name']):
        exit(Color.ERROR + "Environment already exist." + Color.DEFAULT)
    else:
        init_env(yml_file)
        print(Color.GREEN + "Environment created successfully " + Color.BOLD + Color.BLUE + yml_file[
            'name'] + Color.DEFAULT + Color.GREEN + '.' + Color.DEFAULT)


def remove_env(name_env):
    if os.path.exists(Variable.env_path + name_env):
        shutil.rmtree(Variable.env_path + name_env)
        tools.manage_config_file('remove', name_env)
        tools.manage_config_file('remove', name_env + "-user")
        print(
            Color.GREEN + "Environment removed successfully " + Color.BOLD + Color.BLUE + name_env + Color.DEFAULT + Color.GREEN + '.' + Color.DEFAULT)
    else:
        print(Color.ERROR + "Sorry this environment doesn't exist :/" + Color.DEFAULT)


def init_env(yml_file):
    name_env = yml_file['name']
    key_env = yml_file['repositories'][0]['key']
    repo_env = yml_file['repositories'][1]['repository']
    req_env = yml_file['requirements'][0]
    user_env = yml_file['user'] if "user" in yml_file else "user-box"

    os.mkdir(Variable.env_path + name_env)
    tools.copy_base(Variable.base_path, Variable.env_path + name_env)
    tools.prepare_box(Variable.env_path + name_env)
    tools.mount_directory(Variable.env_path + name_env)
    tools.chroot_box(Variable.env_path + name_env)
    tools.install_package(key_env, repo_env, req_env)
    tools.create_user(user_env, 4242)
    tools.unchroot(Variable.root_path)
    tools.umount_directory(Variable.env_path + name_env)
    tools.manage_config_file('create', name_env, yml_file['run'])
    tools.manage_config_file('create', name_env + "-user", user_env)


def build_box_process(box_name):
    if os.path.exists(box_name):
            print("Building environment...")
            create_env(tools.get_yml_file(box_name))
    else:
        exit(Color.ERROR + "The YAML you specify doesn't exit" + Color.DEFAULT)


def run_box_process(box_name):
    if os.path.exists(Variable.env_path + box_name):
            print("Run environment")
            run_command = tools.manage_config_file('get', box_name)
            user_env = tools.manage_config_file('get', box_name + "-user") if tools.manage_config_file('get', box_name + "-user") else "user-box"

            tools.prepare_box(Variable.env_path + box_name)
            tools.mount_directory(Variable.env_path + box_name)
            tools.chroot_box(Variable.env_path + box_name)
            tools.switch_user(user_env, run_command)
            tools.unchroot(Variable.root_path)
            tools.umount_directory(Variable.env_path + box_name)
    else:
        exit(Color.ERROR + "The name you specify doesn't exit" + Color.DEFAULT)