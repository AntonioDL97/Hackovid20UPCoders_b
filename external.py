from time import time
import googlemaps
import populartimes

import utils
from data_loader import Data
from structures import Shop


class GoogleMapsHandler:
    def __init__(self):
        self._api_key = 'AIzaSyDSbCbc_tuJC57KYxkUPiaxyG2tRkc3-Wk'
        self._client = googlemaps.Client(key=self._api_key)

    def get_shop_info(self, shop: Shop):
        """
        Add docu
        :param shop:
        """
        init = time()
        query_string = f'{shop.address.name} {shop.address.street} {shop.address.num}'
        search_result = self._client.find_place(query_string, 'textquery',
                                                fields=('place_id', 'opening_hours', 'rating'))
        if not search_result['candidates']:
            print(f'Failed to find in {time() - init:.2f}s')
            return
        gmaps_id = search_result['candidates'][0].get('place_id')
        is_open = search_result['candidates'][0].get('opening_hours', {}).get('open_now', False)
        rating = search_result['candidates'][0].get('rating', 0)
        shop.set_gmaps_info(gmaps_id=gmaps_id, is_open=is_open, rating=rating)
        print(f'Google search took {time() - init:.2f}s: is_open={is_open}, rating={rating}')

    def get_popular_times(self, shop: Shop):
        """
        Add docu
        :param shop:
        """
        init = time()
        if shop.gmaps_id is None:
            return
        data = populartimes.get_id(self._api_key, shop.gmaps_id)
        print(f'Populartimes query took {time() - init:.2f}s')
        day, hour = utils.current_weekday(), utils.current_hour()
        pct_people = data.get('current_popularity')
        if pct_people is None:
            if 'populartimes' in data:
                for weekday_info in data['populartimes']:
                    if weekday_info['name'] == day:
                        day = weekday_info['name']
                        pct_people = weekday_info['data'][int(hour)]
            else:
                pct_people = 0
        shop.set_pct_people(pct_people=pct_people)


def main():
    data = Data()
    gmh = GoogleMapsHandler()
    import random
    ids = random.sample(data._id2shop.keys(), 10)
    print(ids)
    shops = [data[identifier] for identifier in ids]
    init = time()
    for shop in shops:
        gmh.get_shop_info(shop)
        gmh.get_popular_times(shop)
    print(f'All data found in {time() - init:.2f}s')


if __name__ == '__main__':
    main()
