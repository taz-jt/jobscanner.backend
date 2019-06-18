from flask_restplus import Resource, fields
from ads.rest import ns_jobgeocount
from ads.repositories import auranest as auranestRepro
from ads.rest.model import queries
from ads.rest.model.auranest_results import auranest_listd
import requests
from ads.apiresources import helper


@ns_jobgeocount.route('')
class JobGeoCount(Resource):
    @ns_jobgeocount.doc(description='get job count for a free text query')
    @ns_jobgeocount.expect(queries.job_query)
    def get(self):
        args = queries.allJobs_query.parse_args()
        args['show-expired'] = 'false'
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
                if len(loc):
                    loc_resp = helper.location_response_builder(loc_resp, loc)
        httpSession.close()
        loc_resp['total'] = helper.get_total_jobCount(loc_resp['lan'])
        return self.marshal_default(loc_resp)

    @ns_jobgeocount.marshal_with(auranest_listd)
    def marshal_default(self, results):
        return results
