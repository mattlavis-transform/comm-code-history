import os
from strings import Strings


class MeasureCondition(object):
    def __init__(self):
        self.strings = Strings()
        self.instance_count = 1
        self.condition_class_priority = 0
    
    def populate(self):
        self.get_positive_negative()
        self.get_document_code()
        self.get_requirement()
        self.get_class()
        
    def get_class(self):
        exemptions = [
            "999L",
            "C084"
        ]
        universal_waivers = [
            "999L"
        ]
        if self.positive:
            if self.document_code is None:
                self.condition_class = "threshold"
                self.condition_class_priority = 2
            elif self.document_code in universal_waivers:
                self.condition_class = self.strings.univeral_waiver_string
            elif self.document_code[0] == "Y" or self.document_code in exemptions:
                self.condition_class = "exemption"
                self.condition_class_priority = 3
            else:
                self.condition_class = "document"
                self.condition_class_priority = 4
        else:
            self.condition_class = "negative"
            self.condition_class_priority = 1
            
    def get_positive_negative(self):
        if self.action_code >= "24":
            self.positive = True
        else:
            self.positive = False

    def get_document_code(self):
        if self.certificate_type_code is not None:
            self.document_code = self.certificate_type_code + self.certificate_code
        else:
            self.document_code = None

    def get_requirement(self):
        self.unit_string = ""
        self.unit_abbreviation_string = ""
        self.qualifier_string = ""
        if self.positive:
            if self.condition_measurement_unit_code is not None:
                self.unit = self.condition_measurement_unit_code
                if self.condition_measurement_unit_qualifier_code is not None:
                    self.unit += self.condition_measurement_unit_qualifier_code
                    self.qualifier_string = self.strings.qualifiers[self.unit]["description"]
                    
                self.unit_string = self.strings.units[self.unit]["description"]
                self.unit_abbreviation_string = self.strings.abbreviations[self.unit]["abbreviation"]

            if self.certificate_type_code is not None:
                self.requirement = self.certificate_type_description + ": " + self.certificate_description
            else:
                self.requirement = "<span>{amount}</span> <abbr title='{unit}'>{unit_abbreviation}</abbr>".format(
                    amount = str(self.condition_duty_amount),
                    unit = self.unit_string,
                    unit_abbreviation = self.unit_abbreviation_string
                )
        else:
            self.requirement = None

    def as_dict(self):
        ret = {
            "id": self.measure_condition_sid,
            "type": "measure_condition",
            "attributes": {
                "action": self.action_code_description,
                "action_code": self.action_code,
                "certificate_description": self.certificate_description,
                "condition": self.condition_code + ": " + self.condition_code_description,
                "condition_code": self.condition_code,
                "condition_duty_amount": self.condition_duty_amount,
                "condition_measurement_unit_code": self.condition_measurement_unit_code,
                "condition_measurement_unit_qualifier_code": self.condition_measurement_unit_qualifier_code,
                "condition_monetary_unit_code": self.condition_monetary_unit_code,
                "document_code": self.document_code,
                "duty_expression": "tbc",
                "monetary_unit_abbreviation": "tbc",
                "requirement": self.requirement,
                "condition_class": self.condition_class
            }
        }
        return ret
    
    def id_as_dict(self):
        ret = {
            "id": self.measure_condition_sid,
            "type": "measure_condition"
        }
        return ret