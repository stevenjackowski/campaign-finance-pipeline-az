import logging
import os
import json

import azure.functions as func
from azure.storage.blob import BlobServiceClient

def transform_candidate(candidate_blob, candidate_name):
    """
    Function transforms a candidate blob into the desired output format by aggregating values across committees.
    Values to be collected include total_contributions, operating_expenditures, and cash_on_hand_end_period,
    total_recipes, and candidate_contribution_period.
    """
    xfrmed_dict = {}
    # Iterate through results and aggregate values if there are multiple committees
    for result in candidate_blob["results"]:
        end_date = result["coverage_end_date"]
        if end_date in xfrmed_dict.keys():
            nested_dict = xfrmed_dict[end_date]
            nested_dict["total_contributions_period"] = nested_dict["total_contributions_period"] + result["total_contributions_period"]
            nested_dict["operating_expenditures_period"] = nested_dict["operating_expenditures_period"] + result["operating_expenditures_period"]
            nested_dict["cash_on_hand_end_period"] = nested_dict["cash_on_hand_end_period"] + result["cash_on_hand_end_period"]
            nested_dict["candidate_contribution_period"] = nested_dict["candidate_contribution_period"] + result["candidate_contribution_period"]
            nested_dict["total_receipts_period"] = nested_dict["total_receipts_period"] + result["total_receipts_period"]
        else:
            nested_dict = {}
            nested_dict["total_contributions_period"] = result["total_contributions_period"]
            nested_dict["operating_expenditures_period"] = result["operating_expenditures_period"]
            nested_dict["cash_on_hand_end_period"] = result["cash_on_hand_end_period"]
            nested_dict["candidate_contribution_period"] = result["total_contributions_period"]
            nested_dict["total_receipts_period"] = result["total_receipts_period"]

            xfrmed_dict[end_date] = nested_dict
    
    # Use function to flatten the dictionary to a list of dicts instead of a dict of date keys
    def flatten_fun(kv_pair):
        return {
            "candidate": candidate_name,
            "period_end_date": kv_pair[0],
            "total_contributions_period": kv_pair[1]["total_contributions_period"],
            "operating_expenditures_period": kv_pair[1]["operating_expenditures_period"],
            "cash_on_hand_end_period": kv_pair[1]["cash_on_hand_end_period"],
            "candidate_contribution_period": kv_pair[1]["candidate_contribution_period"],
            "total_receipts_period": kv_pair[1]["total_receipts_period"]
        }
    out = map(flatten_fun, iter(xfrmed_dict.items()))
    logging.info(xfrmed_dict)
    logging.info(out)
    return list(out)

def main(req: func.HttpRequest, inputblob: func.InputStream, outputblob: func.Out[str]) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # Establish storage account connection
    # Note - in this function, bindings are not used as we want to iterate through all of the blobs in a container
    # Bindings only allow us to connect to a specific blob file/location
    storage_account_string = os.environ["AzureWebJobsStorage"]
    blob_service_client = BlobServiceClient.from_connection_string(storage_account_string)
    container_client = blob_service_client.get_container_client("raw-data")
    candidate_blobs = container_client.list_blobs()

    xfrmed_results = []
    for candidate_blob in candidate_blobs: 
        blob_client = container_client.get_blob_client(candidate_blob.name)
        blob_data = json.loads(blob_client.download_blob().readall())[0]
        xfrmed = transform_candidate(blob_data, candidate_blob.name.split('.json')[0])
        logging.info(xfrmed)
        xfrmed_results.extend(xfrmed)

    # Output transformed JSON to final blob
    outputblob.set(json.dumps(xfrmed_results))

    return func.HttpResponse(
            json.dumps(xfrmed_results),
            status_code=200
    )