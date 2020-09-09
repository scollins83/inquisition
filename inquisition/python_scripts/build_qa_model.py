import whoosh.index
from whoosh.qparser import QueryParser, OrGroup, WildcardPlugin
from deeppavlov import build_model, configs

# Instantiate the Q&A model
bert_squad_model = build_model(configs.squad.squad_bert, download=False)

# Load the index
whoosh_idx = whoosh.index.open_dir('../tests/artifacts/data/king_arthur_idx',
                                   indexname='arthur')

# Only search in the text field.
query_parser = QueryParser('text',
                           schema=whoosh_idx.schema,
                           group=OrGroup)

# Set up for natural language queries
query_parser.remove_plugin_class(WildcardPlugin)

# Search the index and grab the top hit
with whoosh_idx.searcher() as searcher:
    while True:
        query = input('Query ("exit" to quit): ')
        if query == 'exit':
            break

        parsed_query = query_parser.parse(query)

        search_results = searcher.search(parsed_query, limit=1)
        top_hit = [hit['text'] for hit in search_results][0]

        print(bert_squad_model([top_hit], [query]))
