from pyproj import Proj, transform


def transform_coord_3857(lat, lng):
    P3857 = Proj(init='epsg:3857')
    P4326 = Proj(init='epsg:4326')

    x, y = transform(P4326, P3857, lat, lng)
    return x, y
