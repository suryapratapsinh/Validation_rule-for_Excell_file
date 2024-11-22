import pandas as pd
import numpy as np
import re

df = pd.read_excel("C:/Users/Admin/PycharmProjects/validation_rules/validation_testing.xlsx",index_col=0)

# l=[df.columns.values]
# print(l)
# headers_list =df.columns.values.tolist()
# print(headers_list)


def product_price(df):
    # print(df['price'])   # get product urls data

    invalid_price = []

    for index, value in df['price'].items():
        if ( pd.isna(value)    or     value == "NA"   or   (isinstance(value, str) and not value.strip().isdigit())  or not isinstance(value,(int,float))):   # Check for NaN or empty cell --- Check for 'NA' strings --- Check for strings
            print("for price :",index,":",value)
            invalid_price.append({"Row ID": index + 1, "Invalid Value": value})



    result_df = pd.DataFrame(invalid_price)
    df2 = result_df.replace(np.nan, "NaN")
    return df2
def product_mrp(df):
    # print(df['price'])   # get product urls data

    invalid_mrp = []

    for index, value in df['mrp'].items():
        if ( pd.isna(value)    or     value == "NA"   or   (isinstance(value, str) and not value.strip().isdigit())  or not isinstance(value,(int,float))):  # Check for empty spaces
            print("for mrp :",index,":",value)
            invalid_mrp.append({"Row ID": index + 1, "Invalid Value": value})

    result_df = pd.DataFrame(invalid_mrp)
    df2 = result_df.replace(np.nan, "NaN")
    return df2
def product_currency(df):
    # print(df['price'])   # get product urls data

    invalid_currency = []

    for index, value in df['currency'].items():
        if ( pd.isna(value)    or    value == "NA"  or  isinstance(value, str) and value != "$" ):  # Check for empty spaces   or   (isinstance(value, str) and not value.strip().isdigit())
            print("for currency :",index,":",value)
            invalid_currency.append({"Row ID": index + 1, "Invalid Value": value})

    result_df = pd.DataFrame(invalid_currency)
    df2 = result_df.replace(np.nan, "NaN")
    return df2
def product_number(df):
    invalid_product_number = []

    for index, value in df['product_number'].items():
        if (pd.isna(value) or   value == "NA" or  value == ""  or isinstance(value,(str,float))):  # Check for empty spaces  and not value.strip().isdigit()
            print("for product_number :",index,":",value)
            invalid_product_number.append({"Row ID": index + 1, "Invalid Value": value})

    result_df = pd.DataFrame(invalid_product_number)
    df2 = result_df.replace(np.nan, "NaN")
    return df2
def product_url(df):

    invalid_urls = []
    url_pattern = re.compile(
        r'^(https?://)'  # Start with http:// or https://
        r'([a-zA-Z0-9.-]+)'  # Domain name
        r'(\.[a-zA-Z]{2,})'  # Dot followed by domain extension  ^(https?:\\/\\/)?(www\\.)?[a-zA-Z0-9-]+\\.[a-zA-Z]{2,}$
    )

    # average_length = sum(len(s) for s in df['product_url']) / len(df['product_url'])
    # print("avg len :",average_length)

    for index, value in df['product_url'].items():

        if (pd.isna(value) or  value == "NA" or value == " " or not isinstance(value, str)  or  not url_pattern.match(value.strip())  or  len(value) >= 255  ):#or  len(value) == average_length
            print("for url :",index,":",value)
            invalid_urls.append({"Row ID": index + 1, "Invalid Value": repr(value) if pd.notna(value) else "NaN"})

    # Convert list of invalid entries into a DataFrame
    result_df = pd.DataFrame(invalid_urls)
    df2 = result_df.replace(np.nan, "NaN")
    return df2

def product_name(df):
    # print(df['price'])   # get product urls data
    invalid_product_names = []

    for index, value in df['product_name'].items():
        if (pd.isna(value)   or   value == "NA"  or value == "  "  or  value == "   "  or   len(value.strip()) < 3  or len(value) > 100  or  value.count(" ") > 15 ):   # Check for NaN or empty cell --- Check for 'NA' strings --- Check for strings
            print("for price :",index,":",value)
            invalid_product_names.append({"Row ID": index + 1, "Invalid Value": value})

    result_df = pd.DataFrame(invalid_product_names)
    df2 = result_df.replace(np.nan, "NaN")
    return df2

def price_per_unit(df):
    # print(df['price'])   # get product urls data
    price_p_u = []

    # pattern =  re.compile(r"\$\s+?\d{1,3}(?:,\d{3})*(?:\.\d{1,3})?\s?\/\s?\d+(\s?(ml|gm|kg|g|un))\s\.\s?")                 #\$\s?\d{1,3}(?:,\d{3})*(?:\.\d{1,3})?\s?\/\s?\d+(\s?ml|\s?gm|\s?un|\s?g|\s?kg)\.")  #'^$[0-9].[0-9]/[0-9][A-Z][a-z]?'

    for index, value in df['price_per_unit'].items():
        if (pd.isna(value)   or   value == "NA"  or value == "  " or value == "   "   or  "$" not in value  or  'ml' not in value  or 'gm' not in value  or 'kg' not in value   or 'g' not in  value   or 'un' not in value  or value.count(" ") >5 ):       # not pattern.match(value.strip()) Check for NaN or empty cell --- Check for 'NA' strings --- Check for strings
            print("for price per unit :",index,":",value)
            price_p_u.append({"Row ID": index + 1, "Invalid Value": value})

    result_df = pd.DataFrame(price_p_u)
    df2 = result_df.replace(np.nan, "NaN")
    return df2

def product_image(df):

    invalid_image_url = []
    url_pattern = re.compile(r"https:\/\/product-images\.metro\.ca\/images\/[a-z0-9]+\/[a-z0-9]+\/\d+\.(jpg|png|jpeg|gif)")

    # average_length = sum(len(s) for s in df['product_url']) / len(df['product_url'])
    # print("avg len :",average_length)

    for index, value in df['product_image'].items():

        if (pd.isna(value) or  value == "NA" or value == " " or not isinstance(value, str)  or  not url_pattern.match(value.strip())  or  len(value) >= 255  ):   #or  len(value) == average_length
            print("for product image :",index,":",value)
            invalid_image_url.append({"Row ID": index + 1, "Invalid Value": repr(value) if pd.notna(value) else "NaN"})

    # Convert list of invalid entries into a DataFrame
    result_df = pd.DataFrame(invalid_image_url)
    df2 = result_df.replace(np.nan, "NaN")
    return df2






if __name__=="__main__":

    price_issues = product_price(df)
    mrp_issues = product_mrp(df)
    currency_issue = product_currency(df)
    product_number_issue = product_number(df)
    url_issue = product_url(df)
    product_name_issue = product_name(df)
    ppu_issue = price_per_unit(df)
    image_issue=product_image(df)

# Write results to separate sheets in one Excel file

    output_file = "validation_results_11.xlsx"

    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        price_issues.to_excel(writer, sheet_name="Price Issues", index=False)
        mrp_issues.to_excel(writer, sheet_name="MRP Issues", index=False)
        currency_issue.to_excel(writer, sheet_name="CURRENCY Issues", index=False)
        product_number_issue.to_excel(writer, sheet_name="PRODUCT_NUMBER Issues", index=False)
        url_issue.to_excel(writer, sheet_name="URL Issues", index=False)
        product_name_issue.to_excel(writer, sheet_name="NAME Issues", index=False)
        ppu_issue.to_excel(writer, sheet_name="price_per_unit Issues", index=False)
        image_issue.to_excel(writer, sheet_name="price_per_unit Issues", index=False)



    print(f"Validation results saved to '{output_file}'")








# pd.isna(value)    or                                                 # Check for NaN or empty cells
#                 value == "NA"   or                                              # Check for 'NA' strings
#                 (isinstance(value, str) and not value.strip().isdigit()) or   # Check for strings
#                 value == "$"



#function calling code
# fl=[product_price,product_mrp,product_currency]
    # for i in fl:
    #     print("for",i,"function")
        # print(i(df))





# $2.64 /100g
# $3.00 /100g
# $13.62 /100g
# $0.33 /un.
# $0.08 /un.
# $1.87 /100ml
# $2.33 /100g
# $0.81 /un.
# $1.37 /un.