class QuotaOrderNumberOrigin(object):
    def __init__(self, row):
        self.row = row
        self.populate()
        
    def populate(self):
        self.geographical_area_id = self.row[0]
        self.description = self.row[1]
        self.validity_start_date = self.row[2]
        self.validity_end_date = self.row[3]

    def as_dict(self):
        ret = {
            "geographical_area_id": self.geographical_area_id,
            "description": self.description,
            "validity_start_date": self.validity_start_date,
            "validity_end_date": self.validity_end_date
        }
        return ret
     