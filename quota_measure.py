class QuotaMeasure(object):
    def __init__(self, row):
        self.row = row
        self.populate()

    def populate(self):
        self.goods_nomenclature_item_id = self.row[0]
        self.commodity_description = self.row[1]
        self.measure_sid = self.row[2]
        self.measure_type_description = self.row[3]
        self.geographical_area_id = self.row[4]
        self.geographical_area_description = self.row[5]
        self.validity_start_date = self.row[6]
        self.validity_end_date = self.row[7]
        self.duty = self.row[8]

    def as_dict(self):
        ret = {
            "goods_nomenclature_item_id": self.goods_nomenclature_item_id,
            "commodity_description": self.commodity_description,
            "measure_sid": self.measure_sid,
            "measure_type_description": self.measure_type_description,
            "geographical_area_id": self.geographical_area_id,
            "geographical_area_description": self.geographical_area_description,
            "validity_start_date": self.validity_start_date,
            "validity_start_date": self.validity_start_date,
            "validity_end_date": self.validity_end_date,
            "duty": self.duty
        }
        return ret
