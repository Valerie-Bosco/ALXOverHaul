import os
import pathlib
import shutil
import stat
from os import sep as os_separator


def main():
    zip_addon()


def get_addon_version(bl_info: dict) -> list[int] | None:
    if "version" in bl_info.keys():
        return bl_info.get("version")
    return None


def remove_readonly(func, path, _):
    os.chmod(path, stat.S_IWRITE)
    func(path)


def zip_addon():
    path = pathlib.Path(
        "".join(
            [
                folder if folder[-1] == os_separator else f"{folder}{os_separator}"
                for folder in pathlib.Path(__file__).parts[:-1]
            ]
        )
    )

    parent_path = path
    folder_name = path.name

    if parent_path.is_dir():
        zip_source_path = pathlib.Path.joinpath(parent_path, folder_name)
        zip_target_path = parent_path.joinpath(f"{folder_name}")
        zip_work_path = parent_path.joinpath("temp")

        shutil.copytree(
            src=zip_source_path,
            symlinks=False,
            ignore=shutil.ignore_patterns("__pycache__"),
            dst=parent_path.joinpath("temp", folder_name),
        )
        shutil.make_archive(
            base_name=str(zip_target_path), format="zip", root_dir=zip_work_path
        )
        shutil.rmtree(path=zip_work_path, onexc=remove_readonly)

    else:
        raise ValueError(f"Parent_Path is not a directory: {parent_path}")


if __name__ == "__main__":
    main()
