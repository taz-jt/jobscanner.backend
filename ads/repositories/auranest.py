import logging
import json
from datetime import datetime
from flask_restplus import abort
from elasticsearch import exceptions
from ads import settings
from ads.repositories import elastic
from collections import OrderedDict


log = logging.getLogger(__name__)


def findAds(args):
    log.debug('Getting request: %s', args)
    # Do this with skills and traits for occupation
    # aggregates = _statistics(args.pop(settings.STATISTICS),
    #                         args.pop(settings.STAT_LMT))
    query_dsl = _parse_args(args)
    query_dsl['aggs'] = {"total": {"cardinality": {"field": "group.id"}}}
    # if aggregates:
    #    query_dsl['aggs'].update(aggregates)
    # log.debug(json.dumps(query_dsl, indent=2))
    try:
        query_result = elastic.search(index=settings.ES_AURANEST, body=query_dsl)
    except exceptions.ConnectionError as e:
        logging.exception('Failed to connect to elasticsearch: %s' % str(e))
        abort(500, 'Failed to establish connection to database')
        return
    return query_result


def _statistics(agg_fields, agg_size):
    aggs = dict()
    size = agg_size if agg_size else 10

    for agg in agg_fields if agg_fields else []:
        aggs[agg] = {
            "terms": {
                "field": settings.auranest_stats_options[agg],
                "size": size
            }
        }
    return aggs


def _parse_args(args):
    args = dict(args)
    query_dsl = dict()
    query_dsl['from'] = args.pop(settings.OFFSET, 0)
    query_dsl['size'] = args.pop(settings.LIMIT, 10)
    # Remove api-key from args to make sure an empty query can occur
    # args.pop(settings.APIKEY, None)

    # Make sure to only serve published ads
    query_dsl['query'] = {
        'bool': {
            'must': [],
        }
    }
    query_dsl['collapse'] = {
        "field": "group.id",
        "inner_hits": {
            "name": "other",
            "_source": ["id", "source.url", "source.site.name"],
            "size": 20
        }
    }
    # Allways remove all expired job ads
    if(args[settings.SHOW_EXPIRED]=='false'):
        print(datetime.date(datetime.now()))
        query_dsl['query']['bool']['filter'] = [
            {'range': {'source.removedAt': {'gte': datetime.date(datetime.now())}}}
        ]
    # TODO: Filter on 'deadline' show or not show (en växel)
    # Check for empty query
    if not any(v is not None for v in args.values()):
        log.debug("Constructing match-all query")
        query_dsl['query']['bool']['must'].append({'match_all': {}})
        return query_dsl

    freetext_query = _build_query(args.get(settings.FREETEXT_QUERY),
                                  __freetext_fields)
    if freetext_query:
        query_dsl['query']['bool']['must'].append(freetext_query)
    place_query = _build_query(args.get(settings.PLACE),
                               __place_fields)
    if place_query:
        query_dsl['query']['bool']['must'].append(place_query)
    return query_dsl


def _build_query(querystring, fields_method):
    if not querystring:
        return None
    if isinstance(querystring, list):
        inc_words = ' '.join([w for w in querystring if not w.startswith('-')])
        exc_words = ' '.join([w[1:] for w in querystring if w.startswith('-')])
    else:
        inc_words = ' '.join([w for w in querystring.split(' ') if not w.startswith('-')])
        exc_words = ' '.join([w[1:] for w in querystring.split(' ') if w.startswith('-')])

    shoulds = fields_method(inc_words) if inc_words else None
    mustnts = fields_method(exc_words) if exc_words else None
    ft_query = {"bool": {}}
    if shoulds:
        ft_query['bool']['should'] = shoulds
    if mustnts:
        ft_query['bool']['must_not'] = mustnts

    return ft_query if shoulds or mustnts else None


def __place_fields(searchword):
    return [
        {
            "match": {
                "location.translations.sv-SE": searchword,
            }
        }
    ]


def __freetext_fields(searchword):
    search_fields = ["header^3", "title.freetext^3", "keywords",
                     "employer.name^2", "content.text"]
    return [
        {
            "multi_match": {
                "query": searchword,
                "type": "cross_fields",
                "operator": "and",
                "fields": search_fields
            }
        }
    ]


# Check and evaluate methods for skills and traits of an occupation


def initialize():
    global skills, traits
    skills = {}
    traits = {}


def validate_list(l):
    return True if (isinstance(l, list) and len(l) > 0) else False


def traverse_job_qualities(qualities, quality_type):
    if not validate_list(qualities):
        pass
    else:
        for q in qualities:
            quality_assembler(q, quality_type)


def quality_assembler(quality, quality_type):

    if not isinstance(quality, str):
        return 'Wrong value'

    if quality_type == 'skills':
        if quality not in skills:
            skills[quality] = 1
        else:
            skills[quality] += 1
    else:
        if quality not in traits:
            traits[quality] = 1
        else:
            traits[quality] += 1


def quality_sorter(qualities):
    l = ()
    if qualities == 'skills':
        return dict(sorted(skills.items(), key=lambda t: t[1], reverse=True))
    else:
        return dict(sorted(traits.items(), key=lambda t: t[1], reverse=True))


def quality_formatter(qualities):
    l = []
    totalQ = len(qualities)
    for k, v in qualities.items():
        l.append({'name': k, 'freq': round(v/totalQ, 2)})

    return l
