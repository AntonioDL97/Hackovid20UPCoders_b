import populartimes as pt
from time import time
from Ocupacio import *
import utils

import googlemaps
from datetime import datetime

class Populartimes():

    def __init__(self, name):
        self.apikey = 'AIzaSyDSbCbc_tuJC57KYxkUPiaxyG2tRkc3-Wk'
        self.I = Input(name)

    def get_optimization_info(self, id, shopinfo):
        day = utils.current_weekday()
        hour = utils.current_hour()
        people = -1
        for item in shopinfo:
            if((item == 'current_popularity')):
                people = shopinfo['current_popularity']
        if(people == -1):
            for i in range(len(shopinfo['populartimes'])):
                if(shopinfo['populartimes'][i]['name'] == day):
                    day = shopinfo['populartimes'][i]['name']
                    people = shopinfo['populartimes'][i]['data'][int(hour)]
        print(people)
        return(people)




    def find_shop(self, id, info_list):
        #init = time()
        gmaps = googlemaps.Client(key='AIzaSyDSbCbc_tuJC57KYxkUPiaxyG2tRkc3-Wk')
        shopinfo = self.I.get_store_info(id, info_list)
        #print(f'Data loaded in {time() - init:.2f}s')
        string = ''
        for item in shopinfo:
            string = str(str(string) + str(shopinfo[item]) + str(' '))
        #string = 'Netto city Harscampstraße Aachen'
        search1 = gmaps.find_place(string, 'textquery', fields=('place_id', 'opening_hours', 'rating'))
        try:
            shopid = search1['candidates'][0]['place_id']
            open_closed = search1['candidates'][0]['opening_hours']['open_now']
            rating = search1['candidates'][0]['rating']
            #init = time()
            data = pt.get_id('AIzaSyDSbCbc_tuJC57KYxkUPiaxyG2tRkc3-Wk', shopid)
            #print(f'Data loaded in {time() - init:.2f}s')
            day = utils.current_weekday()
            hour = utils.current_hour()
            people = -1
            try:
                for item in data:
                    if ((item == 'current_popularity')):
                        people = data['current_popularity']
                if (people == -1):
                    for i in range(len(data['populartimes'])):
                        if (data['populartimes'][i]['name'] == day):
                            day = data['populartimes'][i]['name']
                            people = data['populartimes'][i]['data'][int(hour)]
            except:
                people = 0
            relevant_info = [shopid, open_closed, rating, people]
            print(relevant_info)
            return(relevant_info)
        except:
            print('-')

def main():
    init = time()
    P = Populartimes('2019_censcomercialbcn_detall.csv')
    #print(f'Data loaded in {time() - init:.2f}s')
    #init = time()
    infolist = ['Nom_Local', 'Nom_Via', 'Num_Policia_Inicial']
    id = [1035811, 1028982, 1059038, 1014854, 1014832, 1014816, 1014934, 1014925, 1028716, 1014898, 1057015, 1048179, 1040130, 1014909, 1014834, 1014958]
    for i in range(len(id)):
        data = P.find_shop(id[i], infolist)
        #P.get_optimization_info(id[i], data)
    #print(data)
    print(f'Data loaded in {time() - init:.2f}s')

if __name__ == '__main__':
    main()