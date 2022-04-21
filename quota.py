import os
from classes.database import Database
from quota_order_number_origin import QuotaOrderNumberOrigin
from quota_definition import QuotaDefinition
from quota_measure import QuotaMeasure
from quota_balance_event import QuotaBalanceEvent
from quota_subsidiary_event import QuotaSubsidiaryEvent


class Quota(object):
    def __init__(self, quota_order_number_id):
        self.quota_order_number_id = quota_order_number_id
        self.measures = []

    def get_quota(self):
        self.get_core()
        if self.valid:
            self.get_origins()
            self.get_definitions()
            self.get_balance_events()
            self.get_subsidiary_events()

    def get_quota_measures(self):
        self.get_core()
        if self.valid:
            self.get_origins()
            self.get_measures()
            
    def get_measures(self):
        sql = """
        select m.goods_nomenclature_item_id, c.description as commodity_description,
        m.measure_sid, mtd.description as measure_type_description,
        m.geographical_area_id, ga.description as geographical_area_description,
        m.validity_start_date, m.validity_end_date, m.duty
        from utils.materialized_all_duties m, measure_type_descriptions mtd,
        utils.materialized_commodities c, utils.geographical_areas ga 
        where m.measure_type_id = mtd.measure_type_id
        and m.goods_nomenclature_sid = c.goods_nomenclature_sid 
        and m.geographical_area_id = ga.geographical_area_id 
        and ordernumber = %s
        order by m.validity_start_date desc, m.goods_nomenclature_item_id;
        """
        d = Database()
        params = [
            self.quota_order_number_id
        ]
        rows = d.run_query(sql, params)
        for row in rows:
            m = QuotaMeasure(row)
            self.measures.append(m.as_dict())

    def get_core(self):
        sql = """
        select validity_start_date, validity_end_date 
        from quota_order_numbers qon where quota_order_number_id = %s;
        """
        d = Database()
        params = [
            self.quota_order_number_id
        ]
        rows = d.run_query(sql, params)
        if rows:
            row = rows[0]
            self.validity_start_date = row[0]
            self.validity_end_date = row[1]
            self.valid = True
        else:
            self.valid = False

    def get_origins(self):
        sql = """
        select qono.geographical_area_id, ga.description, qono.validity_start_date, qono.validity_end_date
        from quota_order_number_origins qono, quota_order_numbers qon, utils.geographical_areas ga
        where qono.quota_order_number_sid = qon.quota_order_number_sid 
        and ga.geographical_area_sid = qono.geographical_area_sid 
        and qon.quota_order_number_id = %s;"""
        d = Database()
        params = [
            self.quota_order_number_id
        ]
        rows = d.run_query(sql, params)
        self.quota_order_number_origins = []
        for row in rows:
            qono = QuotaOrderNumberOrigin(row)
            self.quota_order_number_origins.append(qono.as_dict())
    
    def get_definitions(self):
        sql = """select quota_order_number_id, quota_definition_sid, validity_start_date, validity_end_date,
        initial_volume, measurement_unit_code, measurement_unit_qualifier_code,
        maximum_precision, critical_state, critical_threshold 
        from quota_definitions qd
        where quota_order_number_id = %s
        and validity_start_date <= current_date
        order by validity_start_date desc;
        """

        d = Database()
        params = [
            self.quota_order_number_id
        ]
        rows = d.run_query(sql, params)
        self.quota_definitions = []
        for row in rows:
            qd = QuotaDefinition(row)
            self.quota_definitions.append(qd.as_dict())

    def get_balance_events(self):
        sql = """select qbe.quota_definition_sid, qbe.occurrence_timestamp, qbe.last_import_date_in_allocation,
        qbe.old_balance, qbe.new_balance, qbe.imported_amount 
        from quota_balance_events qbe, quota_definitions qd 
        where qbe.quota_definition_sid = qd.quota_definition_sid 
        and qd.quota_order_number_id = %s
        order by qd.validity_start_date desc, occurrence_timestamp desc;
        """

        d = Database()
        params = [
            self.quota_order_number_id
        ]
        rows = d.run_query(sql, params)
        self.quota_balance_events = []
        for row in rows:
            qbe = QuotaBalanceEvent(row)
            self.quota_balance_events.append(qbe.as_dict())

        self.assign_balance_events_to_definitions()
            
    def get_subsidiary_events(self):
        sql = """
        select distinct qd.quota_definition_sid, ev.critical_state_change_date as stamp, 'Critical state change' as event_type, ev.critical_state as state
        from quota_critical_events ev, quota_definitions qd
        where qd.quota_definition_sid = ev.quota_definition_sid 
        and qd.quota_order_number_id = %s

        union

        select qd.quota_definition_sid, ev.exhaustion_date as stamp, 'Exhaustion event' as event_type, null as state
        from quota_exhaustion_events ev, quota_definitions qd
        where qd.quota_definition_sid = ev.quota_definition_sid 
        and qd.quota_order_number_id = %s

        union

        select qd.quota_definition_sid, ev.reopening_date as stamp, 'Reopening event' as event_type, null as state
        from quota_reopening_events ev, quota_definitions qd
        where qd.quota_definition_sid = ev.quota_definition_sid 
        and qd.quota_order_number_id = %s
        
        union

        select qd.quota_definition_sid, ev.unblocking_date as stamp, 'Unblocking event' as event_type, null as state
        from quota_unblocking_events ev, quota_definitions qd
        where qd.quota_definition_sid = ev.quota_definition_sid 
        and qd.quota_order_number_id = %s

        union

        select qd.quota_definition_sid, ev.unsuspension_date as stamp, 'Unsuspension event' as event_type, null as state
        from quota_unsuspension_events ev, quota_definitions qd
        where qd.quota_definition_sid = ev.quota_definition_sid 
        and qd.quota_order_number_id = %s

        order by 1 desc, 2 desc;
        """
        d = Database()
        params = [
            self.quota_order_number_id,
            self.quota_order_number_id,
            self.quota_order_number_id,
            self.quota_order_number_id,
            self.quota_order_number_id
        ]
        rows = d.run_query(sql, params)
        self.quota_subsidiary_events = []
        for row in rows:
            ev = QuotaSubsidiaryEvent(row)
            self.quota_subsidiary_events.append(ev.as_dict())

        self.assign_subsidiary_events_to_definitions()

    def assign_balance_events_to_definitions(self):
        for qbe in self.quota_balance_events:
            for qd in self.quota_definitions:
                if qbe["quota_definition_sid"] == qd["quota_definition_sid"]:
                    qd["quota_balance_events"].append(qbe)
                    break

    def assign_subsidiary_events_to_definitions(self):
        for qse in self.quota_subsidiary_events:
            for qd in self.quota_definitions:
                if qse["quota_definition_sid"] == qd["quota_definition_sid"]:
                    qd["quota_subsidiary_events"].append(qse)
                    break
    
    def as_dict(self):
        if self.valid:
            self.data = {
                "id": self.quota_order_number_id,
                "validity_start_date": self.validity_start_date,
                "validity_end_date": self.validity_end_date,
                "type": "quota",
                "quota_order_number_origins": self.quota_order_number_origins,
                "quota_definitions": self.quota_definitions
            }
            ret = {
                "data": self.data
            }
        else:
            ret = {}
            
        return ret
     
    
    def measures_as_dict(self):
        if self.valid:
            self.data = {
                "id": self.quota_order_number_id,
                "validity_start_date": self.validity_start_date,
                "validity_end_date": self.validity_end_date,
                "type": "quota",
                "quota_order_number_origins": self.quota_order_number_origins,
                "measures": self.measures
            }
            ret = {
                "data": self.data
            }
        else:
            ret = {}
            
        return ret
     