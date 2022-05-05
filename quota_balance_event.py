import datetime

class QuotaBalanceEvent(object):
    def __init__(self, row):
        self.row = row
        self.populate()
        
    def populate(self):
        self.quota_definition_sid = self.row[0]
        self.occurrence_timestamp = self.row[1].strftime("%Y-%m-%dT00:00:00.000Z")  # "1972-01-01T00:00:00.000Z"
        if self.row[2] is None:
            self.last_import_date_in_allocation = None
        else:
            self.last_import_date_in_allocation = self.row[2].strftime("%Y-%m-%dT00:00:00.000Z")  # "1972-01-01T00:00:00.000Z"
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
     