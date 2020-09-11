import inquisition as inq
from pathlib import Path
from tqdm import tqdm
import whoosh.index
import argparse
import sys


def parse_args(args):
    """
    Returns arguments passed at the command line as a dict
    :param args: Command line arguments
    :return: args as a dict
    """
    parser = argparse.ArgumentParser(description='Create a whoosh index of text')
    parser.add_argument('-t', '--text_path', help="Path where text to be indexed is stored.",
                        required=True, dest='text_path')
    parser.add_argument('-a', '--analyzer_type', help='Whoosh analyzer type to use for index',
                        required=False, default='Stemming', dest='analyzer_type')
    parser.add_argument('-ip', '--index_path', help='Path where the index should be stored',
                        required=True, dest='index_path')
    parser.add_argument('-in', '--index_name', help='Name assigned to the index',
                        required=True, dest='index_name')
    return vars(parser.parse_args(args))


def build_index():
    args = parse_args(sys.argv[1:])

    text_files = inq.get_file_names(args['text_path'])
    schema = inq.create_title_and_text_schema(analyzer=args['analyzer_type'])

    idx = whoosh.index.create_in(args['index_path'],
                                 schema=schema,
                                 indexname=args['index_name'])

    writer = idx.writer()

    for file in tqdm(text_files):
        path = Path(file)

        chapter_title = path.stem
        with path.open('r') as f:
            chapter_text = f.read()

        writer.update_document(
            title=chapter_title,
            text=chapter_text,
        )

    writer.commit()

    return 1


if __name__ == '__main__':
    build_index()


"""
# Get the file list
text_path = '../tests/artifacts/data/king_arthur/*.txt'
analyzer_type = 'Stemming'
index_path = '/Users/saracollins/PycharmProjects/inquisition/inquisition/tests/artifacts/data/king_arthur_idx'
index_name = 'arthur'
"""
