from flask_restplus import Resource, fields
from ads.rest import ns_geojobcount
from ads.repositories import auranest as auranestRepro
from ads.rest.model import queries
from ads.rest.model.auranest_results import auranest_lista, auranest_listb
from ads.apiresources import geokomp
import requests
from ads.apiresources import helper


@ns_geojobcount.route('')
class GeoJobCount(Resource):
    @ns_geojobcount.doc(description='get job count for a free text query')
    @ns_geojobcount.expect(queries.job_query)
    def get(self):
        args = queries.allJobs_query.parse_args()
        query_result = auranestRepro.findAds(args)

        loc_resp = {
            'total': 0,
            'lan': []
        }
        # GeoKomp add location
        httpSession = requests.Session()
        for ad in query_result['hits']['hits']:
            if ad['_source']['location']:
                loc_text = ad['_source']['location']['translations']['sv-SE']
                loc = helper.get_location_data('POSTORT', loc_text, httpSession)
                loc_resp = helper.location_response_builder(loc_resp, loc)
        httpSession.close()
        loc_resp['total'] = len(loc_resp['lan'])
        return 'hello geo-job-count'
