# Purpose: Leverage NPM API and Python requests library to programmatically create new hosts in NPM
# Programmer: Kadar Anwar
# Language: Python 3.10.12
# Filename: npm_api_automation.py
# Date: 19 MAY 2024

# ---------
# Changelog
# ---------
#
# 19 MAY 2024 - v0.1 - initial code re-write
# 14 FEB 2025 - v0.2 - removed hardcoded domain name in command output; substitute {domain_name} from the .env file instead

import csv
import requests
import os
import json
from dotenv import load_dotenv

# Securely read in environment variables using .env files;
# this allows for flexibility in configuration while not exposing any
# sensitive information
load_dotenv()

api_key = os.getenv('API_KEY')
admin_url = os.getenv('ADMIN_URL')
certificate_id = os.getenv('CERTIFICATE')
domain_name = os.getenv('DOMAIN_NAME')

def create_host():
    # Read CSV file
    with open('proxy_hosts.csv', 'r') as file:
        csv_reader = csv.reader(file)
        
        for row in csv_reader:
#            print (row)
            
            # Extracting values from CSV
            sub = row[0]
            scheme = row[1]
            container_name = row[2]
            port = row[3]
            
            # Constructing URL for proxy host creation
            url = f"{admin_url}/api/nginx/proxy-hosts"
        
            # Data for the API call - not all values are used, un-comment accordingly
            data = {
                "domain_names": [sub+'.'+domain_name],
                "forward_scheme": scheme,
                "forward_host": container_name,
                "forward_port": port,
                "certificate_id": certificate_id,
                # "meta": {
                #     "letsencrpyt_agree": false,
                #     "dns_challenge": false
                # },
                # "advanced_config": "",
                # "locations": [],
                "block_exploits": "true",
                "caching_enabled": "true",
                # "allow_websocket_upgrade": "false",
                "http2_support": "true",
                # "hsts_enabled": "false",
                # "hsts_subdomains": "false",
                #"ssl_forced": "true",
                #"access_list_id": 0,
                "enabled": "true"
            }   
                
            headers = {
            "Authorization": f"Bearer" + api_key,
            "Content-Type": "application/json"
            }
            
            # Prettify JSON for debugging output
            pretty_data = json.dumps(data, indent=4)
            
            # Debugs can be un-commented for troubleshooting
            # print("======")
            # print("Payload to be sent to URL:"+' ' + url)
            # print("======")
            # print(pretty_data)

            #Make API call to create proxy host
            response = requests.post(url, json=data, headers={"Authorization":f"Bearer {api_key}"})

            # Status code explanations
            status_code_explanations = {
                200: "OK: The request was successful.",
                201: "Created: The request was successful and a resource was created.",
                400: "Bad Request: The request was invalid or cannot be otherwise served - this may mean the proxy host already exists, or there is an error in the CSV file.",
                401: "Unauthorized: Authentication is required and has failed or has not yet been provided.",
                403: "Forbidden: The request was valid, but the server is refusing action.",
                404: "Not Found: The requested resource could not be found.",
                405: "Method Not Allowed: A request method is not supported for the requested resource.",
                408: "Request Timeout: The server timed out waiting for the request.",
                500: "Internal Server Error: An error has occurred in the server.",
                502: "Bad Gateway: The server was acting as a gateway or proxy and received an invalid response from the upstream server.",
                503: "Service Unavailable: The server is not ready to handle the request. Common causes are a server that is down for maintenance or that is overloaded.",
                504: "Gateway Timeout: The server was acting as a gateway or proxy and did not receive a timely response from the upstream server."
            }

            # Handle response
            if response.status_code in status_code_explanations:
                print(f"HTTP {response.status_code}: {status_code_explanations[response.status_code]}")
                if response.status_code in (200, 201):
                    print(f"Proxy host for {sub}.{domain_name} created successfully")
                else:
                    print(f"There was an error in creating proxy host for {sub}.{domain_name} The returned status code was: {response.status_code}.")
            else:
                print(f"Received unexpected status code: {response.status_code}.")

def main():
    create_host()

main()