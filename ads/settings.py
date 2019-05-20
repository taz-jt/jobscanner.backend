import os

# Elasticsearch settings
ES_HOST = os.getenv("ES_HOST", "localhost")
ES_PORT = os.getenv("ES_PORT", 9200)
ES_USER = os.getenv("ES_USER")
ES_PWD = os.getenv("ES_PWD", "aPassword")
ES_AURANEST = os.getenv("ES_AURANEST", "anIndex")

# Flask-Restplus settings
RESTPLUS_SWAGGER_UI_DOC_EXPANSION = 'list'
RESTPLUS_VALIDATE = False
RESTPLUS_MASK_SWAGGER = False
RESTPLUS_ERROR_404_HELP = False
RESTPLUS_BUNDLE_ERRORS = True

# Query parameters
PLACE = 'place'
OFFSET = 'offset'
LIMIT = 'limit'
STATISTICS = 'stats'
STAT_LMT = 'stats.limit'
MAX_OFFSET = 2000
MAX_LIMIT = 100
FREETEXT_QUERY = 'q'
TYPEAHEAD_QUERY = 'typehead'
FREETEXT_FIELDS = 'qfields'
SORT = 'sort'
PUBLISHED_BEFORE = 'published-before'
PUBLISHED_AFTER = 'published-after'
EXPERIENCE_REQUIRED = 'experience'
PARTTIME_MIN = 'parttime.min'
PARTTIME_MAX = 'parttime.max'
LONGITUDE = 'longitude'
LATITUDE = 'latitude'
POSITION = 'position'
POSITION_RADIUS = 'position.radius'
DEFAULT_POSITION_RADIUS = 5
EMPLOYER = 'employer'

# For all ads
SHOW_EXPIRED = 'show-expired'

auranest_sort_options = {
    'relevance': "_score",
    'pubdate-desc': {"source.firstSeenAt": "desc"},
    'pubdate-asc':  {"source.firstSeenAt": "asc"},
    'applydate-desc':  {"application.deadline": "desc"},
    'applydate-asc':  {"application.deadline": "asc"},
}

auranest_stats_options = {
    'employers': 'employer.name.keyword',
    'sites': 'source.site.name.keyword',
    'locations': 'location.translations.sv-SE.keyword'
}
