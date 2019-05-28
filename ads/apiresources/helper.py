from ads.apiresources import geokomp

location_cache = {}


def get_location_data(type, location, reqSession):
    if location not in location_cache:
        loc_resp = geokomp.makeGeoLocationReq(location, reqSession)
        loc = list(filter(lambda l: l['typ'] == type, loc_resp))
        location_cache[location] = loc[0]

    return location_cache[location]


def location_response_builder(resp, loc):
    match_lan_index = check_value_exist(loc['lankod'], resp['lan'], 'lankod')
    print(match_lan_index, loc['lankod'], resp['lan'], sep=' -- ')
    if match_lan_index < 0:
        lan = {
            'lannamn': loc['lannamn'],
            'lankod': loc['lankod'],
            'lan_job_total': 1,
            'kommun': [{
                'kommunnamn': loc['kommunnamn'],
                'kommunkod': loc['kommunkod'],
                'kommun_job_total': 1
            }]
        }
        resp['lan'].append(lan)
    else:
        match_kom_index = check_value_exist(loc['kommunkod'], resp['lan'][match_lan_index]['kommun'], 'kommunkod')
        if match_kom_index < 0:
            kommun = {
                'kommunnamn': loc['kommunnamn'],
                'kommunkod': loc['kommunkod'],
                'kommun_job_total': 1
            }
            resp['lan'][match_lan_index]['kommun'].append(kommun)
            resp['lan'][match_lan_index]['lan_job_total'] += 1
        else:
            resp['lan'][match_lan_index]['lan_job_total'] += 1
            resp['lan'][match_lan_index]['kommun'][match_kom_index]['kommun_job_total'] += 1

    return resp


def check_value_exist(value, ref_list, check_value):
    if len(ref_list) == 0:
        return -1
    else:
        for index, ref in enumerate(ref_list):
            if ref[check_value] == value:
                return index
        return -1
