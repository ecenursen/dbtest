class hospital_personnel:
    def __init__(self,personnel_id,worker_name,job_title,job_experience,work_days,phone_num,working_field,hospital_worked,tckn,hospital):
        self.personnel_id=personnel_id
        self.worker_name=worker_name
        self.job_title=job_title
        self.job_experience=job_experience
        self.work_days=work_days
        self.phone_num=phone_num
        self.working_field=working_field
        self.hospital_worked=hospital_worked
        self.tckn=tckn
        self.hospital =hospital

    def get_id(self):
        return self.personnel_id
    def get_name(self):
        return self.worker_name
    def get_title(self):
        return self.job_title
    def get_exp(self):
        return self.job_experience
    def get_days(self):
        return self.work_days
    def get_number(self):
        return self.phone_num
    def get_field(self):
        return self.working_field
    def get_hospital(self):
        return self.hospital_worked
    def get_tckn(self):
        return self.tckn
    def get_hospital_name(self):
        return self.hospital