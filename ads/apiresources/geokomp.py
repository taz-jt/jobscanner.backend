import logging
import json

log = logging.getLogger(__name__)

class GeoKomp:
    tmpCache={}
    pass

def __getCoordinates(aObject):
    orderToCheck = ['ORT', 'POSTORT', 'KOMMUN', 'LAN']
    dictObjects = {}
    for geo in aObject:
        dictObjects[geo['typ']]=geo
    if any(dictObjects.values()):
        for name in orderToCheck:
            if name in dictObjects:
                return __setCoordinate(dictObjects[name])
    coordinates = {'lat': None, 'lng': None}
    return coordinates


def __setCoordinate(aObject):
    coordinates = {'lat': aObject['koordinater']['WGS84']['x'], 'lng': aObject['koordinater']['WGS84']['y']}
    return coordinates

def getGeoLocation(location, reqSession):
    if not location:
        return {'lat': None, 'lng': None}
    #TODO: move all config to settings.py
    if location not in GeoKomp.tmpCache:
        geokomp_URL = "http://www.arbetsformedlingen.se:80/rest/geo/rest"
        friText_path = '/v1/fritext'
        params = {'text': location, 'hints': 'postnummer,gata'}
        url = geokomp_URL + friText_path
        headers = {'Accept': 'application/json', 'applicationId': 'Jobscanner'}
        response = reqSession.get(geokomp_URL + friText_path, params=params, headers=headers)
        response.encoding='ISO-8859-1'
        jresp = json.loads(response.text)
        if jresp:
            coordinates = __getCoordinates(jresp)
        else:
            coordinates = {'lat': None, 'lng': None}
        GeoKomp.tmpCache[location]=coordinates;
    return GeoKomp.tmpCache[location]