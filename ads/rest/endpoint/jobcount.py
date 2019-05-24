from flask_restplus import Resource, fields
from ads.rest import ns_jobcount
from ads.repositories import auranest as auranestRepro
from ads.rest.model import queries
from ads.rest.model.auranest_results import auranest_listc

from ads.apiresources import geokomp
import requests
from ads.apiresources import helper

@ns_jobcount.route('')
class JobCount(Resource):
    @ns_jobcount.doc(description='Find job count')
    @ns_jobcount.expect(queries.jobcount_query)
    def get(self):
        args = queries.allJobs_query.parse_args()
        query_result = auranestRepro.findAds(args)

        loc_resp = {}
        # GeoKomp add location
        httpSession = requests.Session()
        for ad in query_result['hits']['hits']:
            if ad['_source']['location']:
                loc_text = ad['_source']['location']['translations']['sv-SE']
                loc = helper.get_location_data('POSTORT', loc_text, httpSession)
                loc_resp = helper.location_response_builder(loc_resp, loc)
                # resp = geokomp.makeGeoLocationReq(ad['_source']['location']['translations']['sv-SE'], httpSession)
                # print(ad['_source']['location']['translations']['sv-SE'], resp)
        httpSession.close()
        loc_resp['total'] = helper.get_total_count(loc_resp)
        print(loc_resp)
        return 'hello job count'

