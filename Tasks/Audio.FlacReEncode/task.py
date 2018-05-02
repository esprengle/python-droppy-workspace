#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import os
import subprocess
import sys

sys.path.append(os.path.abspath(os.path.join(__file__, os.pardir, os.pardir, 'DropPy.Common')))
from file_tools import get_file_paths_from_directory
from shell_tools import sanitize_file_path_for_shell


def get_tag(metaflac_exe, file_path, key):
    command = [metaflac_exe, file_path, '--show-tag=%s' % key]
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, _ = p.communicate()

    return out.decode(encoding='utf-8')


def normalize_tag(key_and_value):
    # Cut off the "key=" part of the combined "key=value" string.
    value = key_and_value[key_and_value.find('=') + 1:]

    # No spaces at the beginning and no linebreaks anywhere.
    value = value.strip()

    # Reliably capitalize each single word. Just using .title() doesn't work well for single letter words.
    value = ' '.join(word.capitalize() for word in value.split())

    # Additional step needed to capitalize the first word inside brackets.
    for bracket_type in ['(', '[', '{']:
        if bracket_type in value:
            value = capitalize_after_char(value, bracket_type)

    return value


def capitalize_after_char(string, char):
    tmp = []
    for word in string.split(char):
        if len(word) > 0:
            tmp.append(word[0].upper() + word[1:])
        else:
            tmp.append(word[1:])
    return char.join(tmp)


class Task(object):
    """
    Documentation: https://docs.droppyapp.com/tasks/audio-flac-re-encode
    """
    def __init__(self, input_dir, output_dir, **kwargs):
        # Get keyword arguments.
        flac_exe = kwargs.get(str('flac_executable'), '/usr/local/bin/flac')
        metaflac_exe = kwargs.get(str('metaflac_executable'), '/usr/local/bin/metaflac')
        copy_tags = kwargs.get(str('copy_tags'), False)
        compression = kwargs.get(str('compression'), '--compression-level-8')

        # Check for required external executables.
        if not os.path.isfile(flac_exe):
            sys.exit('flac not found at "%s"' % flac_exe)
        if not os.path.isfile(metaflac_exe):
            sys.exit('metaflac not found at "%s"' % metaflac_exe)

        # Process files and directories.
        for item_name in os.listdir(input_dir):
            item_path = os.path.join(input_dir, item_name)

            if os.path.isfile(item_path):
                self.reencode_file(item_path, output_dir, copy_tags, flac_exe, metaflac_exe, compression)

            elif os.path.isdir(item_path):
                output_sub_dir = os.path.join(output_dir, item_name)

                os.makedirs(output_sub_dir)
                contained_files = get_file_paths_from_directory(item_path)

                for contained_file in contained_files:
                    self.reencode_file(contained_file, output_sub_dir, copy_tags, flac_exe, metaflac_exe, compression)

    @staticmethod
    def reencode_file(input_file, output_dir, copy_tags, flac_exe, metaflac_exe, compression):
        output_file_name, _ = os.path.splitext(os.path.basename(input_file))
        output_wav_file = os.path.join(output_dir, output_file_name + '.wav')
        output_flac_file = os.path.join(output_dir, output_file_name + '.flac')

        # Decoding flac to wav leads to the tags getting deleted.
        # Get all relevant tags from the source file beforehand if they should be copied.
        if copy_tags:
            tag_artist = normalize_tag(get_tag(metaflac_exe, input_file, 'ARTIST'))
            tag_title = normalize_tag(get_tag(metaflac_exe, input_file, 'TITLE'))
            tag_track_number = normalize_tag(get_tag(metaflac_exe, input_file, 'TRACKNUMBER'))
            tag_track_total = normalize_tag(get_tag(metaflac_exe, input_file, 'TRACKTOTAL'))
            tag_album = normalize_tag(get_tag(metaflac_exe, input_file, 'ALBUM'))
            tag_date = normalize_tag(get_tag(metaflac_exe, input_file, 'DATE'))
            tag_genre = normalize_tag(get_tag(metaflac_exe, input_file, 'GENRE'))
            tag_disk = normalize_tag(get_tag(metaflac_exe, input_file, 'DISCNUMBER'))
            tag_disk_total = normalize_tag(get_tag(metaflac_exe, input_file, 'DISCTOTAL'))
        else:
            tag_artist = ''
            tag_title = ''
            tag_track_number = ''
            tag_track_total = ''
            tag_album = ''
            tag_date = ''
            tag_genre = ''
            tag_disk = ''
            tag_disk_total = ''

        # Decode the flac file into a temporary wav file.
        decode_command = '%s -d "%s" -o "%s"' % (flac_exe,
                                                 sanitize_file_path_for_shell(input_file),
                                                 sanitize_file_path_for_shell(output_wav_file))

        print('Calling: %s' % decode_command)

        exit_code = subprocess.call(decode_command, shell=True)
        if exit_code > 0:
            sys.exit(exit_code)

        # Encode the wav file into flac, passing the tags.
        encode_command = '%s ' % flac_exe
        encode_command += '"%s" ' % sanitize_file_path_for_shell(output_wav_file)
        encode_command += '%s ' % compression
        encode_command += '-o "%s" ' % sanitize_file_path_for_shell(output_flac_file)
        if copy_tags:
            encode_command += '--tag=ARTIST="%s" ' % tag_artist
            encode_command += '--tag=TITLE="%s" ' % tag_title
            encode_command += '--tag=TRACKNUMBER="%s" ' % tag_track_number
            encode_command += '--tag=TRACKTOTAL="%s" ' % tag_track_total
            encode_command += '--tag=ALBUM="%s" ' % tag_album
            encode_command += '--tag=DATE="%s" ' % tag_date
            encode_command += '--tag=GENRE="%s" ' % tag_genre
            encode_command += '--tag=DISCNUMBER="%s" ' % tag_disk
            encode_command += '--tag=DISCTOTAL="%s" ' % tag_disk_total

        print('Calling: %s' % encode_command)

        exit_code = subprocess.call(encode_command, shell=True)
        if exit_code > 0:
            sys.exit(exit_code)

        # Delete the temporary wav file.
        os.remove(output_wav_file)
