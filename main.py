import pandas as pd
import xml.etree.cElementTree as ET
from geopy.geocoders import Nominatim
from models.OsmBuildingModel import OsmBuildingModel
from models.BuildingModel import BuildingModel
from models.BuildingWithLocationModel import BuildingWithLocationModel


# получение города
def find_city(tree, jkh):
    city = None
    for field in tree.findall('way'):
        city_tmp = field.find("tag[@k='addr:city']")
        if city_tmp is not None:
            city = city_tmp.attrib['v']
            break
    if city is None:
        for field in tree.findall('relation'):
            city_tmp = field.find("tag[@k='addr:city']")
            if city_tmp is not None:
                city = city_tmp.attrib['v']
                break
    if city is None:
        city = jkh['formalname_city'].value_counts().index[0]
    return city


# извлекаем данные из осм
def parse_osm(tree, field_name):
    osm_list = []
    for field in tree.findall(field_name):
        osmid = field.attrib['id']

        housenumber = None
        housenumber_tmp = field.find("tag[@k='addr:housenumber']")
        if housenumber_tmp is not None:
            housenumber = housenumber_tmp.attrib['v']

        street = None
        street_tmp = field.find("tag[@k='addr:street']")
        if street_tmp is not None:
            street = street_tmp.attrib['v']

        building_type = None
        building_type_tmp = field.find("tag[@k='building']")
        if building_type_tmp is not None:
            building_type = building_type_tmp.attrib['v']

        if osmid is not None and housenumber is not None and street is not None and building_type is not None:
            osm_way_model = OsmBuildingModel(osmid, housenumber, street, building_type)
            osm_list.append(osm_way_model)

    return osm_list


# сопоставляем данные осм и реестра жкх
def prepare_building(jkh_data, osm_list, city):
    l = len(jkh_data.values[0])
    used_ways = []
    building_list = []
    for d in jkh_data.values:
        if d[10].lower() == city.lower():
            if pd.isna(d[12]) or pd.isna(d[13]):
                continue
            for way in osm_list:
                if way not in used_ways \
                        and d[12].lower() in str(way.street).lower() \
                        and d[13].lower() == way.housenumber.lower():
                    building = None
                    # Если есть площадь жилых помещений
                    if not pd.isna(d[35]):
                        area = d[35]
                        inhabitants_count = int(float(area.replace(',', '.')) // 25)
                        building = BuildingModel(way.osmid, way.housenumber, way.street, 'reforma', area,
                                                 inhabitants_count, d)
                    # # Иначе если есть общая площадь
                    elif not pd.isna(d[34]):
                        area = d[34]
                        inhabitants_count = int(float(area.replace(',', '.')) // 25)
                        building = BuildingModel(way.osmid, way.housenumber, way.street, 'reforma', area,
                                                 inhabitants_count, d)
                    # Иначе если есть кол-во квартир
                    elif not pd.isna(d[31]):
                        # площадь считаем, как произведение квартир в доме и среднего размера квартиры в России
                        area = int(d[31]) * 50
                        inhabitants_count = int(float(area) // 25)
                        building = BuildingModel(way.osmid, way.housenumber, way.street, 'reforma', area,
                                                 inhabitants_count, d)
                    if building:
                        used_ways.append(way)
                        building_list.append(building)

    valid_building_types = ["house", "terrace", "detached"]
    for way in osm_list:
        if way not in used_ways:
            if way.building_type in valid_building_types:
                building = BuildingModel(way.osmid, way.housenumber, way.street, way.building_type, None, 3, [None for _ in range(l)])
                used_ways.append(way)
                building_list.append(building)

    return building_list


# геокодирование
def geocode(building_list, city):
    result_list = []
    geolocator = Nominatim(user_agent="qgisModule")
    for building in building_list:
        addr_tmp = [city, building.street, building.housenumber.replace(' ', '').lower()]
        location = geolocator.geocode(' '.join(addr_tmp))
        if location:
            building_with_location = \
                BuildingWithLocationModel(building.osmid, building.housenumber, building.street, building.building_type,
                                          building.inhabitants_count, location.latitude, location.longitude,
                                          location.address, building.jkh)
            result_list.append(building_with_location)
    return result_list


def main():
    tree = ET.parse('C:\\Users\\mrkol\\Downloads\\export.osm')
    jkh_data = pd.read_csv('C:\\Users\\mrkol\\Downloads\\export-reestrmkd-31-20210601\\export-reestrmkd-31-20210601.csv', sep=';')
    osm_list = parse_osm(tree, 'way') + parse_osm(tree, 'relation')
    city = find_city(tree, jkh_data)
    building_list = prepare_building(jkh_data, osm_list, city)
    building_with_location = geocode(building_list, city)
    names = jkh_data.columns.values
    data = list((a.osmid, a.latitude, a.longitude, a.address, a.inhabitants_count, *a.jkh) for a in building_with_location)
    result = pd.DataFrame(data, columns=['Osmid', 'Latitude', 'Longitude', 'GeocodeAddress', 'InhabitantsCount', *names])
    result.to_csv('building.csv', index=False)


if __name__ == '__main__':
    main()