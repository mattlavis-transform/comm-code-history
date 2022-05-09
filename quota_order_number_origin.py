class QuotaOrderNumberOrigin(object):
    def __init__(self, row):
        self.row = row
        self.populate()

    def populate(self):
        self.geographical_area_id = self.row[0]
        self.description = self.row[1]
        self.validity_start_date = self.row[2]
        self.validity_end_date = self.row[3]
        self.quota_order_number_origin_sid = self.row[4]
        self.exclusions = []

    def as_dict(self):
        ret = {
            "geographical_area_id": self.geographical_area_id,
            "description": self.description,
            "validity_start_date": self.validity_start_date,
            "validity_end_date": self.validity_end_date,
            "quota_order_number_origin_sid": self.quota_order_number_origin_sid,
            "exclusions": []
        }
        return ret
