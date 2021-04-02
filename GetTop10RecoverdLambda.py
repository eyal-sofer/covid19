
import json
import urllib3

def lambda_handler(event, context):
    url = "https://covid-api.mmediagroup.fr/v1/history?country=All&status=recovered"
    http = urllib3.PoolManager()
    resp = http.request('GET',url)
    response = resp.data
    result = {}
    res = json.loads(response)
    for key,value in res.items():
        country = key
        for key,value in value.items():
            if key != "All":
                break
                #country = key #skipping nested countries without sq_km_area property
            for key,value in value.items():
                if key == "population":
                    population = value  
                if key == "dates":
                    dates = value  
                    #for key,value in dates.items():
                    rcvd_last_week = list(dates.values())[0] - list(dates.values())[6]
                    #print("country", country, "rcvd_last_ten_days", rcvd_last_ten_days)
                    if (country != "Global"):
                        result[country] = rcvd_last_week
    
    for key,value in result.items():
        print("key:", key,",", "value:", value)
    
    my_keys = sorted(result, key=result.get, reverse=True)[:10]

# Serializing json   
    return {
        'statusCode': 200,
        'body': json.dumps(my_keys, indent = 4)
    }
