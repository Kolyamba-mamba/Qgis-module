class BuildingModel:
    """Класс зданий с площадью и кол-вом жителей"""

    def __init__(self, osmid, housenumber, street, building_type, area, inhabitants_count, jkh):
        self.osmid = osmid
        self.housenumber = housenumber
        self.street = street
        self.building_type = building_type
        self.area = area
        self.inhabitants_count = inhabitants_count
        self.jkh = jkh