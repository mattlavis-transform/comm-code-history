class QuotaPeriod(object):
    def __init__(self, row):
        self.row = row
        self.populate()

    def populate(self):
        self.quota_definition_sid = self.row[0]
        self.start_date = self.row[1]
        self.end_date = self.row[2]
        self.description = self.row[3]
        self.period_type = self.row[4]

    def as_dict(self):
        ret = {
            "quota_definition_sid": self.quota_definition_sid,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "description": self.description,
            "period_type": self.period_type
        }
        return ret
