import numpy as np
from math import ceil
import sys
import random

street_intersection_mapping = {}
intersection_streets_mapping = {}
intersection_streets_mapping_in = {} # ulice koje ulaze u intersection npr map[Intersection]
streets_map = {} # lil-pump

def read_input(filename):
    global street_intersection_mapping, intersection_streets_mapping, streets_map, intersection_streets_mapping_in

    f = open(filename, 'r')
    lines = f.readlines()

    D, I, S, V, F = lines[0].split()
    D = int(D)
    I = int(I)
    S = int(S)
    V = int(V)
    F = int(F)

    streets = [] #[(B_intersection, I_intersection, name), ...]
    routes = []

    lines = lines[1:]
    for i in range(S):
        B, E, street_name, L = lines[i].split()
        B = int(B)
        E = int(E)
        L = int(L)
        streets.append((B,E,street_name,L))
        streets_map[street_name] = (B,E,L)
        street_intersection_mapping[street_name] = E

        if B in intersection_streets_mapping.keys():
            intersection_streets_mapping[B].append(street_name)
        else:
            intersection_streets_mapping[B] = [street_name]

        if E in intersection_streets_mapping_in.keys():
            intersection_streets_mapping_in[E].append(street_name)
        else:
            intersection_streets_mapping_in[E] = [street_name]

    lines = lines[S:]

    for i in range(V):
        route = lines[i].split()[1:]
        routes.append(route)

    return D, I, S, V, F, streets, routes

def stats(streets, routes):
    route_len_0 = sum(np.array(list(map(lambda street: streets_map[street][2], routes[0]))))

    min_time = streets[0][3]; max_time = streets[0][3]; avg_time = 0; sum_time = 0
    min_route_len = route_len_0; max_route_len = route_len_0; avg_route_len = 0; sum_route_len = 0

    for _,_,_,t in streets:
        sum_time += t
        if t > max_time:
            max_time = t
        if t < min_time:
            min_time = t

    avg_time = sum_time / float(len(streets))

    for route in routes:
        route_len = sum(np.array(list(map(lambda street: streets_map[street][2], route))))
        sum_route_len += route_len

        if route_len > max_route_len:
            max_route_len = route_len
        if route_len < min_route_len:
            min_route_len = route_len

    avg_route_len = sum_route_len / float(len(routes))

    print(f"Streets:\nMin time: {min_time}\nMax time: {max_time}\nAvg time: {avg_time}\n")
    print(f"Routes:\nMin route len: {min_route_len}\nMax route len: {max_route_len}\nAvg route len: {avg_route_len}\n")
    # return min_time, max_time, avg_time, min_route_len, max_route_len, avg_route_len


def route_len_time(route):
    return sum(np.array(list(map(lambda street: streets_map[street][2], route))))


if __name__ == "__main__":
    filename = sys.argv[1]
    n_split = int(sys.argv[2])
    D, I, S, V, F, streets, routes = read_input(filename)
    # stats(streets, routes)
    # exit()

    len1 = len(routes)
    routes = list(filter(lambda route: route_len_time(route) <= D, routes))
    # print(f"Removed {len1 - len(routes)} routes")

    # print(f"I={I}")
    intersection_jam = {}

    for i in range(I):
        intersection_jam[i] = {}
        for street in intersection_streets_mapping_in[i]:
            intersection_jam[i][street] = 0

    # print(intersection_jam)

    for route in routes:
        for i in range(len(route)):
            street = route[i]
            b = 5 * (i+1) / float(len(route))
            b = int(ceil(b))
            intersection_jam[street_intersection_mapping[street]][street] += max(1, b)

    # print(intersection_jam)

    for key in intersection_jam.keys():
        # print(intersection_jam[key])
        # print(dict(filter(lambda elem: elem[1] > 0, intersection_jam[key].items())))
        intersection_jam[key] = dict(filter(lambda elem: elem[1] > 0, intersection_jam[key].items()))

    intersection_jam = dict(filter(lambda elem: bool(elem[1]), intersection_jam.items()))

    # print(intersection_jam[499])
    # exit()
    print(len(intersection_jam))
    for key in intersection_jam.keys():
        print(key)
        if len(intersection_jam[key]) == 1:
            print(len(intersection_jam[key]))
            k = list(intersection_jam[key].keys())[0]
            print(f"{k} 1")
        else:
            values = list(intersection_jam[key].values())
            suma = sum(intersection_jam[key].values())

            intervals = []
            for street_name in intersection_jam[key].keys():
                #sort
                duration = ceil(D * intersection_jam[key][street_name] / (suma * n_split))
                percentage = ceil(intersection_jam[key][street_name] / (suma))
                intervals.append((street_name, duration,percentage))
            # intervals.sort(reverse=True, key=lambda e: e[1])
            # print(f"{intervals[0][0]} {1}")
            # random.shuffle(intervals)
            # intervals = list(filter(lambda e: e[2]>0.05, intervals))
            randss = []
            intss = []
            for i in range(len(intervals)):
                if random.random() > 0.05:
                    intss.append(intervals[i])

            print(len(intss))
            for i in range(len(intss)):
                street_name, duration, _ = intervals[i]
                print(f"{street_name} {1}")
            # for street_name, duration, _ in intervals:
            #     # print(f"{street_name} {duration}")
            #     if random.rand()
            #     print(f"{street_name} {1}")
