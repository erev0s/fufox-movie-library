from django_elasticsearch_dsl import Index, fields
from django_elasticsearch_dsl.documents import DocType
from elasticsearch_dsl import analyzer

from library.models import *


# Name of the Elasticsearch index
INDEX = Index('s_movies')

# See Elasticsearch Indices API reference for available settings
INDEX.settings(
    number_of_shards=1,
    number_of_replicas=1
)


html_strip = analyzer(
    'html_strip',
    tokenizer="standard",
    filter=["standard", "lowercase", "stop", "snowball"],
    char_filter=["html_strip"]
)


@INDEX.doc_type
class MovieDocument(DocType):
    """Movie Elasticsearch document."""

    id = fields.IntegerField(attr='id')

    prettyUrl = fields.TextField()

    title = fields.StringField(
        analyzer=html_strip,
        fields={
            'raw': fields.KeywordField(),
            'suggest': fields.CompletionField(),
        }
    )

    summary = fields.StringField(
        analyzer=html_strip,
        fields={
            'raw': fields.KeywordField(),
        }
    )

    people = fields.StringField(
        attr='people_indexing',
        analyzer=html_strip,
        fields={
            'raw': fields.KeywordField(multi=True),
            'suggest': fields.CompletionField(multi=True),
        },
        multi=True
    )

    genres = fields.StringField(
        attr='genres_indexing',
        analyzer=html_strip,
        fields={
            'raw': fields.KeywordField(multi=True),
            'suggest': fields.CompletionField(multi=True),
        },
        multi=True
    )

    score = fields.FloatField(attr='score')

    year = fields.FloatField(attr='year')

    class Django(object):
        """Meta options."""
        model = Movie  # The model associate with this DocType








# Name of the Elasticsearch index
sINDEX = Index('s_series')

# See Elasticsearch Indices API reference for available settings
sINDEX.settings(
    number_of_shards=1,
    number_of_replicas=1
)


@sINDEX.doc_type
class SeriesDocument(DocType):
    """Series Elasticsearch document."""

    id = fields.IntegerField(attr='id')

    prettyUrl = fields.TextField()

    title = fields.StringField(
        analyzer=html_strip,
        fields={
            'raw': fields.KeywordField(),
            'suggest': fields.CompletionField(),
        }
    )

    summary = fields.StringField(
        analyzer=html_strip,
        fields={
            'raw': fields.KeywordField(),
        }
    )

    people = fields.StringField(
        attr='people_indexing',
        analyzer=html_strip,
        fields={
            'raw': fields.KeywordField(multi=True),
            'suggest': fields.CompletionField(multi=True),
        },
        multi=True
    )

    genres = fields.StringField(
        attr='genres_indexing',
        analyzer=html_strip,
        fields={
            'raw': fields.KeywordField(multi=True),
            'suggest': fields.CompletionField(multi=True),
        },
        multi=True
    )

    score = fields.FloatField(attr='score')

    class Django(object):
        """Meta options."""
        model = Series  # The model associate with this DocType