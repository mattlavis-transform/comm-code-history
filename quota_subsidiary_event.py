class QuotaSubsidiaryEvent(object):
    def __init__(self, row):
        self.row = row
        self.populate()
        
    def populate(self):
        self.quota_definition_sid = self.row[0]
        self.timestamp = self.row[1]
        self.event_type = self.row[2]
        self.state = self.row[3]

    def as_dict(self):
        ret = {
            "quota_definition_sid": self.quota_definition_sid,
            "timestamp": self.timestamp,
            "event_type": self.event_type,
            "state": self.state
        }
        return ret
