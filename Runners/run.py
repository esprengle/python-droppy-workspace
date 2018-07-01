#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import argparse
import importlib
import json
import os
import six
import sys
import traceback


TASK_SUBFOLDER_IN_WORKSPACE = 'Tasks'
WORKFLOW_SUBFOLDER_IN_WORKSPACE = 'Workflows'
TASK_PYTHON_FILE_NO_EXT = 'task'
TASK_CLASS_NAME = 'Task'
EXIT_ON_SUCCESS = True


class Run(object):
    def __init__(self, workspace_path, workflow_name, input_path, output_path):
        workflow_dict = self.read_workflow_json(workspace_path, workflow_name)
        task_name, kwargs_dict = self.get_task_info(output_path, workflow_dict)
        self.instantiate_and_execute(workspace_path, task_name, input_path, output_path, kwargs_dict)

    @staticmethod
    def read_workflow_json(workspace_path, workflow_name):
        workflow_path = os.path.join(workspace_path, WORKFLOW_SUBFOLDER_IN_WORKSPACE, workflow_name)
        with open(workflow_path, str('r')) as file_handler:
            workflow_dict = json.loads(file_handler.read())
        return workflow_dict

    @classmethod
    def get_task_info(cls, output_path, workflow_dict):
        task_number = int(os.path.basename(output_path))
        task_name = workflow_dict['queue'][task_number - 1]['task']
        if 'kwargs' in workflow_dict['queue'][task_number - 1]:
            kwargs_dict = workflow_dict['queue'][task_number - 1]['kwargs']
        else:
            kwargs_dict = {}
        return task_name, kwargs_dict

    @staticmethod
    def get_task_count(workflow_dict):
        return len(workflow_dict['queue'])

    @staticmethod
    def instantiate_and_execute(workspace_path, task_name, input_path, output_path, kwargs_dict):
        try:
            task_dir = os.path.join(workspace_path, TASK_SUBFOLDER_IN_WORKSPACE, task_name)
            sys.path.insert(0, task_dir)
            task_module = importlib.import_module(TASK_PYTHON_FILE_NO_EXT)
            task_class = getattr(task_module, TASK_CLASS_NAME)
            task_class(input_path, output_path, **kwargs_dict)
            if EXIT_ON_SUCCESS:
                sys.exit(0)
            else:
                sys.modules.pop(TASK_PYTHON_FILE_NO_EXT)
        except Exception as err:
            print(err)
            traceback.print_exc()
            sys.exit(1)


def commandline_type(byte_string, encoding=sys.stdin.encoding):
    # Source: https://stackoverflow.com/a/33812744
    if six.PY2:
        unicode_string = byte_string.decode(encoding)
    else:  # if six.PY3:
        unicode_string = str(byte_string)
    return unicode_string


def parse_arguments():
    parser = argparse.ArgumentParser()
    required_named = parser.add_argument_group('required named arguments')
    required_named.add_argument('-w', '--workspace',
                                help='Absolute path to DropPy workspace',
                                action='store',
                                type=commandline_type,
                                required=True)
    required_named.add_argument('-j', '--json',
                                help='File name of selected Workflow json file',
                                action='store',
                                type=commandline_type,
                                required=True)
    required_named.add_argument('-i', '--input',
                                help='Absolute path to the input directory',
                                action='store',
                                type=commandline_type,
                                required=True)
    required_named.add_argument('-o', '--output',
                                help='Absolute path to the output directory',
                                action='store',
                                type=commandline_type,
                                required=True)
    parser.add_argument('-v', '--version',
                        help='Display version info and exit',
                        action='store_true')
    parser.add_argument('-a', '--all',
                        help='Execute all Tasks of the Workflow sequentially',
                        action='store_true')
    return parser.parse_args()


def print_version():
    print('Version 3.0, 2018-05-04')
    sys.exit(0)


if __name__ == '__main__':
    args = parse_arguments()
    if args.version:
        print_version()
    elif args.all:
        if os.path.basename(args.input) != "0":
            print('Error: For the "all" option to work the input directory has to be named "0".')
            print('       Your input directory is named "%s".' % os.path.basename(args.input))
            sys.exit(1)

        workflow_json = Run.read_workflow_json(workspace_path=args.workspace,
                                               workflow_name=args.json)
        number_of_tasks = Run.get_task_count(workflow_json)
        if number_of_tasks < 1:
            print('Error: There are 0 Tasks in your Workflow.')
            sys.exit(1)

        in_out_par_dir = os.path.abspath(os.path.join(args.input, os.pardir))
        EXIT_ON_SUCCESS = False

        for i in range(0, number_of_tasks):
            input_dir = os.path.join(in_out_par_dir, str(i))
            if not os.path.isdir(input_dir):
                os.makedirs(input_dir)
            output_dir = os.path.join(in_out_par_dir, str(i + 1))
            if not os.path.isdir(output_dir):
                os.makedirs(output_dir)
            r = Run(args.workspace, args.json, input_dir, output_dir)
    else:
        r = Run(args.workspace, args.json, args.input, args.output)
