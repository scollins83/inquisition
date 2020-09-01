import inquisition as inq
from pathlib import Path
from tqdm import tqdm
import whoosh.index

# Get the file list
text_files = inq.get_file_names('../tests/artifacts/data/king_arthur/*.txt')

# Create the blank schema
schema = inq.create_title_and_text_schema(analyzer='Stemming')

# Create the index
idx = whoosh.index.create_in('/Users/saracollins/PycharmProjects/inquisition/inquisition/tests/artifacts/data/king_arthur_idx',
                             schema=schema,
                             indexname='arthur')

writer = idx.writer()

for file in tqdm(text_files):
    path = Path(file)

    # Read in the info to be indexed
    chapter_title = path.stem
    with path.open('r') as f:
        chapter_text = f.read()

    # Add info to index
    writer.update_document(
        title=chapter_title,
        text=chapter_text,
    )

# Commit the index build
writer.commit()
