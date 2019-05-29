from ads.apiresources import geokomp

location_cache = {}


def get_location_data(type, location, reqSession):
    if location not in location_cache:
        loc_resp = geokomp.makeGeoLocationReq(location, reqSession)
        loc = list(filter(lambda l: l['typ'] == type, loc_resp))
        location_cache[location] = loc[0]

    return location_cache[location]


def location_response_builder(loc_resp, loc):

    if loc['lankod'] not in loc_resp:
        loc_resp[loc['lankod']] = {
            'lan_total': 1,
            'lannamn': loc['lannamn'],
            loc['kommunkod']: {
                'kommunnamn': loc['kommunnamn'],
                'kommun_total': 1
            }
        }
    else:
        if loc['kommunkod'] not in loc_resp[loc['lankod']]:
            temp_dict = loc_resp[loc['lankod']]
            temp = {
                'kommunnamn': loc['kommunnamn'],
                'kommun_total': 1
            }
            temp_dict[loc['kommunkod']] = temp
            loc_resp[loc['lankod']]['lan_total'] += 1
            print(loc_resp[loc['lankod']][loc['kommunkod']])
        else:
            loc_resp[loc['lankod']]['lan_total'] += 1
            loc_resp[loc['lankod']][loc['kommunkod']]['kommun_total'] += 1

    # print(loc)
    return loc_resp


def get_total_count(loc_resp):
    total_count = 0
    for loc in loc_resp:
        total_count += loc['lan_total']
    return total_count
