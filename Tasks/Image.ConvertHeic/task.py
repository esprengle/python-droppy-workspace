#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import os
try:
    import Image
except ImportError:
    from PIL import Image
import pyheif  # this requires the libheif library, eg. `brew install libheif`
import sys

sys.path.append(os.path.abspath(os.path.join(__file__, os.pardir, os.pardir, 'DropPy.Common')))
from file_tools import get_file_paths_from_directory


class Task(object):
    def __init__(self, input_dir, output_dir, **kwargs):
        # Get keyword arguments.
        extension = kwargs.get(str('extension'), 'jpg')

        # Process files and directories.
        for item_name in os.listdir(input_dir):
            item_path = os.path.join(input_dir, item_name)

            if os.path.isfile(item_path):
                self.convert_file(item_path, output_dir, extension)

            elif os.path.isdir(item_path):
                output_sub_dir = os.path.join(output_dir, item_name)
                os.makedirs(output_sub_dir)

                contained_files = get_file_paths_from_directory(item_path)
                for contained_file in contained_files:
                    self.convert_file(contained_file, output_sub_dir, extension)

    @staticmethod
    def convert_file(input_file, output_dir, output_extension):
        input_file_name, _ = os.path.splitext(os.path.basename(input_file))
        output_file = os.path.join(output_dir, input_file_name + '.' + output_extension)

        heif_image = pyheif.read_heif(input_file)
        input_image = Image.frombytes(mode=heif_image.mode, size=heif_image.size, data=heif_image.data)
        input_image.save(output_file)
