#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import argparse                                                                    
import sys                                                                          
import json
import zipfile

import pandas as pd 
import io    
import urllib 

def dataJsonMaker(data):
    dataJson = []
    for element in data['features']:                                                                                         
        Name = element['properties']['name']
        Marque = element['properties']['marque']
        if element['properties']['capacity']:
            Capacity = element['properties']['capacity']
        else:
            Capacity = element['properties']['capacity'] = 0       
        Zip_code = element['properties']['com_insee']                               
        City = element['properties']['com_nom']                                      
        dataDict = {
            'Name' : Name,
            'Marque' : Marque,
            'City' : City,
            'Zip_code' : Zip_code,
            'Capacity' : int(Capacity),
        }
        dataJson.append(dataDict)   
    return dataJson


def main(args):
    if args.network == "vue":
        access_url = urllib.request.urlopen('https://geodatamine.fr/dump/cinema_geojson.zip')
        z = zipfile.ZipFile(io.BytesIO(access_url.read()))
        data = json.loads(z.read(z.infolist()[0]).decode())
            
        dataJson = dataJsonMaker(data)

        df = pd.DataFrame.from_dict(dataJson, orient='columns')
        cleanDf = df[df.Capacity != 0]

        TenSmallestTheatre = cleanDf.nsmallest(10, 'Capacity')
        Biggest_networks = df['Marque'].value_counts()[:3].index.tolist()
        cityAndTheatre = df.groupby(['Zip_code', 'City'])['Name'].count().reset_index(name='theaters')

        print(
            "10 smallest theaters :\n\n", TenSmallestTheatre,"\n",
            "\nBiggest networks :\n\n", Biggest_networks,"\n",
            "\nThe city with the most theaters :\n\n", cityAndTheatre.nlargest(1, 'theaters'), "\n"
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--network', dest='network', default='vue',                              
                        type=str, choices=['vue'],                             
                        help="Display some statistics about french theaters", required=True)                    
    args = parser.parse_args()
    main(args)
    
