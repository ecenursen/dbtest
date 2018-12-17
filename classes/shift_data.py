class shift_data:
    def __init__(self,shift_id,personnel_id,shift_begin_date,shift_repeat_interval,shift_hours, dayshift,emergency_area_assigned, name):
        self.shift_id=shift_id
        self.personnel_id=personnel_id
        self.begin=shift_begin_date
        self.repeat=shift_repeat_interval
        self.hours=shift_hours
        self.dayshift=dayshift
        self.ea=emergency_area_assigned
        self.name=name
    def get_id(self):
        return self.shift_id
    def get_personnel_id(self):
        return self.personnel_id
    def get_begin(self):
        return self.begin
    def get_repeat(self):
        return self.repeat
    def get_hours(self):
        return self.hours
    def get_dayshift(self):
        return self.dayshift
    def get_ea(self):
        return self.ea
    def get_name(self):
        return self.name
