from os import environ, pathsep


def add_path(path: str) -> None:
    """ Add specified path to the environment PATH variable

    :param path: path to add to PATH
    """
    environ['PATH'] = path + pathsep + environ['PATH']
