# Walmart V5 Products Schema Parser

This Python script processes Walmart's V5 product schema (`MP_ITEM-5.0.20230926-17_34_53-apimp_fullschema.json`) and generates simplified or split JSON outputs for easier inspection and automation.

## Features

- Parses and loads the Walmart product schema
- Splits the `Visible` section into individual JSON schema files per field
- Optionally generates structured JSON templates based on the full schema

## Project Structure

```
.
├── main.py               # Entry point: choose split or generate mode
├── schema_handler.py     # Handles schema splitting logic
├── json_handler.py       # Handles schema loading and JSON generation
└── MP_ITEM-5.0.20230926-17_34_53-apimp_fullschema.json  # Walmart schema (not included)
```

## Input

- `MP_ITEM-5.0.20230926-17_34_53-apimp_fullschema.json`
  - This is the official Walmart full schema (V5, dated 2023-09-26).
  - Place this file in the following path:

  ```
  ~/Downloads/Walmart JSON/MP_ITEM-5.0.20230926-17_34_53-apimp_fullschema.json
  ```

## Output

- The script outputs JSON files under:

  ```
  ~/Downloads/Walmart JSON/
  ```

- In **split mode**, it creates one file per field under `Visible` (e.g., `brand.json`, `color.json`).
- In **generate mode**, it outputs JSON data structures following the schema format.

## Usage

1. Open `main.py`
2. Set the desired mode by changing this line:

```python
generateJson = False  # Set to True to run generation mode instead of split mode
```

3. Run the script:

```bash
python main.py
```

## Modes

### Split Mode (`generateJson = False`)
- Extracts all fields inside the `Visible` section of the Walmart schema
- Writes each field as a mini standalone schema file

### Generate Mode (`generateJson = True`)
- Produces example JSON data based on the schema
- Includes headers, `Visible`, and `Orderable` sections
- Does not populate example values if `omit_values` is `True`

## Notes

- All output is written to your `Downloads/Walmart JSON` folder
- This project is standalone; no dependencies or `requirements.txt` are needed
- Only Python 3.6+ is required (standard library only)

## License

This project is provided as-is under the MIT License. See `LICENSE` if included.
