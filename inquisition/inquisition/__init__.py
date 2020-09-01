"""Top-level package for inquisition."""

__author__ = """Sara Collins"""
__email__ = 'saracollins0508@gmail.com'
__version__ = '0.0.1-RC-1'

import glob
from whoosh.fields import Schema, TEXT, ID
from whoosh.analysis import StemmingAnalyzer


def get_file_names(file_path):
    """
    Returns a list of filenames in a given directory
    :param file_path: Directory from which to get file names.
    :return: List of file names
    """
    return glob.glob(file_path)


def create_title_and_text_schema(analyzer='Stemming'):
    """
    Returns a blank two field whoosh schema, one for a
    chapter title, one for chapter text.
    :param analyzer: Which whoosh analyzer to use.
    :return: Blank whoosh schema
    """
    if analyzer == 'Stemming':
        schema = Schema(
            title=ID(stored=True, unique=True),
            text=TEXT(stored=True, analyzer=StemmingAnalyzer()),
        )
        return schema


if __name__ == '__main__':
    pass
