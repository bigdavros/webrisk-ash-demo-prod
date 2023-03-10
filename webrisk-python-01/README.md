
# Web Risk Demo in Python


## Description
This is Python based project to demostrate how to use different APIs of Web Risk

What is Web Risk
Web Risk is a Google Cloud service that lets client applications check URLs against Google's constantly updated lists of unsafe web resources. 

The Lookup API lets your client applications check if a URL is included on any of the Web Risk lists.

The Update API lets your client applications download hashed versions of the Web Risk lists for storage in a local or in-memory database. URLs can then be checked locally. 

The Web Risk's Extended Coverage API helps to improve the coverage of malicious urls with a small amount (less than 10%) of potential false positives.

The Evaluate API to let your client applications evaluate the maliciousness of a URL. 

The Submission URLs lets your submit the URL that you suspect are unsafe to Safe Browsing for analysis, and asynchronously check the results of these submissions. 


## What this project does
The Web Risk demo can be used with the Google Cloud WebRisk APIs to access the Google Cloud WebRisk lists of unsafe web resources. Inside the directory, you can find two programs: 
    webrisk_cmd.py and app.py. 
    The app program creates a web server to check safe/unsafe URLs and submit unsafe URLs. 
    The webrisk_cmd program is a command line service that can  be used to do the same thing.


## Language

The webapp is developed using  Flask 2.1.0/Python 3.10.8
The CLI app is developed using Python 3.9.6


## Installation

Install all the required packages from the requirements.txt :

```bash
  pip install -r requirements.txt
```

## Run Locally

Create file myconfig.py with below contents:
```bash
PROJECT_ID="<YOUR GCP PROJECT ID>"
WEBRISK_API_KEY='<YOUR WEB RISK API KEY'
  ```  
Create private key for Web Risk Service Account. Download the file that contains the private key and save it as 
```bash
service-account-webrisk.json
```  
  

After installing all required packages run the application by either of the below commands:

```bash
  python3 webrisk_cmd.py
  python3 app.py
```    
