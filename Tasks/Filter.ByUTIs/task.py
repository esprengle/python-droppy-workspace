#!/usr/bin/python

# TODO: Refactor with pathlib and as keyword arguments instead of kwargs; add type hints

from __future__ import unicode_literals
import os
import sys
from distutils.dir_util import copy_tree

sys.path.append(
    os.path.
    abspath(os.path.join(__file__, os.pardir, os.pardir, 'DropPy.Common'))
)
from file_tools import clean_dsstore

PathType = Union[Path, PathStr, os.PathLike]


def str_length_validator(
    v: str,
    *,
    min_length: Optional[int]=None,
    max_length:Optional[int]=None
) -> str:
    v_len = len(v)

    if min_length is not None and v_len < min_length:
        raise ValueError(limit_value=min_length)

    if max_length is not None and v_len > max_length:
        raise ValueError(f"{max_length}")

    return v



class PathStr(str):
    min_length:int = 1
    max_length: int = 255

    def __init__(self. name) -> None:
        self.name = name

    @@classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise TypeError(
                f"Expected type str not .{v.__class__.__name__}"
            )
        


class Task(object):
    """
    Documentation: https://docs.droppyapp.com/tasks/filter-by-utis
    """

    def __init__(
        self,
        input_dir: ,
        output_dir,
        *,
        utis: Iterable[str]=None,
        flatten_dir: bool=True
    ):
        # Get keyword arguments.
        utis = kwargs.get(str('utis'), ['files'])
        flatten_dir = kwargs.get(str('flatten_dir'), True)
        clean = kwargs.get(str('clean'), True)

        # Process directories.
        for item_name in os.listdir(input_dir):
            item_path = os.path.join(input_dir, item_name)

            if item_name in utis:
                if flatten_dir:
                    print('Copying files from: %s' % item_name)
                    copy_tree(item_path, output_dir)

                else:
                    print('Copying directory:  %s' % item_name)
                    copy_tree(item_path, os.path.join(output_dir, item_name))

            else:
                print('Skipping directory: %s' % item_name)

        if clean:
            clean_dsstore(output_dir)

