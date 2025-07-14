# schema_handler.py

import os
import json

class SchemaFileSplitter:
    def __init__(self, schema_file_path, output_directory):
        self.schema_file_path = schema_file_path
        self.output_directory = output_directory

    def split_schema_file(self):
        # Create output directory if it doesn't exist
        os.makedirs(self.output_directory, exist_ok=True)

        with open(self.schema_file_path, 'r', encoding='utf-8') as schema_file:
            schema_data = json.load(schema_file)

            if 'properties' in schema_data and 'MPItem' in schema_data['properties'] and 'items' in schema_data['properties']['MPItem'] and 'properties' in schema_data['properties']['MPItem']['items']:
                visible_properties = schema_data['properties']['MPItem']['items']['properties'].get('Visible', {}).get('properties', {})

                for prop_name, prop_data in visible_properties.items():
                    # Prepare a mini schema including all necessary properties
                    mini_schema = self.create_mini_schema(schema_data, prop_name)

                    # Write the mini schema to a JSON file
                    file_path = os.path.join(self.output_directory, f"{prop_name}.json")
                    with open(file_path, 'w') as output_file:
                        json.dump(mini_schema, output_file, indent=4)
            else:
                print("Error: 'properties' under 'MPItem' or its nested structure not found in the schema.")

    def create_mini_schema(self, schema_data, current_property):
        # Function to create a mini schema including parent properties, "Visible", and current_property data

        # Initialize mini schema with parent properties and title
        mini_schema = {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "additionalProperties": False,
            "type": "object",
            "title": schema_data.get('title', 'Mini Schema'),
            "properties": {}
        }

        # Include all parent properties except 'properties' and 'MPItem'
        for key, value in schema_data.items():
            if key != 'properties' and key != 'MPItem':
                mini_schema[key] = value

        # Include "Visible" and current_property data filtered for current_property
        if 'properties' in schema_data['properties']['MPItem']['items']:
            visible_data = schema_data['properties']['MPItem']['items']['properties'].get('Visible', {})
            filtered_visible = self.filter_visible_data(visible_data, current_property)
            mini_schema['properties']['Visible'] = filtered_visible

        return mini_schema

    def filter_visible_data(self, visible_data, current_property):
        # Function to filter "Visible" data to include only relevant parts for current_property

        filtered_visible = {}

        for key, value in visible_data.items():
            if key == 'properties':
                filtered_visible['properties'] = {current_property: value.get(current_property, {})}
            elif key == 'oneOf':
                filtered_visible['oneOf'] = [item for item in value if current_property in item.get('required', [])]
            elif isinstance(value, dict):
                filtered_visible[key] = self.filter_visible_data(value, current_property)

        return filtered_visible
