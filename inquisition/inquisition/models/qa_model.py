import whoosh.index
from whoosh.qparser import QueryParser, OrGroup, WildcardPlugin
from deeppavlov import build_model, configs
import argparse


def parse_args(args):
    """
    Returns arguments passed at the command line as a dict
    :param args: Command line arguments
    :return: args as a dict
    """
    parser = argparse.ArgumentParser(description='Create a whoosh index of text')
    parser.add_argument('-ip', '--index_path', help='Path where the index should be stored',
                        required=True, dest='index_path')
    parser.add_argument('-in', '--index_name', help='Name assigned to the index',
                        required=True, dest='index_name')
    parser.add_argument('-m', '--model_config', help='DeepPavlov model configuration to use',
                        default='squad.squad_bert', dest='model_selection')
    return vars(parser.parse_args(args))


class QAModel:
    def __init__(self, index_path, index_name, model_config):
        self._index_path = None
        self._index_name = None
        self._model_config = None
        self._model = None
        self._whoosh_index = None
        self._query_parser = None

        self.index_path = index_path
        self.index_name = index_name
        self.model_config = model_config

        self.load_model()
        self.load_index()
        self.create_and_prep_query_parser()

    @property
    def index_path(self):
        return self._index_path

    @index_path.setter
    def index_path(self, value):
        if type(value) == str:
            self._index_path = value
        else:
            ValueError('Index path must be a string')

    @property
    def index_name(self):
        return self._index_name

    @index_name.setter
    def index_name(self, value):
        if type(value) == str:
            self._index_name = value
        else:
            ValueError('Index name must be a string')

    @property
    def model_config(self):
        return self._model_config

    @model_config.setter
    def model_config(self, value):
        if type(value) == str:
            self._model_config = value
        else:
            ValueError('Model config must be a string')

    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, value):
        self._model = value

    @property
    def whoosh_index(self):
        return self._whoosh_index

    @whoosh_index.setter
    def whoosh_index(self, value):
        self._whoosh_index = value

    @property
    def query_parser(self):
        return self._query_parser

    @query_parser.setter
    def query_parser(self, value):
        self._query_parser = value

    def load_model(self):
        """
        Loads the model specified by model config
        """
        if self.model_config == 'squad.squad_bert':
            self.model = build_model(configs.squad.squad_bert, download=False)

    def load_index(self):
        """

        """
        self.whoosh_index = whoosh.index.open_dir(self.index_path,
                                                  indexname=self.index_name)

    def create_and_prep_query_parser(self):
        self.query_parser = QueryParser('text',
                                        schema=self.whoosh_index.schema,
                                        group=OrGroup)
        # Set up for natural language queries
        self.query_parser.remove_plugin_class(WildcardPlugin)

    def answer_question(self, input_query):
        """

        :param input_query:
        :return:
        """
        with self.whoosh_index.searcher() as searcher:
            parsed_query = self.query_parser.parse(input_query)

            search_results = searcher.search(parsed_query, limit=1)
            top_hit = [hit['text'] for hit in search_results][0]

            return self.model([top_hit], [input_query])
