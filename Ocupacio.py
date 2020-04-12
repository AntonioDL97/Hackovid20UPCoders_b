import pandas as pd
from time import time
from collections import defaultdict

class Input():

    def __init__(self, df_name):
        self.b = True
        self.df = Input.read_csv(self, df_name)

    def read_csv(self, name):
        df = pd.read_csv(name, encoding="utf8", low_memory=False)
        return(df)

    def write_csv(self, name): #without index
        self.df.to_csv(name, index=False)

    def get_store_info(self, id, list_columns):
        shop = []
        data = {}
        for i in range(len(self.df.columns)):
            for j in range(len(list_columns)):
                if(self.df.columns[i] == list_columns[j]):
                    shopelement = Input.get_value(self, id, self.df.columns[i])
                    data[list_columns[j]] = shopelement
        return(data)


    def create_column(self, position, name, value):
        # Chacking if there is a column for the queue. In case there isn't, create a new one.
        for i in range(len(self.df.columns)):
            if (self.df.columns[i] == name):
                self.b = False
                break
        if (self.b == True):
            self.df.insert(position, name, value, allow_duplicates=False)
            Input.write_csv(self, '2019_censcomercialbcn_detall.csv')

    def change_value(self, id, element, columna):
        self.df.loc[self.df['ID_Bcn_2019'] == id, [columna]] += element
        Input.write_csv(self, '2019_censcomercialbcn_detall.csv')

    def get_value(self, id, columna):
        #df = Input.read_csv(self, '2019_censcomercialbcn_detall.csv')
        position = self.df.loc[self.df['ID_Bcn_2019'] == id, [columna]]
        index = position.index[0]
        value = self.df._get_value(index, columna)
        return(value)




def main():
    init = time()
    I = Input('2019_censcomercialbcn_detall.csv')
    # Reading the csv file
    # df = I.read_csv('2019_censcomercialbcn_detall.csv')
    # posicio = 49
    # columna = 'Ocupacio'
    # valor = 0
    # I.create_column(posicio, columna, valor, df)
    id = 1014751
    listcolumns = ['ID_Bcn_2019', 'Nom_Local', 'Ocupacio']
    #New person leaving (-1) or coming (+1)
    # new_ocupacio = 0
    # columna = 'Ocupacio'
    # I.change_value(df, id, new_ocupacio, columna)
    # queue = I.get_value(id, columna)
    # print('la cua del comerç', id, 'és de', queue, 'persones')
    shopinfo = I.get_store_info(id, listcolumns)
    print()
    print(shopinfo)
    print(f'Data loaded in {time() - init:.2f}s')


if __name__ == '__main__':
    main()