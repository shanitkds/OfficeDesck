from math import radians, cos, sin, asin, sqrt

def calculate_distance_km(lat1, lon1, lat2, lon2):
    R = 6371
    lat1, lon1, lat2, lon2 = map(
        radians, [lat1, lon1, lat2, lon2]
    )

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = sin(dlat/2)**2 + cos(lat1)*cos(lat2)*sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    return R * c


def verify_location(office_lat, office_lon, user_lat, user_lon, allowed_km=1):
    distance = calculate_distance_km(
        office_lat, office_lon, user_lat, user_lon
    )
    return distance <= allowed_km
