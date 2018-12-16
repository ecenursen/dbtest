class hospital:
    def __init__(self,hospital_id,hospital_name,is_public,location,administrator,telephone_number,ambulance_count):
        self.hospital_id=hospital_id
        self.hospital_name=hospital_name
        self.is_public=is_public
        self.location=location
        self.administrator=administrator
        self.telephone_number=telephone_number
        self.ambulance_count=ambulance_count


    def get_id(self):
        return self.hospital_id
    def get_name(self):
        return self.hospital_name
    def get_public(self):
        return self.is_public
    def get_location(self):
        return self.location
    def get_administrator(self):
        return self.administrator
    def get_telephone_number(self):
        return self.telephone_number
    def get_ambulance_count(self):
        return self.ambulance_count