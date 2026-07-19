import os
import re
import sys
from pprint import pprint
from tempfile import gettempdir

import bpy

enc = sys.getfilesystemencoding()


def abspath(path):
    return os.path.abspath(bpy.path.abspath(path))


def quotepath(path):
    if " " in path:
        path = '"%s"' % (path)
    return path


def add_path_to_recent_files(path):
    try:
        recent_path = bpy.utils.user_resource("CONFIG", path="recent-files.txt")
        with open(recent_path, "r+", encoding=enc) as f:
            content = f.read()
            f.seek(0, 0)
            f.write(path.rstrip("\r\n") + "\n" + content)

    except (IOError, OSError, FileNotFoundError):
        pass


def get_next_files(filepath, next=True, debug=False):
    current_dir = os.path.dirname(filepath)
    current_file = os.path.basename(filepath)

    blend_files = sorted(
        [
            f
            for f in os.listdir(current_dir)
            if os.path.splitext(f)[1].startswith(".blend")
        ]
    )

    current_idx = blend_files.index(current_file)

    if debug:
        print()
        print("files:")

        for idx, file in enumerate(blend_files):
            if idx == current_idx:
                print(" >", file)
            else:
                print("  ", file)

    next_file = None
    next_backup_file = None

    if next:
        next_blend_files = blend_files[current_idx + 1:]

    else:
        next_blend_files = blend_files[:current_idx]
        next_blend_files.reverse()

    if debug:
        print()
        nextstr = "next" if next else "previous"
        print(f"{nextstr} files:")

    for file in next_blend_files:
        if debug:
            print(" ", file)

        ext = os.path.splitext(file)[1]

        if next_file is None and ext == ".blend":
            next_file = file

        if next_backup_file is None and ext.startswith(".blend"):
            next_backup_file = file

        if next_file and next_backup_file:
            break

    if debug:
        print()
        print(f"{nextstr} file:", next_file)
        print(f"{nextstr} file (incl. backups):", next_backup_file)

    return current_dir, next_file, next_backup_file


def get_temp_dir(context):
    temp_dir = context.preferences.filepaths.temporary_directory

    if not temp_dir:
        temp_dir = gettempdir()

    return temp_dir


def open_folder(path):
    import platform
    import subprocess

    if platform.system() == "Windows":
        os.startfile(path)
    elif platform.system() == "Darwin":
        subprocess.Popen(["open", path])
    else:
        os.system(
            'xdg-open "%s" %s &' % (path, "> /dev/null 2> /dev/null")
        )  # > sends stdout,  2> sends stderr


def makedir(pathstring):
    if not os.path.exists(pathstring):
        os.makedirs(pathstring)
    return pathstring


def printd(d, name=""):
    print(f"\n{name}")
    pprint(d, sort_dicts=False)


def get_incremented_paths(currentblend):
    path = os.path.dirname(currentblend)
    filename = os.path.basename(currentblend)

    filenameRegex = re.compile(r"(.+)\.blend\d*$")

    mo = filenameRegex.match(filename)

    if mo:
        name = mo.group(1)
        numberendRegex = re.compile(r"(.*?)(\d+)$")

        mo = numberendRegex.match(name)

        if mo:
            basename = mo.group(1)
            numberstr = mo.group(2)
        else:
            basename = name + "_"
            numberstr = "000"

        number = int(numberstr)

        incr = number + 1
        incrstr = str(incr).zfill(len(numberstr))

        incrname = basename + incrstr + ".blend"

        return os.path.join(path, incrname), os.path.join(path, name + "_01.blend")
