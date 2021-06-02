class OsmWayModel:
    """Класс данных из osm после парсинга"""

    def __init__(self, housenumber, street, building_type):
        self.housenumber = housenumber
        self.street = street
        self.building_type = building_type