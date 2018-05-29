# -*- coding: utf-8 -*-

import http.client, urllib.parse, json
import time

# **********************************************
# *** Update or verify the following values. ***
# **********************************************

# Replace the subscriptionKey string value with your valid subscription key.
subscriptionKey = "68a5eaf5c5714d0c82b05327106e76a5"

# Verify the endpoint URI.  At this writing, only one endpoint is used for Bing
# search APIs.  In the future, regional endpoints may be available.  If you
# encounter unexpected authorization errors, double-check this value against
# the endpoint for your Bing Web search instance in your Azure dashboard.
host = "api.cognitive.microsoft.com"
path = "/bing/v7.0/search"
terms = ['国际运动', '达赖喇嘛', '热门故事',
         '警察检查站', 'religious festival',
         'Party Congress', 'UNESCO World',
         '他的圣洁', 'World heritage', 'Press release']

def BingWebSearch(search):
    "Performs a Bing Web search and returns the results."

    headers = {'Ocp-Apim-Subscription-Key': subscriptionKey}
    conn = http.client.HTTPSConnection(host)
    query = urllib.parse.quote(search)
    conn.request("GET", path + "?q=" + query, headers=headers)
    response = conn.getresponse()
    headers = [k + ": " + v for (k, v) in response.getheaders()
                   if k.startswith("BingAPIs-") or k.startswith("X-MSEdge-")]
    return headers, response.read().decode("utf8")


if len(subscriptionKey) == 32:
    for term in terms:
        print('Searching the Web for: ', term)
        headers, result = BingWebSearch(term)
        print("\nRelevant HTTP Headers:\n")
        print("\n".join(headers))
        print("\nJSON Response:\n")
        webpages = json.loads(result)['webPages']
        for webpage in webpages['value']:
            print(webpage['url'])
        print()
        time.sleep(1)
else:
    print("Invalid Bing Search API subscription key!")
    print("Please paste yours into the source code.")    
