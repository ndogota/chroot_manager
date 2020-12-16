import os


class Variable:
	root_path = os.open("/", os.O_RDONLY)
	box_path = "/var/lib/box/"
	base_path = box_path + "base/"
	env_path = box_path + "env/"
