import json 
import os


class Strings(object):
    def __init__(self):
        self.univeral_waiver_string = "universal_waiver"
        self.not_applicable = "n/a"

        # Get units
        path = os.path.join(os.getcwd(), "units.json")
        with open(path, "r") as f:
            self.units = json.load(f)

        # Get qualifiers
        path = os.path.join(os.getcwd(), "qualifiers.json")
        with open(path, "r") as f:
            self.qualifiers = json.load(f)

        # Get abbreviations
        path = os.path.join(os.getcwd(), "abbreviations.json")
        with open(path, "r") as f:
            self.abbreviations = json.load(f)

