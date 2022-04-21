class QuotaDefinition(object):
    def __init__(self, row):
        self.row = row
        self.quota_balance_events = []
        self.quota_subsidiary_events = []
        self.populate()
        
    def populate(self):
        self.quota_order_number_id = self.row[0]
        self.quota_definition_sid = self.row[1]
        self.validity_start_date = self.row[2]
        self.validity_end_date = self.row[3]
        self.initial_volume = self.row[4]
        self.measurement_unit_code = self.row[5]
        self.measurement_unit_qualifier_code = self.row[6]
        self.maximum_precision = self.row[7]
        self.critical_state = self.row[8]
        self.critical_threshold = self.row[9]

    def as_dict(self):
        ret = {
            "quota_order_number_id": self.quota_order_number_id,
            "quota_definition_sid": self.quota_definition_sid,
            "validity_start_date": self.validity_start_date,
            "validity_end_date": self.validity_end_date,
            "initial_volume": self.initial_volume,
            "measurement_unit_code": self.measurement_unit_code,
            "measurement_unit_qualifier_code": self.measurement_unit_qualifier_code,
            "maximum_precision": self.maximum_precision,
            "critical_state": self.critical_state,
            "critical_threshold": self.critical_threshold,
            "quota_balance_events": self.quota_balance_events,
            "quota_subsidiary_events": self.quota_subsidiary_events
        }
        return ret
     