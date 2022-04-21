import os
from classes.sqlite_helper import DatabaseLite
from measure_condition import MeasureCondition
from measure import Measure
from geographical_area import GeographicalArea
from measure_type import MeasureType
from strings import Strings


class Commodity(object):
    def __init__(self, goods_nomenclature_item_id):
        self.database_filename = os.path.join(os.getcwd(), "db", "commodity-code-history.db")
        self.goods_nomenclature_item_id = goods_nomenclature_item_id

        self.measures = []
        self.measure_conditions = []
        self.measures_list = []
        self.measure_conditions_list = []
        self.geographical_areas = []
        self.geographical_areas_list = []
        self.measure_types = []
        self.measure_types_list = []

        self.strings = Strings()

        self.get_commodity_detail()
        if self.valid:
            self.get_ancestry_string()
            self.get_measure_conditions()
            self.get_measures()
            self.get_geographical_areas()
            self.get_measure_types()
            self.assign_measure_conditions()
            self.check_for_universal_waiver()
            self.get_condition_permutations()
            self.get_measures_dict()

    def check_for_universal_waiver(self):
        for m in self.measures:
            for mc in m.measure_conditions:
                if mc.condition_class == self.strings.univeral_waiver_string:
                    m.features_universal_waiver = True
                    break

    def get_measures_dict(self):
        for m in self.measures:
            self.measures_list.append(m.as_dict())

    def get_condition_permutations(self):
        for m in self.measures:
            m.count_condition_codes()
            m.check_shared_conditions()
            m.get_condition_permutations()

    def get_ancestry_string(self):
        self.ancestry_array = self.ancestry_array.replace("[", "")
        self.ancestry_array = self.ancestry_array.replace("]", "")
        self.ancestry_array = self.ancestry_array.split(",")
        self.ancestry_array.append(str(self.goods_nomenclature_sid))
        self.ancestry_string = ",".join(self.ancestry_array)
        
    def get_commodity_detail(self):
        sql = "select * from commodities c where goods_nomenclature_item_id = '" + self.goods_nomenclature_item_id + "' and productline_suffix = '80'"
        db = DatabaseLite(self.database_filename)
        rows = db.run_query(sql)
        if len(rows) > 0:
            self.valid = True
            row = rows[0]
            self.goods_nomenclature_sid = row[0]
            self.goods_nomenclature_item_id = row[1]
            self.productline_suffix = row[2]
            self.description = row[3]
            self.ancestry_array = row[4]
        else:
            self.valid = False

    def get_measure_conditions(self):
        sql = "select mc.*, ma.description as action_code_description, " \
        "dc.certificate_type_description, dc.certificate_description, mcc.description as condition_code_description " \
        "from measures m, measure_actions ma, measure_condition_codes mcc, " \
        "measure_conditions mc " \
        "left outer join document_codes dc " \
        "on mc.certificate_type_code = dc.certificate_type_code  " \
        "and mc.certificate_code = dc.certificate_code  " \
        "where m.goods_nomenclature_sid in (" + self.ancestry_string + ") " \
        "and m.measure_sid = mc.measure_sid and mc.action_code = ma.action_code " \
        "and mc.condition_code = mcc.condition_code  " \
        "order by measure_sid, condition_code, component_sequence_number;"

        db = DatabaseLite(self.database_filename)
        rows = db.run_query(sql)
        if len(rows) > 0:
            for row in rows:
                measure_condition = MeasureCondition()
                measure_condition.measure_condition_sid = row[0]
                measure_condition.measure_sid = row[1]
                measure_condition.condition_code = row[2]
                measure_condition.component_sequence_number = row[3]
                measure_condition.certificate_type_code = row[4]
                measure_condition.certificate_code = row[5]
                measure_condition.condition_duty_amount = row[6]
                measure_condition.condition_monetary_unit_code = row[7]
                measure_condition.condition_measurement_unit_code = row[8]
                measure_condition.condition_measurement_unit_qualifier_code = row[9]
                measure_condition.action_code = row[10]
                measure_condition.action_code_description = row[11]
                measure_condition.certificate_type_description = row[12]
                measure_condition.certificate_description = row[13]
                measure_condition.condition_code_description = row[14]
                measure_condition.populate()

                self.measure_conditions.append(measure_condition)

    def get_measures(self):
        sql = "select * from measures m where goods_nomenclature_sid in (" + self.ancestry_string + ") " \
        "and validity_start_date <= current_date " \
        "and (validity_end_date is null or validity_end_date >= current_date) " \
        "order by measure_type_id, geographical_area_id;"
        db = DatabaseLite(self.database_filename)
        rows = db.run_query(sql)
        if len(rows) > 0:
            for row in rows:
                measure = Measure()
                measure.ancestry_string = self.ancestry_string
                measure.measure_sid = row[0]
                measure.goods_nomenclature_item_id = row[1]
                measure.geographical_area_id = row[2]
                measure.measure_type_id = row[3]
                measure.measure_generating_regulation_id = row[4]
                measure.ordernumber = row[5]
                measure.reduction_indicator = row[6]
                measure.additional_code_type_id = row[7]
                measure.additional_code_id = row[8]
                measure.additional_code = row[9]
                measure.measure_generating_regulation_role = row[10]
                measure.justification_regulation_role = row[11]
                measure.justification_regulation_id = row[12]
                measure.stopped_flag = row[13]
                measure.geographical_area_sid = row[14]
                measure.goods_nomenclature_sid = row[15]
                measure.additional_code_sid = row[16]
                measure.export_refund_nomenclature_sid = row[17]
                measure.validity_start_date = row[18]
                measure.validity_end_date = row[19]
                measure.additional_code_sid = row[20]
                measure.get_excise_vat()

                self.measures.append(measure)
                
        return self.measures
    
    def get_geographical_areas(self):
        self.geographical_areas = []
        sql = "select distinct ga.geographical_area_id, ga.description " \
        "from measures m, geographical_areas ga  " \
        "where goods_nomenclature_sid in (" + self.ancestry_string + ") " \
        "and validity_start_date <= current_date " \
        "and (validity_end_date is null or validity_end_date >= current_date) " \
        "and ga.geographical_area_id = m.geographical_area_id  " \
        "order by 1;"

        db = DatabaseLite(self.database_filename)
        rows = db.run_query(sql)
        if len(rows) > 0:
            for row in rows:
                ga = GeographicalArea()
                ga.geographical_area_id = row[0]
                ga.description = row[1]
                self.geographical_areas.append(ga)
                
        for ga in self.geographical_areas:
            self.geographical_areas_list.append(ga.as_dict())
    
    def get_measure_types(self):
        self.measure_types = []
        
        sql = "select distinct mt.measure_type_id, mt.measure_type_description as description " \
        "from measures m, measure_types mt " \
        "where goods_nomenclature_sid in (" + self.ancestry_string + ") " \
        "and m.validity_start_date <= current_date " \
        "and (m.validity_end_date is null or m.validity_end_date >= current_date) " \
        "and mt.measure_type_id = m.measure_type_id " \
        "order by 1;"
        
        db = DatabaseLite(self.database_filename)
        rows = db.run_query(sql)
        if len(rows) > 0:
            for row in rows:
                mt = MeasureType()
                mt.measure_type_id = row[0]
                mt.description = row[1]
                self.measure_types.append(mt)
                
        for mt in self.measure_types:
            self.measure_types_list.append(mt.as_dict())

    def assign_measure_conditions(self):
        for mc in self.measure_conditions:
            if mc.measure_condition_sid == 20162032:
                a = 1
            for m in self.measures:
                if m.measure_sid == mc.measure_sid:
                    m.measure_conditions.append(mc)
                    m.measure_condition_ids.append(mc.id_as_dict())
                    self.measure_conditions_list.append(mc.as_dict())
                    break

    def as_dict(self):
        self.data = {
            "id": self.goods_nomenclature_sid,
            "type": "commodity",
            "attributes": {
                "producline_suffix": self.productline_suffix,
                "description": self.description,
                "number_indents": 999,
                "goods_nomenclature_item_id": self.goods_nomenclature_item_id,
                "bti_url": "tbc",
                "formatted_description": self.description,
                "description_plain": self.description,
                "consigned": False,
                "consigned_from": None,
                "basic_duty_rate": "tbc",
                "meursing_code": False,
                "declarable": False
            },
            "relationships": {
                "tbc": "tbc"
            },
            "meta": {
                "tbc": "tbc"
            }
        }
        ret = {
            "data": self.data,
            "included": self.measures_list + self.measure_conditions_list + self.geographical_areas_list + self.geographical_areas_list + self.measure_types_list
        }
        return ret
     