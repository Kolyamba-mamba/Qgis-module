class BuildingWithLocationModel:
    """Класс зданий с координатами"""

    def __init__(self, osmid, housenumber, street, building_type, inhabitants_count, latitude, longitude, address, jkh):
        self.osmid = osmid
        self.housenumber = housenumber
        self.street = street
        self.building_type = building_type
        self.inhabitants_count = inhabitants_count
        self.latitude = latitude
        self.longitude = longitude
        self.jkh = jkh
        self.address = address
