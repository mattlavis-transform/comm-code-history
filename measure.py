import os
import itertools
from classes.sqlite_helper import DatabaseLite
from measure_condition import MeasureCondition
from strings import Strings


class Measure(object):
    def __init__(self):
        self.database_filename = os.path.join(
            os.getcwd(), "db", "commodity-code-history.db")
        self.measure_conditions = []
        self.measure_condition_ids = []
        self.measure_conditions_list = []
        self.condition_permutations = []
        self.features_universal_waiver = False
        self.strings = Strings()

    def get_excise_vat(self):
        if self.measure_type_id == "306":
            self.vat = False
            self.excise = True
        elif self.measure_type_id == "305":
            self.vat = True
            self.excise = False
        else:
            self.vat = False
            self.excise = False

    def count_condition_codes(self):
        self.condition_codes = []
        if len(self.measure_conditions) > 0:
            for mc in self.measure_conditions:
                if mc.condition_code not in self.condition_codes:
                    self.condition_codes.append(mc.condition_code)

        if len(self.condition_codes) > 1:
            self.complex = True
        else:
            self.complex = False

    def check_shared_conditions(self):
        entities = []
        if self.measure_sid == 20169904:
            a = 1
        self.contains_shared_conditions = False
        if len(self.measure_conditions) > 0:
            for mc in self.measure_conditions:
                if mc.positive:
                    if mc.condition_class != self.strings.univeral_waiver_string:
                        entity = {
                            "document_code": mc.document_code,
                            "condition_duty_amount": mc.condition_duty_amount
                        }
                        if entity in entities:
                            self.contains_shared_conditions = True
                            break
                        else:
                            entities.append(entity)

    def get_condition_permutations(self):
        if len(self.measure_conditions) > 0:
            if self.complex and self.contains_shared_conditions:
                self.get_condition_permutations_complex()
            else:
                self.get_condition_permutations_simple()

    def get_condition_permutations_complex(self):
        perm_object = None
        entities = []

        # Count the instances first
        for mc in self.measure_conditions:
            if mc.positive:
                entity = {
                    "document_code": mc.document_code,
                    "condition_duty_amount": mc.condition_duty_amount
                }
                mc.instance_count = 0
                for mc2 in self.measure_conditions:
                    if mc2.positive:
                        entity2 = {
                            "document_code": mc2.document_code,
                            "condition_duty_amount": mc2.condition_duty_amount
                        }
                        if entity == entity2:
                            mc.instance_count += 1

        # Then group them, starting with the multiples first
        lst_sorted = sorted(self.measure_conditions, key=lambda x: x.condition_class_priority, reverse=True)
        lst_sorted = sorted(self.measure_conditions, key=lambda x: x.instance_count, reverse=True)

        entities = []
        single_perms = []
        single_perms2 = []
        perm_object = {
            "condition_code": self.strings.not_applicable,
            "permutations": []
        }
        for mc in lst_sorted:
            if mc.positive:
                if mc.condition_class != self.strings.univeral_waiver_string:
                    entity = {
                        "document_code": mc.document_code,
                        "condition_duty_amount": mc.condition_duty_amount
                    }
                    if entity not in entities:
                        if mc.instance_count > 1:
                            perm = [mc.measure_condition_sid]
                            perm_object["permutations"].append(perm)
                        else:
                            single_perms.append(mc.measure_condition_sid)
                            single_perms2.append(mc)

                        entities.append(entity)

        condition_codes = []

        if len(single_perms2) > 0:
            single_perms2 = sorted(single_perms2, key=lambda x: x.condition_code, reverse=False)
            for perm in single_perms2:
                condition_codes.append(perm.condition_code)

            condition_codes = sorted(list(set(condition_codes)))

            single_perms3 = {}
            for condition_code in condition_codes:
                single_perms3[condition_code] = []

            for perm in single_perms2:
                single_perms3[perm.condition_code].append(perm.measure_condition_sid)
            a = 1

            single_perms4 = []
            for condition_code in single_perms3:
                single_perms4.append(single_perms3[condition_code])

            perm1_list = single_perms4[0]
            perm2_list = single_perms4[1]

            for r in itertools.product(perm1_list, perm2_list):
                single_perms = [r[0], r[1]]
                perm_object["permutations"].append(single_perms)
                print(str(r[0]) + " : " + str(r[1]))

            a = 1

        # if len(single_perms) > 0:
        #     perm_object["permutations"].append(single_perms)

        self.condition_permutations.append(perm_object)

    def get_condition_permutations_simple(self):
        last_condition_code = ""
        perm_object = None
        for mc in self.measure_conditions:
            if mc.positive:
                if mc.condition_class != self.strings.univeral_waiver_string:
                    if last_condition_code != mc.condition_code:
                        if perm_object is not None:
                            self.condition_permutations.append(perm_object)

                        perm_object = {
                            "condition_code": mc.condition_code,
                            "permutations": [
                                [mc.measure_condition_sid]
                            ]
                        }
                    else:
                        perm_object["permutations"].append([mc.measure_condition_sid])

                    last_condition_code = mc.condition_code

        self.condition_permutations.append(perm_object)

    def as_dict(self):
        measure = {
            "id": self.measure_sid,
            "type": "measure",
            "attributes": {
                "id": self.measure_sid,
                "origin": "eu",
                "effective_start_date": self.validity_start_date,
                "effective_end_date": self.validity_end_date,
                "import": True,
                "excise": self.excise,
                "vat": self.vat,
                "reduction_indicator": self.reduction_indicator,
                "meursing": False,
                "features_universal_waiver": self.features_universal_waiver,
                "resolved_duty_expression": ""
            },
            "relationships": {
                "measure_type": {
                    "data": {
                        "id": self.measure_type_id,
                        "type": "measure_type"
                    }
                },
                "geographical_area": {
                    "data": {
                        "id": self.geographical_area_id,
                        "type": "geographical_area"
                    }
                },
                "measure_conditions": {
                    "data": self.measure_condition_ids
                },
                "measure_condition_permutations": {
                    "data": self.condition_permutations
                }
            }
        }
        return measure
