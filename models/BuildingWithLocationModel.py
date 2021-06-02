class BuildingWithLocationModel:
    """Класс зданий с координатами"""

    def __init__(self, housenumber, street, building_type, area, inhabitants_count, latitude, longitude, address):
        self.housenumber = housenumber
        self.street = street
        self.building_type = building_type
        self.area = area
        self.inhabitants_count = inhabitants_count
        self.latitude = latitude
        self.longitude = longitude
        self.address = address
