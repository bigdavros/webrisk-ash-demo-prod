import requests
import json
import myconfig
import google.auth
import google.auth.transport.requests
from google.oauth2 import service_account
import os
import pyfiglet
from termcolor import  cprint

basedir = os.path.abspath(os.path.dirname(__file__))

key = myconfig.WEBRISK_API_KEY
project_id=myconfig.PROJECT_ID


# --------------------------------------------------
def do_lookup(uri: str):
    """ Lookup API
        curl -X GET "https://webrisk.googleapis.com/v1/uris:search?threatTypes=MALWARE&uri=http%3A%2F%2Ftestsafebrowsing.appspot.com%2Fs%2Fmalware.html&key=API_KEY"
    """
    header = {"Content-Type": "application/json"}
    lookup_api = 'https://webrisk.googleapis.com/v1/uris:search?'
    threat_lookup = 'MALWARE'

    requeststring = lookup_api + "threatTypes=" + threat_lookup + "&uri=" + uri + "&key=" + key

    try:
        req = requests.get(requeststring, headers=header)
        return req.json()

    except Exception as e:
        print(" Google API returned error:", e)
        return None


# --------------------------------------------------
def do_update():
    """Update API
      curl -X GET "https://webrisk.googleapis.com/v1/threatLists:computeDiff?threatType=MALWARE&versionToken=Gg4IBBADIgYQgBAiAQEoAQ%3D%3D&constraints.maxDiffEntries=2048&constraints.maxDatabaseEntries=4096&constraints.supportedCompressions=RAW&key=API_KEY"
    """

    header = {"Content-Type": "application/json"}
    update_api = 'https://webrisk.googleapis.com/v1/'

    threatType = "MALWARE"
    versionToken = "ChAIARAGGAEiAzAwMSiAEDABEIPzCxoCGAvYCfmb"
    maxDiffEntries = "2048"
    maxDatabaseEntries = "4096"
    supportedCompressions = "RAW"
    threat = "threatLists:computeDiff?threatType=" + threatType + "&versionToken=" + versionToken + "&constraints.maxDiffEntries=" + maxDiffEntries + "&constraints.maxDatabaseEntries=" + maxDatabaseEntries + "&constraints.supportedCompressions=" + supportedCompressions

    requeststring = update_api + threat + "&key=" + key

    try:
        req = requests.get(requeststring, headers=header)
        return req.json()

    except Exception as e:
        print(" Google API returned error:", e)
        return None


# --------------------------------------------------
def do_extendedcoverage(uri: str):
    """Extended Coverage
       curl -X GET "https://webrisk.googleapis.com/v1/uris:search?threatTypes=SOCIAL_ENGINEERING_EXTENDED_COVERAGE&uri=http%3A%2F%2Ftestsafebrowsing.appspot.com%2Fs%2Fsocial_engineering_extended_coverage.html&key=API_KEY"
    """

    header = {"Content-Type": "application/json"}
    extended_coverage_api = 'https://webrisk.googleapis.com/v1/uris:search?threatTypes=SOCIAL_ENGINEERING_EXTENDED_COVERAGE'
    requeststring = extended_coverage_api + "&uri=" + uri + "&key=" + key

    try:
        req = requests.get(requeststring, headers=header)
        return req.json()

    except Exception as e:
        print("Google API returned error:", e)
        return None


# --------------------------------------------------
def do_evaluate(uri: str):
    """Evaluate API
       curl -X POST -H "Content-Type: application/json; charset=utf-8" -d @request.json "https://webrisk.googleapis.com/v1eap1:evaluateUri?key=API_KEY"
    """

    evaluate_api = "https://webrisk.googleapis.com/v1eap1:evaluateUri?key=" + key
    # header is empty
    headers = {}

    payload = {
        "uri": uri,
        "threatTypes": ["SOCIAL_ENGINEERING", "MALWARE", "UNWANTED_SOFTWARE"],
        "allowScan": "true"
    }

    try:
        req = requests.post(evaluate_api, data=json.dumps(payload), headers=headers)
        return req.json()

    except Exception as e:
        print("Google API returned error:", e)
        return None


# --------------------------------------------------
def do_submission(project_id: str, uri: str):
    """Submission API
    curl -X POST -H "Authorization: Bearer $(gcloud auth application-default print-access-token)" -H "Content-Type: application/json; charset=utf-8" -d @request.json "https://webrisk.googleapis.com/v1/projects/project-id/uris:submit"
    """

    submission_api = "https://webrisk.googleapis.com/v1/projects/" + project_id + "/uris:submit"
    

    # NOTE: use below code if you want to use gcloud auth and/or JSON file does not work 
    # token = subprocess.run(['gcloud', 'auth', 'print-access-token'], stdout=subprocess.PIPE)
    # token = subprocess.run(['gcloud', 'auth', 'application-default', 'print-access-token'], stdout=subprocess.PIPE)
    #
    # # print("Token type:", type(token.stdout))
    # token_str = token.stdout.decode("utf-8")
    # token_str = str(token_str).strip('\n')

    credentials = service_account.Credentials.from_service_account_file(
        os.path.join(basedir, 'service-account-webrisk.json'),
        scopes=[
            'https://www.googleapis.com/auth/cloud-platform'])
    auth_req = google.auth.transport.requests.Request()
    credentials.refresh(auth_req)
    print("auth_req :", auth_req)
    token_str = credentials.token

    bearer = "Bearer " + str(token_str)
    header = {"Content-Type": "application/json",
              "Authorization": bearer}

    payload = {
        "submission": {
            "uri": uri
        }
    }

    #TODO check status of submission
    # GET https://webrisk.googleapis.com/v1/projects/project-id/operations/operation-id&key=API_KEY
    #     https://webrisk.googleapis.com/v1/projects/wide-plating-348023/operations/1398048980146928771&key=AIzaSyA0NXXF2JSPHpbGR5LmIOXnrOM06WNX1rU
    
    header_check_status = {"Content-Type": "application/json"}

    try:
        req = requests.post(submission_api, data=json.dumps(payload), headers=header)

        #check status
        operation_id =  req.json()["name"].split('/')[3]
        # operation_id = operation_id_str
        print("operation_id : " + operation_id)
        # submission_api_status = "https://webrisk.googleapis.com/v1/projects/" + project_id + "/operations/" + operation_id+ "&key="  + key
        # print ("submission_api_status:" + submission_api_status)
        # req2 = requests.get(submission_api_status, headers=header)
        # print(req2.json())

        return req.json()

    except Exception as e:
        print("Google API returned error:", e)
        return None

# --------------------------------------------------
  
def main():

    #print the banner Web Risk in yellow
    cprint(pyfiglet.figlet_format('=== Web Risk  === ',  width = 100, justify="center"), "yellow")
    input1 = input()

    #TODO use if needed
    # url = url.replace(":", "%3A").replace("/", "%2F")

    #Sample URLS

    # http://testsafebrowsing.appspot.com/apiv4/ANY_PLATFORM/MALWARE/URL/
    # http://testsafebrowsing.appspot.com/apiv4/ANY_PLATFORM/SOCIAL_ENGINEERING/URL/
    # http://testsafebrowsing.appspot.com/apiv4/ANY_PLATFORM/UNWANTED_SOFTWARE/URL/
    # http://testsafebrowsing.appspot.com/apiv4/IOS/SOCIAL_ENGINEERING/URL/	    
    # 
    # http://testsafebrowsing.appspot.com/s/malware.html	
    # http://testsafebrowsing.appspot.com/s/phishing.html
    # https://testsafebrowsing.appspot.com/s/unknown.exe
    # http://testsafebrowsing.appspot.com/s/content.exe

    lookup_uri  ="http://testsafebrowsing.appspot.com/s/malware.html"
    extendedcoverage_uri = "http://testsafebrowsing.appspot.com/s/social_engineering_extended_coverage.html"
    evaluate_uri = "https://www.google.com"
    submission_uri = "https://www.phishingsite.com/"

    
    print(pyfiglet.figlet_format("Lookup API", width = 100 ))
    print("URL : " + lookup_uri)
    print(do_lookup(lookup_uri))    
    
    input1 = input()
    
    
    print(pyfiglet.figlet_format("Update API", width = 100 ))
    print(do_update())
    print("                 ")
    input1 = input()

    print(pyfiglet.figlet_format("Extended Coverage", width = 100 ))
    print("URL : " + extendedcoverage_uri)
    print(do_extendedcoverage(extendedcoverage_uri))
    print("                 ")
    input1 = input()

    print(pyfiglet.figlet_format("Evaluate API", width = 100 ))
    print("URL : " + evaluate_uri)
    print(do_evaluate(evaluate_uri)) 
    print(do_evaluate("http://testsafebrowsing.appspot.com/s/malware.html")) 
    print("                 ")
    input1 = input()

    # print(pyfiglet.figlet_format("Submission API", width = 100 ))
    # print("URL : " + submission_uri)
    # print(do_submission(project_id, submission_uri))

if __name__ == "__main__":
    main()  
