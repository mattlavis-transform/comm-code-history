from classes.database import Database
from quota_balance_event import QuotaBalanceEvent


class QuotaDefinition(object):
    def __init__(self, row=None):
        self.quota_balance_events = []
        self.quota_subsidiary_events = []
        self.quota_periods = []

        if row is not None:
            self.row = row
            self.populate()

    def populate(self):
        self.quota_order_number_id = self.row[0]
        self.quota_definition_sid = self.row[1]
        self.validity_start_date = self.row[2].strftime("%Y-%m-%dT00:00:00.000Z")  # "1972-01-01T00:00:00.000Z"
        self.validity_end_date = self.row[3].strftime("%Y-%m-%dT00:00:00.000Z")  # "1972-01-01T00:00:00.000Z"
        self.initial_volume = self.row[4]
        self.measurement_unit_code = self.row[5]
        self.measurement_unit_qualifier_code = self.row[6]
        self.maximum_precision = self.row[7]
        self.critical_state = self.row[8]
        self.critical_threshold = self.row[9]

    def get_quota_definition(self):
        sql = """
        select quota_order_number_id, validity_start_date, validity_end_date , 
        quota_order_number_sid, initial_volume, measurement_unit_code, measurement_unit_qualifier_code,
        maximum_precision, critical_state, critical_threshold 
        from quota_definitions where quota_definition_sid = %s
        """
        d = Database()
        params = [
            self.quota_definition_sid
        ]
        rows = d.run_query(sql, params)
        if rows:
            row = rows[0]
            self.quota_order_number_id = row[0]
            self.validity_start_date = row[1]
            self.validity_end_date = row[2]
            self.quota_order_number_sid = row[3]
            self.initial_volume = row[4]
            self.measurement_unit_code = row[5]
            self.measurement_unit_qualifier_code = row[6]
            self.maximum_precision = row[7]
            self.critical_state = row[8]
            self.critical_threshold = row[9]

            self.get_balance_events()

    def get_balance_events(self):
        sql = """select qbe.quota_definition_sid, qbe.occurrence_timestamp, qbe.last_import_date_in_allocation,
        qbe.old_balance, qbe.new_balance, qbe.imported_amount 
        from quota_balance_events qbe
        where qbe.quota_definition_sid = %s
        order by occurrence_timestamp desc;
        """
        d = Database()
        params = [
            self.quota_definition_sid
        ]
        rows = d.run_query(sql, params)
        self.quota_balance_events = []
        for row in rows:
            qbe = QuotaBalanceEvent(row)
            self.quota_balance_events.append(qbe.as_dict())

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
            "quota_subsidiary_events": self.quota_subsidiary_events,
            "quota_periods": self.quota_periods
        }
        return ret
