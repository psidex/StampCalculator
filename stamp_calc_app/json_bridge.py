import json

def get_dict_from_file(filename):
    with open(filename, "r") as in_file:
        return json.load(in_file)

def dump_dict_to_file(data, filename):
    with open(filename, "w") as out_file:
        json.dump(data, out_file)

def get_name_by_value(data, value):
    for name, v in data.items():
        if v["value"] == value:
            return name
