# -*- coding: utf-8 -*-
import os
import sys
import typing
from contextlib import contextmanager


def add_path(path: str) -> None:
    """ Add specified path to the environment PATH variable

    :param path: path to add to PATH
    """
    os.environ['PATH'] = path + os.pathsep + os.environ['PATH']
