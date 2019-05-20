from flask_restplus import Resource, fields
from ads.rest import ns_alljobs, ns_skillsandtraits
from ads.repositories import auranest as auranestRepro
from ads.rest.model import queries
from ads.rest.model.auranest_results import auranest_lista
from ads.apiresources import geokomp
import requests


@ns_alljobs.route('search')
class AllJobsSearch(Resource):
    @ns_alljobs.doc(description='Search with freetext query')
    @ns_alljobs.expect(queries.allJobs_query)
    def get(self):
        args = queries.allJobs_query.parse_args()
        query_result=auranestRepro.findAds(args)
        # GeoKomp add location
        httpSession=requests.Session()
        for ad in query_result['hits']['hits']:
            if ad['_source']['location']:
                ad['_source']['geolocation'] = {'lat': 0, 'lng': 0}
                coord = geokomp.getGeoLocation(ad['_source']['location']['translations']['sv-SE'], httpSession)
                ad['_source']['geolocation']['lng'] = coord['lng']  # y
                ad['_source']['geolocation']['lat'] = coord['lat']  # x
        httpSession.close()
        return self.marshal_default(query_result )

    @ns_alljobs.marshal_with(auranest_lista)
    def marshal_default(self, results):
        return results


@ns_skillsandtraits.route('skills')
class SkillsAndTraitsSearch(Resource):
    @ns_skillsandtraits.doc(description='Search skills and traits for a specific job')
    @ns_skillsandtraits.expect(queries.skillsandtraits_query)
    def get(self):
        args = queries.skillsandtraits_query.parse_args()
        query_result = auranestRepro.findAds(args)
        for ad in query_result['hits']['hits']:
            if ad['_source']['skills']:
                auranestRepro.traverse_job_qualities(ad['_source']['skills'], 'skills')
                auranestRepro.traverse_job_qualities(ad['_source']['traits'], 'traits')
                print
                # print(ad['_source']['skills'])
                # print(ad['_source']['traits'])
        print(auranestRepro.quality_sorter('skills'))
        print(auranestRepro.quality_sorter('traits'))
        return 'hello skills'
