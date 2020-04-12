import csv
from time import time
from collections import defaultdict

from constants import activities_mapping
from structures import Address, Coords, Shop
from utils import compute_distance


class Data:
    def __init__(self):
        self._data_dump_file = '2019_censcomercialbcn_detall.csv'
        self.activity2shops = defaultdict(list)
        self._load_data()
        self._id2shop = {shop.identifier: shop for shops in self.activity2shops.values() for shop in shops}

    def __getitem__(self, identifier):
        return self._id2shop[identifier]

    def __contains__(self, identifier):
        return identifier in self._id2shop

    def _load_data(self):
        """
        Data Loader
        """
        init = time()
        raw_data = list()
        # Opening of the database
        with open(self._data_dump_file, encoding="utf8", newline='') as csvfile:
            # Extraction of the headers
            reader = csv.reader(csvfile)
            headers = next(reader)
            # raw_data is a dictionari with all the information from each shop
            for row in reader:
                raw_data.append(dict(zip(headers, row)))

        used_ids = set()
        used_addresses = set()
        for shop in raw_data:
            if shop['Nom_Principal_Activitat'] != 'Actiu' or shop['Nom_Local'] == 'SN':
                continue
            activity = shop['Nom_Activitat']
            # ELIMINO   'Finances i assegurances', 'Grans magatzems i hipermercats' i
            #           'Serveis de menjar take away MENJAR RÀPID'!!.
            if activity in activities_mapping:
                identifier = int(shop['ID_Bcn_2019'])
                mapped_activity = activities_mapping[activity]
                address = Address(name=shop['Nom_Local'], street=shop['Nom_Via'], num=int(shop['Num_Policia_Inicial']))
                if address in used_addresses or identifier in used_ids:
                    continue
                used_ids.add(identifier)
                used_addresses.add(address)
                self.activity2shops[mapped_activity].append(Shop(identifier=identifier,
                                                                 activity=mapped_activity,
                                                                 coords=Coords(latitude=float(shop['Latitud']),
                                                                               longitude=float(shop['Longitud']),
                                                                               x_utm=float(shop['X_UTM_ETRS89']),
                                                                               y_utm=float(shop['Y_UTM_ETRS89'])),
                                                                 address=address))
        print(f'Data loaded in {time() - init:.2f}s')

    def get_filtered_shops(self, my_coords: Coords, desired_activities: set, max_radius: int = 1000, max_shops=100):
        """
        Aquesta funció retorna totes les botigues de les activitats que s'han triat. Ex: totes les carniseries,
        peixateries, etc. en el radi indicat
        :param my_coords:
        :param desired_activities:
        :param max_radius:
        :param max_shops:
        :return:
        """
        filtered_shops = defaultdict(list)
        for activity, shops in self.activity2shops.items():
            if activity in desired_activities:
                near_shops = list()
                for shop in shops:
                    dist = compute_distance(my_coords, shop.coords)
                    if dist <= max_radius:
                        near_shops.append((shop, dist))
                filtered_shops[activity] = [shop_dist[0] for shop_dist in
                                            sorted(near_shops, key=lambda x: x[1])[:max_shops]]
        return filtered_shops
