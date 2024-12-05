
from jsonschema  import validate
from jsonschema.exceptions import  ValidationError
import pandas as pd
import re
import json

di={}

# you can use the type keyword to constrain an instance to an object, array, string, number, boolean, or null

def validate_field_with_jsonschema(value, col_name,schema):  #di=None,value=None,col_name=None):           # Function to validate a single field
    try:
        if pd.isnull(value) or str(value).strip().lower() in ["", "na", "null"]:
            return f"{col_name} contains a null or empty value."


        json_obj = {col_name: value}         # Create a temporary JSON object with just the single field



        validate(instance=json_obj, schema=schema)   #field_schema)
        return None                              # No errors
    except ValidationError as e:
        return str(e)  # Return the validation error message


def schemas(column_name):
    print("SCHEMA :")
    print("type ,formate, maxlenght, minlenght, pattern, enum, minimum, maximum ")
    print(f"enter schema for {col_name}")

    attributes=['type','formate','maxlenght','minlenght','pattern','enum','minimum', 'maximum','description' ]
    #exclusiveMaximum, exclusiveMinimum, formate:(date-time,date,time,duration,email,idn-email,hostname,idn-hostname,ipv4,ipv6,)


    schema_details={}

    for attr in attributes:
        value = input(f"{attr}: ")
        if value:  # Only add non-empty attributes to the schema   "^(https?|http?|ftp)://[^\s/$.?#].[^\s]*$"
            if attr == 'enum':  # Special handling for enum
                try:
                    # Convert the input string into a Python list
                    value = json.loads(value)
                    if not isinstance(value, list):  # Ensure it's a list
                        raise ValueError("Enum must be a list.")
                except json.JSONDecodeError:
                    print("Invalid format for enum. Please enter a valid JSON array (e.g., [\"USD\", \"EUR\"]).")
                    continue
            elif attr in ['minimum', 'maximum', 'minLength', 'maxLength']:
                value = int(value)  # Convert numerical attributes to integers

            schema_details[attr] = value


    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "properties": {
            column_name: schema_details
        },
        "required": [column_name]      # Ensure this field is validated
    }
    di[column_name] = schema           # Save schema in the global dictionary
    return schema

    print(di)




#-------------------------------------------start--------------------------------------------------
# Load Excel file
input_file = "C:/Users/Admin/PycharmProjects/validation_rules/swiggy_instamart_20241129.xlsx"              #C:/Users/Admin/PycharmProjects/validation_rules/single_col.xlsx"             #C:/Users/Admin/PycharmProjects/validation_rules/3_col.xlsx"   #C:/Users/Admin/PycharmProjects/validation_rules/metro_canada_full_2024_11_15.xlsx" #C:/Users/Admin/PycharmProjects/validation_rules/single_col.xlsx"
output_file = "C:/Users/Admin/PycharmProjects/validation_rules/invalid_data_swiggy_1.xlsx"
df = pd.read_excel(input_file)
columns_name = df.columns
error_records = []

for col_name in columns_name:
    if  col_name.lower() in ["id", "index"]:
        continue

    schema =  schemas(col_name)
    print("schema :",schema)

    for idx, value in enumerate(df[col_name]):
        error = validate_field_with_jsonschema(value, col_name, schema)

        if error : #or error =="nan" or error == "NA" or error == None
            # Append index, column name, invalid value, and error message to error records
            error_records.append({
                "Row Index": idx+1,
                "Column Name": col_name,
                "Invalid Value": value,
                "Error": error
            })


print("E_R:",error_records)
if error_records:
    error_df = pd.DataFrame(error_records)
    error_df.to_excel(output_file, index=False)
    print(f"Invalid data saved to {output_file}")
else:
    print("No validation errors found!")



