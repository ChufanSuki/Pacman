from typing import Iterable, Union


class DcopInvalidFormatError(Exception):
    pass


def load_dcop_from_file(filenames: Union[str, Iterable[str]]):
    """
    load a dcop from one or several files

    Parameters
    ----------
    filenames: str or iterable of str
        The dcop can the given as a single file or as several files. When
        passing an iterable of file names, their content is concatenated
        before parsing. This can be useful when you want to define the
        agents in a separate file.

    Returns
    -------
    A DCOP object built by parsing the files

    """
