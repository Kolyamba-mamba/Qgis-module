class OsmBuildingModel:
    """Класс данных из osm после парсинга"""

    def __init__(self, osmid, housenumber, street, building_type):
        self.osmid = osmid
        self.housenumber = housenumber
        self.street = street
        self.building_type = building_type