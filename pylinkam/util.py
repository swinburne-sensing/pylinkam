import os
import sys
import typing
from contextlib import contextmanager


def add_path(path: str) -> None:
    """ Add specified path to the environment PATH variable

    :param path: path to add to PATH
    """
    os.environ['PATH'] = path + os.pathsep + os.environ['PATH']


@contextmanager
def supress_stdout(dest_path: str = os.devnull) -> typing.Generator[None, None, None]:
    stdout_fileno = sys.stdout.fileno()

    def _redirect_stdout(dest: typing.IO) -> None:
        # Close original handle
        sys.stdout.close()

        # Duplicate handle
        os.dup2(dest.fileno(), stdout_fileno)

        sys.stdout = os.fdopen(stdout_fileno, 'w')

    with os.fdopen(os.dup(stdout_fileno), 'w') as stdout_file:
        try:
            with open(dest_path, 'w') as dest_file:
                _redirect_stdout(dest_file)

            yield
        finally:
            # Restore original stdout
            _redirect_stdout(stdout_file)
