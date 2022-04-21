class QuotaBalanceEvent(object):
    def __init__(self, row):
        self.row = row
        self.populate()
        
    def populate(self):
        self.quota_definition_sid = self.row[0]
        self.occurrence_timestamp = self.row[1]
        self.last_import_date_in_allocation = self.row[2]
        self.old_balance = self.row[3]
        self.new_balance = self.row[4]
        self.imported_amount = self.row[5]

    def as_dict(self):
        ret = {
            "quota_definition_sid": self.quota_definition_sid,
            "occurrence_timestamp": self.occurrence_timestamp,
            "last_import_date_in_allocation": self.last_import_date_in_allocation,
            "old_balance": self.old_balance,
            "new_balance": self.new_balance,
            "imported_amount": self.imported_amount
        }
        return ret
     