# json_handler.py

import json
import os

class SchemaHandler:
    def __init__(self, file_path):
        self.file_path = file_path
    
    def load_schema(self):
        with open(self.file_path, 'r', encoding='utf-8') as file:
            return json.load(file)

class FileWriter:
    def __init__(self, directory):
        self.directory = directory

    def generate_and_write_json_with_jsonschema(self, schema, omit_values):
        def generate_and_write(schema, omit_values, path=""):
            if 'type' not in schema:
                return None
            if 'enum' in schema:
                if omit_values is True:
                    return None
                else:
                    return schema['enum']
            if schema['type'] == 'object':
                obj = {}
                required = schema.get('required', [])
                for prop, subschema in schema.get('properties', {}).items():
                    if prop == "Visible":
                        for key in subschema.get('properties', {}):
                            visible_data = {
                                "MPItemFeedHeader": {
                                    "businessUnit": ["WALMART_CA", "WALMART_US", "ASDA_GM"],
                                    "locale": ["en"],
                                    "version": ["5.0.20230926-17_34_53-api"]
                                },
                                "MPItem": [
                                    {
                                        "Visible": {
                                            key: generate_and_write(subschema['properties'][key], omit_values)
                                        },
                                        "Orderable": generate_and_write(schema['properties']['Orderable'], omit_values)
                                    }
                                ]
                            }
                            escaped_key = key.replace("/", "_")
                            file_path = os.path.join(self.directory, f"{escaped_key}.json")
                            os.makedirs(os.path.dirname(file_path), exist_ok=True)
                            with open(file_path, 'w') as json_file:
                                json.dump(visible_data, json_file, indent=4)
                    else:
                        obj[prop] = generate_and_write(subschema, omit_values, path)
                        if prop in required and obj[prop] is None:
                            obj[prop] = generate_and_write(subschema, omit_values, path)
                return obj
            if omit_values is True:
                if schema['type'] == 'array':
                    if schema['items']['type'] == 'object':
                        return [[generate_and_write(schema['items'], omit_values)]]
                    else:
                        return None
                if schema['type'] in ['string', 'integer', 'boolean', 'number']:
                    return None
                return None
            else:
                if schema['type'] == 'array':
                    return [generate_and_write(schema['items'], omit_values)]
                if schema['type'] in ['string', 'integer', 'boolean', 'number']:
                    return schema.get('examples', [0] if schema['type'] in ['integer', 'number'] else ["example" if schema['type'] == 'string' else True])
                return None
    
        generate_and_write(schema, omit_values)
