import logging

import azure.functions as func
import requests
import json

BASE_URL = "https://api.open.fec.gov/v1/committee/"
#?api_key=DtAehhI9j9WL6FRthQKdM5tvPBBo6M5SHlTlL0fT&cycle=2020&is_amended=false&type=P"
VALID_CANDIDATES = ["Joe Biden", "Elizabeth Warren", "Bernie Sanders", "Pete Buttigieg", 
    "Michael Bloomberg", "Amy Klobuchar", "Tom Steyr", "Donald Trump"
]

def get_fec_committee_data(committee_id, api_key):
    # Note that some parameters are hardcoded into this URL - this can be improved in the future with some additional paramaterization
    request_url = BASE_URL + f"{committee_id}?api_key={api_key}&cycle=2020&is_amended=false&type=P"
    r = requests.get(request_url)
    r.raise_for_status()
    logging.info("Recieved response: " + str(r.json()))
    return r.json()

def main(req: func.HttpRequest, inputblob: func.InputStream, outputblob: func.Out[str]) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    candidate_name = req.params.get('candidateName')
    api_key = req.params.get('apiKey')

    # Validate candidate name is passed
    if candidate_name in VALID_CANDIDATES:
        pass
    else:
        return func.HttpResponse(
             "Please pass a valid candidateName on the query string",
             status_code=400
        )

    # Validate api key is provided
    if api_key:
        pass
    else:
        return func.HttpResponse(
             "Please pass an apiKey on the query string",
             status_code=400
        )

    # Load the etl control data blob which contains some metadata for our candidates
    candidates = json.loads(inputblob.read())[0]["candidates"]
    candidate = [cand for cand in candidates if cand['name'] == candidate_name][0]

    committees = candidate["committee_ids"]

    # Loop through committees in case there are multiple
    responses = []
    for committee in committees:
        r = get_fec_committee_data(committee, api_key)
        responses.append(r)

    output_string = json.dumps(responses)

    # Output BLOB data
    outputblobname = candidate_name
    outputblob.set(output_string)

    # Send a 200 status code with the copied blob data to the API user
    return func.HttpResponse(
             "Copied JSON data to BLOB: %s" % output_string,
             status_code=200
        )

