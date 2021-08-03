# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import json
import urllib.request
import sqlite3
from os import path

path_database = "C:\\Users\\fadee\\PycharmProjects\\sqllite\\data\\EMPTY.db"
url_base = "https://url.delete.com/"
url_city = "TransportAPI/City/GetCityByRouteType/10607,10610,10613,13637,13639/1"
uriStation = "TransportAPI/Station/GetStationByCity/"
uriCityCenter = "TransportAPI/City/GetCityCoord/"
uriRoute = "TransportAPI/Route/GetCityRoutes/"
urlRouteParam = "/10607,10610,10613,13637,13639/"


def fetch_city():
    connection = sqlite3.connect(path_database)
    cursor = connection.cursor()

    url = url_base + url_city
    data = urllib.request.urlopen(url).read().decode()

    obj = json.loads(data)

    for child in obj:
        print(child)

        cursor.execute('INSERT INTO City(uid, type, name, tilesize, dateupdate) VALUES (?,?,?,?,?)',
                       (child['Id'], "город", child['Name'], child['Size'], ""))
        connection.commit()

    cursor.close()
    connection.close()


def getCityList():
    connection = sqlite3.connect(path_database)
    cursor = connection.cursor()

    sqlite_select_query = """SELECT uid from City"""
    cursor.execute(sqlite_select_query)
    records = cursor.fetchall()
    cities = []
    for row in records:
        cities.append(row[0])

    cursor.close()

    return cities


def fetch_cityCenter():
    connection = sqlite3.connect()
    cursor = connection.cursor()

    for cityId in getCityList():
        url = url_base + uriCityCenter + str(cityId)
        data = urllib.request.urlopen(url).read().decode()
        obj = json.loads(data)

        print(obj)
        center = obj['Center']
        cursor.execute('INSERT INTO Center(cityId, lat, lon) VALUES (?,?,?)',
                       (cityId, center['Lat'], center['Lon']))
        extent = obj['Extent']
        cursor.execute('INSERT INTO Extent(cityId, XMin, XMax, YMin, YMax) VALUES (?,?,?,?,?)',
                       (cityId, extent['XMin'], extent['XMax'], extent['YMin'], extent['YMax']))
        connection.commit()

    cursor.close()
    connection.close()


def fetch_station():
    connection = sqlite3.connect(path_database)
    cursor = connection.cursor()

    for cityId in getCityList():
        url = url_base + uriStation + str(cityId)
        data = urllib.request.urlopen(url).read().decode()
        obj = json.loads(data)

        print(obj)
        for child in obj:
            cursor.execute('INSERT INTO Station(stationId, lat, lon, name, direction, cityId, inCity, length, cluster) '
                           'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                           (
                               child['Id'], child['Coord']['Lat'], child['Coord']['Lon'], child['Name'],
                               child['Direction'],
                               child['CityId'], child['InCity'], child['Length'], child['Cluster']))

        connection.commit()

    cursor.close()
    connection.close()


def fetch_route():
    connection = sqlite3.connect(path_database)
    cursor = connection.cursor()

    for cityId in getCityList():
        url = url_base + uriRoute + str(cityId)
        data = urllib.request.urlopen(url).read().decode()
        obj = json.loads(data)

        print(obj)
        for child in obj:
            cursor.execute('INSERT INTO ROUTE(routeId, number, name, length, type, typeId, stationA, '
                           'stationB, tarif, class) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                           (
                               child['Id'], child['Coord']['Lat'], child['Coord']['Lon'], child['Name'],
                               child['Direction'],
                               child['CityId'], child['InCity'], child['Length'], child['Cluster']))
        connection.commit()

    cursor.close()
    connection.close()


if __name__ == '__main__':
    fetch_city()
    for city in getCityList():
       print(city)
    fetch_cityCenter()
    fetch_station()
