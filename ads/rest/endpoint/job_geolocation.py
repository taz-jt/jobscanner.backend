from flask_restplus import Resource, fields
from ads.rest import ns_jobgeolocation
from ads.repositories import auranest as auranestRepro
from ads.rest.model import queries
from ads.rest.model.auranest_results import auranest_listc

from ads.apiresources import geokomp
import requests


@ns_jobgeolocation.route('')
class JobGeoLocation(Resource):
    @ns_jobgeolocation.doc(description='Find the job count over the map for a specific job')
    @ns_jobgeolocation.expect(queries.heatmap_query)
    def get(self):
        features = []
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
                if coord['lng'] and coord['lat']:
                    features.append({
                        'type': 'Feature',
                        'id': ad['_source']['id'],
                        'geometry': {
                            'type': 'Point',
                            'coordinates': [coord['lat'], coord['lng']]
                        }
                    })

        httpSession.close()
        res = {
            'type': 'FeatureCollection',
            'totalFeatures': len(features),
            'features': features
        }

        return self.marshal_default(res)

    @ns_jobgeolocation.marshal_with(auranest_listc)
    def marshal_default(self, results):
        return results

