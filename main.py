import os
from pathlib import Path
from json_handler import SchemaHandler, FileWriter
from schema_handler import SchemaFileSplitter

def generateJsonFromSchema(schema_path, downloads_path):
    schema_handler = SchemaHandler(schema_path)
    schema = schema_handler.load_schema()

    file_writer = FileWriter(downloads_path)
    file_writer.generate_and_write_json_with_jsonschema(schema, True)
    
def splitSchema(schema_path, downloads_path):
    splitter = SchemaFileSplitter(schema_path, downloads_path)
    splitter.split_schema_file()

def main():
    downloads_path = str(Path.home() / "Downloads/Walmart JSON")
    schema_file_name = 'MP_ITEM-5.0.20230926-17_34_53-apimp_fullschema.json'
    schema_path = os.path.join(downloads_path, schema_file_name)
    
    # Split schema or generate json
    generateJson = False

    if (generateJson):
        generateJsonFromSchema(schema_path, downloads_path)
    else:
        splitSchema(schema_path, downloads_path)
    
    

if __name__ == "__main__":
    main()
