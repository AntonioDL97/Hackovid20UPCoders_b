from time import time
from itertools import permutations, product
from collections import defaultdict
from typing import List

from dijkstra import Graph, Edge
from utils import pairwise, compute_distance

from data_loader import Data
from external import GoogleMapsHandler
from structures import Coords, Shop


class PathFinder:
    def __init__(self):
        self._costs = defaultdict()
        self._data = Data()
        self._gmaps_handler = None

    def install_gmaps_handler(self):
        if self._gmaps_handler is None:
            self._gmaps_handler = GoogleMapsHandler()
        return self._gmaps_handler

    def compute_distance(self, shop1: Shop, shop2: Shop):
        """

        :param shop1:
        :param shop2:
        :return:
        """
        if (shop1.identifier, shop2.identifier) not in self._costs:
            self._costs[(shop1.identifier, shop2.identifier)] = compute_distance(shop1.coords, shop2.coords)
            self._costs[(shop2.identifier, shop1.identifier)] = self._costs[(shop1.identifier, shop2.identifier)]
        return self._costs[(shop1.identifier, shop2.identifier)]

    def compute_edges(self, shop_lists: List[Shop]):
        """

        :param shop_lists:
        :return:
        """
        edges = list()
        for shop_list1, shop_list2 in pairwise(shop_lists):
            for shop1, shop2 in product(shop_list1, shop_list2):
                edges.append(Edge(shop1.identifier, shop2.identifier, self.compute_distance(shop1, shop2)))
        return edges

    def compute_graphs(self, data, my_coords: Coords):
        """

        :param data:
        :param my_coords:
        :return:
        """
        graphs = list()
        # Crea tots els ordres possibles de recorregut
        used_orders = set()
        for i, key_order in enumerate(permutations(data.keys(), len(data)), start=1):
            if key_order in used_orders:
                continue
            used_orders.add(key_order)
            used_orders.add(key_order[::-1])  # Only one direction is enough
            init = time()
            ordered_shops = list()
            ordered_shops.append([Shop(identifier='A', coords=my_coords)])
            ordered_shops.extend([data[key] for key in key_order])
            ordered_shops.append([Shop(identifier='B', coords=my_coords)])
            graph = Graph(self.compute_edges(ordered_shops))
            graphs.append(graph)
            print(f'Computed subgraph {i} in {time() - init:.2f}s')
        return graphs

    def _find_best_with_graphs(self, data, my_coords: Coords):
        """
        Donat el diccionari de comerços dins de l'area i la teva localització et retorna els subgraphs
        :param data:
        :param my_coords:
        :return:
        """
        graphs = self.compute_graphs(data, my_coords)
        abs_best_route = None
        abs_best_dist = float('inf')
        for i, graph in enumerate(graphs, start=1):
            init = time()
            best_route, dist = graph.dijkstra('A', 'B')
            best_route = best_route[1:-1]  # Remove A and B
            if dist < abs_best_dist:
                abs_best_route = best_route
                abs_best_dist = dist
            print(f'Computed best path for subgraph {i} in {time() - init:.2f}s:')
            print('\t' + '-->'.join(['Home'] + [str(identifier) for identifier in best_route] + ['Home']))
            print(f'\tDistance: {dist:.2f}m')
        return abs_best_route, abs_best_dist

    def find_best_path(self, desired_activities, my_coords, max_radius=1000, max_shops=100):
        """

        :param desired_activities:
        :param my_coords: coordinates of my house
        :param max_radius: in meters, max distance between starting point and a shop
        :param max_shops: max shops to consider of each kind, ordered by distance (increasing)
        :return:
        """
        init = time()
        filtered_data = self._data.get_filtered_shops(my_coords=my_coords,
                                                      desired_activities=desired_activities,
                                                      max_radius=max_radius,
                                                      max_shops=max_shops)

        print(f'Found locals in a radius of {max_radius}m:')
        for k, v in filtered_data.items():
            print(f"\t{k + ':':30} {len(v)}")

        best_route, best_dist = self._find_best_with_graphs(filtered_data, my_coords)
        print('The best route is:')
        print('-->'.join(['Home'] + [str(self._data[identifier].address) for identifier in best_route] + ['Home']))
        print(f'The route covers a distance of {best_dist:.2f}m')
        print(f'Total runtime: {time() - init:.2f}s')
        return best_route

    def find_best_supermarket(self, my_coords, max_radius=1000, max_shops=10):
        if self._gmaps_handler is None:
            self.install_gmaps_handler()

        init = time()
        supermarkets = self._data.get_filtered_shops(my_coords=my_coords,
                                                     desired_activities={'Supermercats'},
                                                     max_radius=max_radius,
                                                     max_shops=max_shops)['Supermercats']

        if len(supermarkets) >= max_shops:
            print(f'Found more than {max_shops} supermarkets in a radius of {max_radius}m')
        else:
            print(f'Found a total of {len(supermarkets)} supermarkets in a radius of {max_radius}m')

        for shop in supermarkets:
            self._gmaps_handler.get_shop_info(shop)

        good_shops, bad_shops = [], []
        for shop in supermarkets:
            if shop.rating < 2.5:
                bad_shops.append(shop)
            else:
                good_shops.append(shop)
        rated_shops = good_shops + bad_shops
        rated_shops = rated_shops[:5]

        for shop in rated_shops:
            self._gmaps_handler.get_popular_times(shop)

        best_shop = min(rated_shops, key=lambda x: x.pct_people)
        print(f'The best supermaket is: {best_shop.address}, '
              f'at a distance of {self.compute_distance(Shop(identifier="A", coords=my_coords), best_shop):.2f}m')
        print(f'Found best supermarket in {time() - init:.2f}s')
        return best_shop


if __name__ == '__main__':

    ############################################# Mocked data for tests ################################################
    numero_tendes = 3
    import random
    home_coords = Coords(x_utm=430226.85, y_utm=4581590.93)
    print(f"Starting position: ({home_coords.x_utm}, {home_coords.y_utm})")
    activities = ['Fruiteries i verduleries', 'Farmàcies', 'Drogueries', 'Carnisseries']
    #activities = random.sample({'Fruiteries i verduleries', 'Fleques i Pastisseries', 'Drogueries', 'Supermercats',
     #                           'Herbolaris', 'Peixateries', 'Farmàcies', 'Menjar preparat', 'Carnisseries'},
      #                         numero_tendes)
    ####################################################################################################################

    pf = PathFinder()
    if len(activities) <= 3:
        pf.find_best_path(desired_activities=activities,
                          my_coords=home_coords)
    else:
        pf.find_best_supermarket(my_coords=home_coords)
