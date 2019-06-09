import io
import zipfile
import requests
import pandas as pd
import numpy as np
import scipy
from sklearn.neighbors import KDTree, DistanceMetric
import os
import shapefile
import json
from geopy.geocoders import Nominatim

country_list = ["Afghanistan","Albania","Algeria","Andorra","Angola","Anguilla","Antigua &amp; Barbuda","Argentina","Armenia","Aruba","Australia","Austria","Azerbaijan","Bahamas"
	,"Bahrain","Bangladesh","Barbados","Belarus","Belgium","Belize","Benin","Bermuda","Bhutan","Bolivia","Bosnia &amp; Herzegovina","Botswana","Brazil","British Virgin Islands"
	,"Brunei","Bulgaria","Burkina Faso","Burundi","Cambodia","Cameroon","Canada","Cape Verde","Cayman Islands","Chad","Chile","China","Colombia","Congo","Cook Islands","Costa Rica"
	,"Cote D Ivoire","Croatia","Cruise Ship","Cuba","Cyprus","Czech Republic","Denmark","Djibouti","Dominica","Dominican Republic","Ecuador","Egypt","El Salvador","Equatorial Guinea"
	,"Estonia","Ethiopia","Falkland Islands","Faroe Islands","Fiji","Finland","France","French Polynesia","French West Indies","Gabon","Gambia","Georgia","Germany","Ghana"
	,"Gibraltar","Greece","Greenland","Grenada","Guam","Guatemala","Guernsey","Guinea","Guinea Bissau","Guyana","Haiti","Honduras","Hong Kong","Hungary","Iceland","India"
	,"Indonesia","Iran","Iraq","Ireland","Isle of Man","Israel","Italy","Jamaica","Japan","Jersey","Jordan","Kazakhstan","Kenya","Kuwait","Kyrgyz Republic","Laos","Latvia"
	,"Lebanon","Lesotho","Liberia","Libya","Liechtenstein","Lithuania","Luxembourg","Macau","Macedonia","Madagascar","Malawi","Malaysia","Maldives","Mali","Malta","Mauritania"
	,"Mauritius","Mexico","Moldova","Monaco","Mongolia","Montenegro","Montserrat","Morocco","Mozambique","Namibia","Nepal","Netherlands","Netherlands Antilles","New Caledonia"
	,"New Zealand","Nicaragua","Niger","Nigeria","Norway","Oman","Pakistan","Palestine","Panama","Papua New Guinea","Paraguay","Peru","Philippines","Poland","Portugal"
	,"Puerto Rico","Qatar","Reunion","Romania","Russia","Rwanda","Saint Pierre &amp; Miquelon","Samoa","San Marino","Satellite","Saudi Arabia","Senegal","Serbia","Seychelles"
	,"Sierra Leone","Singapore","Slovakia","Slovenia","South Africa","South Korea","Spain","Sri Lanka","St Kitts &amp; Nevis","St Lucia","St Vincent","St. Lucia","Sudan"
	,"Suriname","Swaziland","Sweden","Switzerland","Syria","Taiwan","Tajikistan","Tanzania","Thailand","Timor L'Este","Togo","Tonga","Trinidad &amp; Tobago","Tunisia"
	,"Turkey","Turkmenistan","Turks &amp; Caicos","Uganda","Ukraine","United Arab Emirates","United Kingdom","United States","United States Minor Outlying Islands","Uruguay"
,"Uzbekistan","Venezuela","Vietnam","Virgin Islands (US)","Yemen","Zambia","Zimbabwe"];

for country in country_list:
    try:
        hs_dir = country+"_healthsites/"
        r = requests.get(
            "https://healthsites.io/media/shapefiles/" + country.replace(' ', '%20') + "_shapefile.zip")
        print("Retrieving shpfile")
        z = zipfile.ZipFile(io.BytesIO(r.content))
        z.extractall(hs_dir)

        sf = shapefile.Reader(hs_dir+country+".shp")
        geojson = sf.__geo_interface__['features']
        # os.remove(hs_dir)

        f = open(country.replace(' ','_')+"_healthsites.geojson", 'w')
        json.dump(geojson, f)
        f.close()
    except:
        pass


def get_nearest_hosp(point, hospitals):

    coords = [[hospital['index'], hospital['lng'], hospital['lat']]
              for hospital in hospitals]
    df = pd.DataFrame(coords, columns=['index', 'x', 'y']).set_index('index')
    print(coords)

    df['reference_y'] = point[0]
    df['reference_x'] = point[1]
 2
    # calculate the distance between each node and the reference point
    distances = great_circle_vec(lat1=df['reference_y'],
                                 lng1=df['reference_x'],
                                 lat2=df['y'],
                                 lng2=df['x'])

    # nearest_node = distances.idxmin()
    # if caller requested return_dist, return distance between the point and the
    # nearest node as well
    nearest = np.argsort(distances)[:10]
    return nearest


def great_circle_vec(lat1, lng1, lat2, lng2, earth_radius=6371009):
    """
    Credit to: OSMNX Python Library
    Vectorized function to calculate the great-circle distance between two
    points or between vectors of points, using haversine.
    Parameters
    ----------
    lat1 : float or array of float
    lng1 : float or array of float
    lat2 : float or array of float
    lng2 : float or array of float
    earth_radius : numeric
        radius of earth in units in which distance will be returned (default is
        meters)
    Returns
    -------
    distance : float or vector of floats
        distance or vector of distances from (lat1, lng1) to (lat2, lng2) in
        units of earth_radius
    """

    phi1 = np.deg2rad(lat1)
    phi2 = np.deg2rad(lat2)
    d_phi = phi2 - phi1

    theta1 = np.deg2rad(lng1)
    theta2 = np.deg2rad(lng2)
    d_theta = theta2 - theta1

    h = np.sin(d_phi / 2) ** 2 + np.cos(phi1) * \
        np.cos(phi2) * np.sin(d_theta / 2) ** 2
    h = np.minimum(1.0, h)  # protect against floating point errors

    arc = 2 * np.arcsin(np.sqrt(h))

    # return distance in units of earth_radius
    distance = arc * earth_radius
    return distance


def find_nearest_hospitals(country, orig_lat, orig_lon):
    geolocator = Nominatim(user_agent="resp")

    f = open(country+"_healthsites.geojson", 'r')
    geojson = json.load(f)
    f.close()
    hospitals = []
    nearest = []
    for i in range(len(geojson)):
        hosp = {}
        hosp['index'] = i
        hosp['activities'] = geojson[i]['properties']['activities']
        hosp['services'] = geojson[i]['properties']['services']
        hosp['beds'] = geojson[i]['properties']['beds']
        hosp['phone'] = geojson[i]['properties']['phone']
        hosp['mobile'] = geojson[i]['properties']['mobile']
        hosp['lat'] = geojson[i]['geometry']['coordinates'][1]
        hosp['lng'] = geojson[i]['geometry']['coordinates'][0]
        hosp['contact'] = geojson[i]['properties']['contact']
        hosp['type'] = geojson[i]['properties']['type']
        hospitals.append(hosp)

    nearest = [hospitals[idx]
               for idx in (get_nearest_hosp((orig_lat, orig_lon), hospitals))]
    for near in nearest:
        print(near["lat"], near["lng"])
        location = geolocator.reverse((near["lat"], near["lng"]))
        near['address'] = location.address

    return nearest

# def find_route(orig_lat, orig_lon, dest_lat, dest_lon, radius):
#     origin = (orig_lat, orig_lon)
#     destination = (dest_lat, dest_lon)
#     G = ox.graph_from_point(origin, distance=radius)
#     (nodes, _) = ox.graph_to_gdfs(G)
#     tree = KDTree(nodes[['y', 'x']], metric='euclidean')

#     orig_idx = tree.query([origin], k=1, return_distance=False)[0]
#     dest_idx = tree.query([destination], k=1, return_distance=False)[0]

#     closest_node_to_orig = nodes.iloc[orig_idx].index.values[0]
#     closest_node_to_dest = nodes.iloc[dest_idx].index.values[0]

#     route = nx.shortest_path(G, closest_node_to_orig, closest_node_to_dest)

#     print(route)
