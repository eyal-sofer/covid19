
import json
import urllib3
import collections

def lambda_handler(event, context):
    result = {}
    url = "https://covid-api.mmediagroup.fr/v1/cases?country=All"
    http = urllib3.PoolManager()
    response = http.request('GET',url)
    response = response.data
    response = json.loads(response)
    for key,value in response.items():
        country = key
        for key,value in value.items():
            if key != "All":
                break
                #country = key #skipping nested countries without sq_km_area property
            for key,value in value.items():
                if key == "recovered":
                    recovered = value
                elif key == "sq_km_area":
                    sq_km_area = value
                    result[country] = round(recovered / sq_km_area * 100)   

    my_keys = collections.OrderedDict(sorted(result.items()))
# Serializing json
    return {
        'statusCode': 200,
        'body': json.dumps(my_keys, indent = 4)
    }
