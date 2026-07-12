import re

import bpy


def bIsLeft(bone: bpy.types.Bone, check_name=False):
    return (
        (bone.head_local[0] > 0.001)
        and (
                re.search(
                    [
                        r"(?<![\S+\s+])L_(?!\s+)",
                        r"(?<![\S+\s+])L\.(?!\s+)",
                        r"(?<![\S+\s+])_L(?!\s+)",
                        r"(?<![\S+\s+])\.L(?!\s+)",
                        r"(?<![\S+\s+])LEFT_(?!\s+)",
                        r"(?<![\S+\s+])LEFT\.(?!\s+)",
                        r"(?<![\S+\s+])_LEFT(?!\s+)",
                        r"(?<![\S+\s+])\.LEFT(?!\s+)",
                        r"(?<![\S+\s+])LEFT(?!\s+)",
                        r"(?<!\s+)LEFT(?![\S+\s+])",
                    ],
                    bone.name,
                    re.IGNORECASE,
                )
                is not None
        )
        if check_name
        else True
    )


def bIsRight(bone: bpy.types.Bone, check_name=False):
    return (
        (bone.head_local[0] > 0.001)
        and (
                re.search(
                    [
                        r"(?<![\S+\s+])R_(?!\s+)",
                        r"(?<![\S+\s+])R\.(?!\s+)",
                        r"(?<![\S+\s+])_R(?!\s+)",
                        r"(?<![\S+\s+])\.R(?!\s+)",
                        r"(?<![\S+\s+])RIGHT_(?!\s+)",
                        r"(?<![\S+\s+])RIGHT\.(?!\s+)",
                        r"(?<![\S+\s+])_RIGHT(?!\s+)",
                        r"(?<![\S+\s+])\.RIGHT(?!\s+)",
                        r"(?<![\S+\s+])RIGHT(?!\s+)",
                        r"(?<!\s+)RIGHT(?![\S+\s+])",
                    ],
                    bone.name,
                    re.IGNORECASE,
                )
                != None
        )
        if check_name
        else True
    )
