import re
import json
import math
import pandas as pd
di={}
validation_rules = {
    "product_url": {
        "type": "string",
        "required": True,
        "starts_with": ["http://", "https://"],
        "max_length": 255,
    },
    "category": {
        "type": "string",
        "required": True,
        "max_length": 100,
       # "allowed_values": [
       #      "Electronics", "Clothing", "Home Appliances", "Books", "Toys","Furniture", "Groceries", "Beauty Products",
       #      "Home", "Aisles", "Baby", "Food", "Formula", "Cereal","Bread", "Bakery Products" ,"Packaged Bread", "Rye",
       #      "Other Grains","Frozen","Meals","Sides","Beef" ,"Veal Meals","Beer", "Microbrewery","Artisanal"
       #  ],
    },
    "product_name": {
        "type": "string",
        "required": True,
        "max_length": 90,
        "min_length": 3,
        # "regex": "^[a-zA-Z0-9 ]+$"
    },
    "product_number": {
        "type": "number",
        "required": True,
        "unique": True,
        "min_length":3
    },
    "mrp": {
        "type": "number",
        "required": True,
        "min": 0,
        "max": 100000,
    },
    "price": {
        "type": "number",
        "required": True,
        "min": 0,
        "max": 100000,
    },
    "currency": {
        "type": "string",
        "required": True,
        "allowed_values": ["$","USD", "EUR", "INR", "GBP"],
        "min_length":1
    },
    "serving_for_people": {
        "type": "number",
        "required": False,
        "min": 1,
        "max": 100,
    },
    "quantity": {
        "type": "alphanumeric",
        "required": True,
        # "pattern": r"^\d+(\.\d+)?\s?[a-zA-Z]+$",
    },
    "price_per_unit": {
        "type": "alphanumeric",
        "required": True,
        "min": 0,
        "max": 1000,
    },
    "product_image": {
        "type": "string",
        "required": True,
        "starts_with": ["http://", "https://"],
        "ends_with": [".jpg", ".png"],
        "max_length": 500,
    },
    "product_description": {
        "type": "string",
        "required": True,
        "max_length": 700,
        "min_length": 10,
    },
    "ingredients": {
        "type": "string",
        "required": True,
        "max_length": 200,
    },
    "valid_date": {
        "type": "string",
        "required": True,
        "format": "yyyy-mm-dd",
    }
}

def validate_value(value, rules):

    if rules.get("required") and value is None or str(value).strip() == "" or value == "NA" or value == " " or pd.isna(value) or str(value).strip().lower() == "na" :
        # a="null value"
        return False

    # Type check
    expected_type = rules.get("type")
    if expected_type:
        if expected_type == "number" and not isinstance(value, (int, float)):
            return False
        if expected_type == "string" and not isinstance(value, str):
            return False
        if expected_type == "alphanumeric" and not (isinstance(value, str) and value.replace(" ", "").isalnum()):
            return False

    # String-specific checks
    if isinstance(value, str):
        if rules.get("trim_whitespace"):
            value = value.strip()
        if rules.get("max_length") and len(value) > rules["max_length"]:
            return False
        if rules.get("min_length") and len(value) < rules["min_length"]:
            return False
        if rules.get("regex") and not re.match(rules["regex"], value):
            return False
        if rules.get("starts_with") and not any(value.startswith(prefix) for prefix in rules["starts_with"]):
            return False
        if rules.get("ends_with") and not any(value.endswith(suffix) for suffix in rules["ends_with"]):
            return False
        if rules.get("no_special_chars") and any(char in value for char in rules["no_special_chars"]):
            return False


    # Number-specific checks
    if isinstance(value, (int, float)):
        if rules.get("min") is not None and value < rules["min"]:
            return False
        if rules.get("max") is not None and value > rules["max"]:
            return False
        if rules.get("step") and (value * 100) % (rules["step"] * 100) != 0:
            return False

    # Generic checks for allowed/disallowed values
    if rules.get("allowed_values") and value not in rules["allowed_values"]: #any(char in value for char in rules["allowed_values"]
        return False

    if rules.get("disallowed_words") and any(word in str(value) for word in rules["disallowed_words"]):
        return False

    return True

def validate_excel(input_file, validation_rules, output_path):
    df = pd.read_excel(input_file)
    # print("abc:",validation_rules)

    for column in df.columns:
        print("cols",column)
        if column in validation_rules:
            rules = validation_rules[column]
            invalid_data = []

            for index, value in df[column].items():                 # iterate every column values
                # print("index",index,":",value)
                if not validate_value(value, rules):
                    invalid_data.append({ "Column": column, "Row": index + 1,  # +1 to match Excel row indexing
                                          "Invalid Value": value,})
            di[column]=invalid_data

    print("di",di)

    flattened_data = []
    for column, entries in di.items():
        for entry in entries:
            for k, v in entry.items():
                if isinstance(v, float) and math.isnan(v):            # Check for NaN
                    entry[k] = "NA"

            flattened_data.append({ "id": entry["Row"],               # Row number becomes id
                                    column: entry["Invalid Value"]})  # Invalid value goes under the corresponding column

    df = pd.DataFrame(flattened_data)

    df = df.groupby("id").first().reset_index()                       # Group by 'id' to consolidate values from different columns

    output_file = "formatted_invalid_data_7.xlsx"                     # Save to Excel in the desired format

    df.to_excel(output_file, index=False)

    print(f"Invalid data has been saved in the desired format to {output_file}")


# Example usage:
input_file = "C:/Users/Admin/PycharmProjects/validation_rules/single_col.xlsx" #C:/Users/Admin/PycharmProjects/validation_rules/gov_il_03_10_2024_native.xlsx" #C:/Users/Admin/PycharmProjects/validation_rules/single_col.xlsx"  # Input Excel file
output_path = "invalid_data_1b.xlsx"  # Output file with invalid data sheets

validate_excel(input_file, validation_rules, output_path)













# def validate_value(value, rules):
#     if "null_check" in rules and rules["null_check"]:
#         if value is None or str(value).strip() == "":
#             return False
#
#         # Other validations (type check, range checks, etc.) go here
#     if "required" in rules and rules["required"] and (value is None or str(value).strip() == ""):
#         return False
#
#         # Type check
#     if "type" in rules:
#         if rules["type"] == "number" and not isinstance(value, (int, float)):
#             return False
#         if rules["type"] == "string" and not isinstance(value, str):
#             return False
#
#         # Continue with other validation rules...
#
#     return True
#
#
# def validate_excel(file_path, validation_rules,output_path):
#     df = pd.read_excel(file_path)
#
#     with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
#         # Iterate through each column and validate
#         for column in df.columns:
#             if column in validation_rules:
#                 rules = validation_rules[column]
#                 invalid_data = []
#
#                 # Validate column values
#                 for index, value in df[column].items():
#                     if not validate_value(value, rules):
#                         # Add the invalid data and its index
#                         invalid_data.append({"Index": index + 1, "Value": value})
#
#                 # If there are invalid values, write them to the respective sheet
#                 if invalid_data:
#                     invalid_df = pd.DataFrame(invalid_data)
#                     invalid_df.to_excel(writer, sheet_name=column, index=False, header=True)
#
#     print(f"Validation complete. Invalid data has been written to {output_path}")
#
#
#
# # Example usage:
# file_path = "C:/Users/Admin/PycharmProjects/validation_rules/val_test.xlsx"  # Input Excel file
# output_path = "validated_output_33.xlsx"  # Output file with invalid data sheets
#
# # Validate the file and create an output with invalid values in separate sheets
# validate_excel(file_path, validation_rules, output_path)


# if invalid_data:
#     invalid_df = pd.DataFrame(invalid_data)
#     invalid_df.to_excel(writer, sheet_name=column, index=False, header=True)

# if not invalid_data:
#     summary_df = pd.DataFrame({"Message": ["No errors found in the file"]})
#     summary_df.to_excel(writer, sheet_name=column, index=False)


# print(f"Validation complete. Invalid data has been written to {output_path}")


# with pd.ExcelWriter(output_path, engine='openpyxl') as writer:   #making sheets from  here
