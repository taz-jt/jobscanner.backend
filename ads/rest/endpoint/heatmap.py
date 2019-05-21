from flask_restplus import Resource, fields
from ads.rest import ns_heatmap
from ads.repositories import auranest as auranestRepro
from ads.rest.endpoint import auranest
from ads.rest.model import queries
import json


@ns_heatmap.route('')
class Heatmap(Resource):
    @ns_heatmap.doc(description='Find heat map of a specific job')
    @ns_heatmap.expect(queries.heatmap_query)
    def get(self):
        ads = auranest.AllJobsSearch().get()
        features = []
        for ad in ads['hits']:
            lng = ad['geolocation']['lng']
            lat = ad['geolocation']['lat']
            print(ad['location'], lat, lng, sep=', ')
            lat = 0 if ad['geolocation']['lat'] is None else ad['geolocation']['lat']
            lng = 0 if ad['geolocation']['lng'] is None else ad['geolocation']['lng']
            features.append({
                'type': 'Feature',
                'id': ad['id'],
                'geometry': {
                    'type': 'Point',
                    'coordinates': [float(lng)*100000, float(lat)*100000]
                }
            })

            # print(feature)

        res = json.dumps({
            'type': 'FeatureCollection',
            'totalFeatures': len(features),
            'features': features
        })
        with open('mock.txt', 'w') as file:
            file.write(res)

        return 'hello heatmap'
