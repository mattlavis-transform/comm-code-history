class QuotaOrderNumberOriginExclusion(object):
    def __init__(self, row):
        self.row = row
        self.populate()

    def populate(self):
        self.excluded_geographical_area_sid = self.row[0]
        self.description = self.row[1]
        self.geographical_area_id = self.row[2]
        self.quota_order_number_id = self.row[3]
        self.quota_order_number_sid = self.row[4]
        self.quota_order_number_origin_sid = self.row[5]

    def as_dict(self):
        ret = {
            "excluded_geographical_area_sid": self.excluded_geographical_area_sid,
            "description": self.description,
            "geographical_area_id": self.geographical_area_id,
            "quota_order_number_id": self.quota_order_number_id,
            "quota_order_number_sid": self.quota_order_number_sid,
            "quota_order_number_origin_sid": self.quota_order_number_origin_sid
        }
        return ret
