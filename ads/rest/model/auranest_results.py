import re
from flask_restplus import fields
from ads.rest import ns_alljobs as api


class ShortString(fields.Raw):
    element_pattern = re.compile('<([a-z]+) *[^/]*?>')

    def _find_last_element(self, words):
        for word in reversed(words):
            match = self.element_pattern.findall(word)
            if match:
                return "</%s>" % match[-1]
        return None

    def format(self, value):
        words = re.split(r'\s+', value)
        if len(words) > 100:
            valid_words = words[0:100]
            last_element = self._find_last_element(valid_words)
            new_value = " ".join(valid_words) + " ..."
            if last_element:
                new_value += last_element
        else:
            new_value = value

        return new_value


annons = api.model('Ad', {
    'id': fields.String(attribute='_source.id'),
    'header': fields.String(attribute='_source.header'),
    'content': ShortString(attribute='_source.content.text'),
    'markup': ShortString(attribute='_source.content.xml'),
    'employer': fields.Nested({
        'name': fields.String(),
        'logoUrl': fields.String()
    }, attribute='_source.employer', skip_none=True),
    'location': fields.String(attribute='_source.location.translations.sv-SE'),
    'geolocation':fields.Nested({
        'lng':fields.String(),
        'lat':fields.String()
    }, attribute='_source.geolocation'),
    'application': fields.Nested({
        'url': fields.String(),
        'email': fields.String(),
        'deadline': fields.DateTime(),
        'reference': fields.String(),
        'site': fields.Nested({
            'url': fields.String(),
            'name': fields.String()
        }, attribute='site')
    }, attribute='_source.application', skip_none=True),
    'detected_keywords': fields.Nested({
        'occupations': fields.List(fields.String),
        'skills': fields.List(fields.String),
        'traits': fields.List(fields.String)
    }, attribute='_source'),
    'sources': fields.List(fields.Nested({
        'id': fields.String(attribute='_source.id'),
        'name': fields.String(attribute='_source.source.site.name'),
        'url': fields.String(attribute='_source.source.url'),
    }), attribute='inner_hits.other.hits.hits')
})

stat_value = api.model('StatValue', {
    'value': fields.String(attribute='key'),
    'count': fields.Integer(attribute='doc_count')
})

auranest_lista = api.model('Ads', {
    'total': fields.Integer(attribute='aggregations.total.value'),
    'stats': fields.Nested({
        'employers': fields.List(fields.Nested(stat_value),
                                 attribute='employers.buckets'),
        'sites': fields.List(fields.Nested(stat_value),
                             attribute='sites.buckets'),
        'locations': fields.List(fields.Nested(stat_value),
                                 attribute='locations.buckets'),
    }, attribute='aggregations', skip_none=True),
    'hits': fields.List(fields.Nested(annons), attribute='hits.hits')
})

quality_value = api.model('QualityValue', {
    'name': fields.String,
    'freq': fields.Float
})

auranest_listb = api.model('SkillnTrait', {
    'skills': fields.List(fields.Nested(quality_value)),
    'traits': fields.List(fields.Nested(quality_value))
})
