import os


def get_instances(path, upper=False):
    all_files = os.listdir(path)

    # we don't want to make an enum for the __init__.py file, and we also don't
    # want to make an enum for the generic category that acts as an interface
    #   Note: the generic category folder ends with an 's', but the file doesn't
    excluded = ["__init__.py", f"{path[:-1]}.py"]

    # get the python files that aren't in the excluded file list
    py_files = list(
        filter(lambda f: f.endswith(".py") and f not in excluded, all_files)
    )

    # remove the .py extension and conver to upper case
    members = list(map(lambda f: f[:-3], py_files))

    if upper:
        members = list(map(lambda f: f.upper(), members))

    # put it into an easily usable format for Enum class initialization
    member_dict = {member: i for i, member in enumerate(members)}

    return member_dict
