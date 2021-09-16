from urllib import request, parse
import urllib.request
import json
import re

def paper_titles_for_id(person_id):

    data = parse.urlencode({"client_id":"APP-09R2KRI2V6E7LM72",
        "client_secret": "f25ed599-6ea5-4571-9e60-6d24d40a79a2",
        "grant_type":"client_credentials",
        "scope":"/read-public"}).encode()
    req =  request.Request("https://orcid.org/oauth/token", data=data) # this will make the method "POST"
    resp = request.urlopen(req)

    access_token = json.load(resp)['access_token']

    data = {"Accept":"application/vnd.orcid+json",
        "Authorization type and Access token": f"Bearer {access_token}"}
    req = urllib.request.Request(f"https://pub.orcid.org/v3.0/{person_id}/record", headers=data)

    output = json.load(urllib.request.urlopen(req))
    
    titles = [re.sub(' +', ' ', x['work-summary'][0]['title']['title']['value'].replace("\n", "")) for x in output["activities-summary"]["works"]["group"]]
    return titles

# paper_titles_for_id("0000-0001-5458-8645")
