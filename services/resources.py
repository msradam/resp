import pandas as pd
import math
from operator import itemgetter
import numpy as np
import scipy
from haversine import haversine
import osmnx as ox
import networkx as nx
from sklearn.neighbors import KDTree, DistanceMetric

csv = 'philippines.csv'


def find_nearest_hospitals(lon_key, lat_key, orig_lat, orig_lon, csv):
    df = pd.read_csv(csv)
    hospitals = []
    print(list(dict(df).keys()))
    for i in range(len(df)):
        hospitals.append(
            {"lat": df[lat_key][i], "lon": df[lon_key][i],
             "pos": i, "type": df["type"][i], "name": df["type"][i],
             "phone": df["phone"][i], "defining-hours": df["defining-hours"][i],
             "physical-address": df["physical-address"][i]})
    for hospital in hospitals:
        dist = haversine((orig_lat, orig_lon),
                         (hospital["lat"], hospital["lon"]))
        hospital["dist"] = dist
    hospitals = sorted(hospitals, key=itemgetter("dist"))
    print(hospitals[0:5])
    # print(hospitals)
    # positions = {}
    # for hospital in hospitals[:3]:
    #     positions[hospital["pos"]] = hospital["dist"]
    # nearest = []
    # for pos in positions.keys():
    #     nearest.append({"name": df['name'][pos],
    #                     "type": df['type'][pos],
    #                     "dist": df["dist"][pos],
    #                     "phone": df['phone'][pos],
    #                     "hours": df['defining-hours'][pos]})
    # return nearest


print(find_nearest_hospitals('X', 'Y', 123.0, 10.0, csv))


def find_route(orig_lat, orig_lon, dest_lat, dest_lon, radius):
    origin = (orig_lat, orig_lon)
    destination = (dest_lat, dest_lon)
    G = ox.graph_from_point(origin, distance=radius)
    (nodes, _) = ox.graph_to_gdfs(G)
    tree = KDTree(nodes[['y', 'x']], metric='euclidean')

    orig_idx = tree.query([origin], k=1, return_distance=False)[0]
    dest_idx = tree.query([destination], k=1, return_distance=False)[0]

    closest_node_to_orig = nodes.iloc[orig_idx].index.values[0]
    closest_node_to_dest = nodes.iloc[dest_idx].index.values[0]

    route = nx.shortest_path(G, closest_node_to_orig, closest_node_to_dest)

    print(route)


"""
instead of using watson use IBM machine learning to create lrm
"""
