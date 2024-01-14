import os
import openai
import json
from openai import OpenAI

# extraction function
def extract_menu_info(context, menuData_format_JSON, set_api_key):
    client = OpenAI(
        api_key=set_api_key
    )
    max_len = 1600,
    size = "ada",
    debug = False,
    max_tokens = int(150),
    stop_sequence = None

    # request to openAI + response parameters
    request = "Extract menu items and descriptions from this restaurant menu."
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an assistant reading the restaurant menu information provided in HTML format, and extracting menu item names and descriptions into a JSON format."},
            {"role": "system", "content": "Use ONLY the information provided in the request. If you cannot understand the information in the request, say that you cannot handle the request."},
            {"role": "system", "content": "Return the answer in the following JSON format. Include the list of ingredients in the description. Put any allergy warnings or information in the allergy label field." + menuData_format_JSON.__str__()},
            {"role": "user", "content": "Context: " + context + "\nRequest: " + request}
        ],
        temperature=0,
        # max_tokens=max_tokens,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=stop_sequence,
    )

    # result of response from openAI
    raw_menu_extract = response.choices[0].message.content

    # handling loop, ensures that result is a complete JSON
    while True:
        if not raw_menu_extract:
            raise ValueError("Couldn't fix JSON")
        try:
            clean_menu_extract = json.loads(raw_menu_extract)
        except json.decoder.JSONDecodeError:
            try:
                clean_menu_extract = json.loads(raw_menu_extract + "]}")
            except json.decoder.JSONDecodeError:
                raw_menu_extract = raw_menu_extract[:-1]
                continue
        break

    # result of extraction function, will be used for analysis function
    return(clean_menu_extract)

# analysis function where menu contains allergy labels
def analyze_menu_allergylabels(allergylist, context, response_format_JSON, set_api_key):
    client = OpenAI(
        api_key=set_api_key
    )

    max_len = 1800,
    size = "ada",
    debug = False,
    max_tokens = int(150),
    stop_sequence = None

    # request to openAI + response parameters
    request = "Analyze this menu for risk of the following allergens: " + allergylist
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an assistant analyzing the restaurant menu specified in the context, for risk of the allergens stated in the user request."},
            {"role": "system", "content": "Only use the allergy_label field in the context to determine if the menu item contains the allergen; do not use the description field in the context."},
            {"role": "system", "content": "Return the answer in the following JSON format: " + response_format_JSON},
            {"role": "user", "content": "Context: " + context.__str__() + "\nRequest: " + request}
        ],
        temperature=0,
        # max_tokens=max_tokens,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=stop_sequence,
    )

    # result of analysis function, will be used for scoring
    return(response.choices[0].message.content)

# analysis function where menu does not contain allergy labels
def analyze_menu_descriptions(allergylist, context, response_format_JSON, set_api_key):
    client = OpenAI(
        api_key=set_api_key
    )
    max_len = 1800,
    size = "ada",
    debug = False,
    max_tokens = int(150),
    stop_sequence = None

    # request to openAI + response parameters
    request = "Analyze this menu for risk of the following allergens: " + allergylist
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an assistant analyzing the restaurant menu specified in the context, for risk of the allergens stated in the user request."},
            {"role": "system", "content": "Only consider the name and description fields in the context; do not consider the allergy_label field in the context."},
            {"role": "system", "content": "Return the answer in the following JSON format: " + response_format_JSON},
            {"role": "user", "content": "Context: " + context.__str__() + "\nRequest: " + request}
        ],
        temperature=0,
        # max_tokens=max_tokens,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=stop_sequence,
    )

    # result of analysis function, will be used for scoring
    return(response.choices[0].message.content)

# scoring function
def score_menu(menu_analysis_result):
    scoring_params = {
        "relative_weight_of_may_vs_very_likely": .7,
        "average_number_of_ingredients_in_a_highly_verbose_menu": 10
    }

    # determining risk score
    risk_score = (menu_analysis_result["number_of_menu_items_that_very_likely_contain_the_allergens"] + scoring_params["relative_weight_of_may_vs_very_likely"]*menu_analysis_result["number_of_menu_items_that_very_likely_contain_the_allergens"])/menu_analysis_result["total_number_of_menu_items"]

    #determining confidence score
    if menu_analysis_result["number_of_menu_items_with_allergy_labels_that_contain_a_value"] > 0:
        confidence_score = 1
    else:
        menu_verbosity = menu_analysis_result["average_number_of_ingredients_specified_per_menu_item"]/scoring_params["average_number_of_ingredients_in_a_highly_verbose_menu"]
        confidence_score = min(menu_verbosity,1)

    # result of scoring function, will be printed by main
    return {"risk_score": round(risk_score,2), "confidence_score": round(confidence_score,2)}
