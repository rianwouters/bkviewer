from .array import Array


class Location:
    def __init__(self, name, short_name=None, city=None, township=None, county=None,  state_or_province=None, country=None, latitude=None, longitude=None, farm_or_manor_name=None, parish=None, postal_address=None, resident_id=None, residence_number=None, farm_number=None, property_number=None):
        self.name = name
        self.short_name = short_name
        self.city = city
        self.township = township
        self.county = county
        self.state_or_province = state_or_province
        self.country = country
        self.latitude = latitude
        self.longitude = longitude
        self.farm_or_manor_name = farm_or_manor_name
        self.parish = parish
        self.postal_address = postal_address
        self.resident_id = resident_id
        self.residence_number = residence_number
        self.farm_number = farm_number
        self.property_number = property_number
        self.notes = Array("Notes")
        self.files = Array("Files")

    def __str__(self) -> str:
        return self.name
