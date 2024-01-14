import os
import json

from foodAllergyRiskEvalFunctions import extract_menu_info
from foodAllergyRiskEvalFunctions import analyze_menu_allergylabels
from foodAllergyRiskEvalFunctions import analyze_menu_descriptions
from foodAllergyRiskEvalFunctions import score_menu

print("Initializing program...")
# set your base directory here
basedir = " "
# insert your own api key here
set_api_key = " "

# insert the allergen(s) you want to search for here.
allergylist = 'Shellfish, nuts'
# insert the menu you want to analyze here
menu_name = "test_menu_indian.txt"

# file object for extraction JSON format
menuData_format_JSON = basedir + "src" + "\\" + "menuData_format.JSON"
f = open(menuData_format_JSON, "r", encoding="UTF-8")
menuData_format_JSON = f.read()

# file object for raw menu data
context = basedir + "data" + "\\" + "input" + "\\" + menu_name
f = open(context, "r", encoding="UTF-8")
context = f.read()

# calling extraction function, assigning result to clean_menu_extract
print("Extracting menu: " + menu_name + "...")
menuData_JSON = extract_menu_info(context, menuData_format_JSON, set_api_key)

# file object for analysis JSON format
response_format_JSON = "menu_analysis_response_format.JSON"
f = open(response_format_JSON, "r", encoding="UTF-8")
response_format_JSON = f.read()

# calling analysis function and assigning result to analysis_result
context = menuData_JSON
print("Analyzing menu: " + menu_name + " for the following allergens => " + allergylist + "...")
menu_analysis_result = json.loads(analyze_menu_allergylabels(allergylist, context, response_format_JSON, set_api_key))
if menu_analysis_result["number_of_menu_items_with_allergy_labels_that_contain_a_value"] == 0:
    menu_analysis_result = json.loads(analyze_menu_descriptions(allergylist, context, response_format_JSON, set_api_key))
else:
    menu_analysis_result["number_of_menu_items_that_very_likely_contain_the_allergens"] = menu_analysis_result["number_of_menu_items_with_allergy_labels_that_say_the_item_contains_the_allergens"]
    menu_analysis_result["number_of_menu_items_with_allergy_labels_that_say_the_item_may_contain_the_allergens"] = menu_analysis_result["number_of_menu_items_with_allergy_labels_that_say_the_item_may_contain_the_allergens"]

# calling scoring function and assigning result to scores + printing results
print("Score for menu: " + menu_name + " => " + (score_menu(menu_analysis_result)).__str__())


