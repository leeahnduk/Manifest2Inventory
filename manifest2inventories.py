# =================================================================================

from tetpyclient import RestClient
import tetpyclient
import json
import requests.packages.urllib3
import sys
import os
import argparse
import time
import csv
import yaml
import pandas as pd

# =================================================================================
# python3 manifest2inventories.py --url https://192.168.30.4 --credential api_credentials.json --yaml multicloud.yaml
# See reason below -- why verify=False param is used
# feedback: Le Anh Duc - anhdle@cisco.com
# =================================================================================
requests.packages.urllib3.disable_warnings()

# ====================================================================================
# GLOBALS
# ------------------------------------------------------------------------------------

parser = argparse.ArgumentParser(description='Script to convert K8s Manifest YAML File to Inventory Filter')
parser.add_argument('--url', help='Tetration URL', required=True)
parser.add_argument('--credential', help='Path to Tetration json credential file', required=True)
parser.add_argument('--yaml', help='Path to Manifest YAML File', required=True)
args = parser.parse_args()

'''
====================================================================================
Class Constructor
------------------------------------------------------------------------------------
'''
def CreateRestClient():
    # create Rest Client connection to Tetration URL with credential JSON file
    rc = RestClient(args.url,
                    credentials_file=args.credential, verify=False)
    return rc

def GetApplicationScopes(rc):
    # Input:
    resp = rc.get('/app_scopes')

    if resp.status_code != 200:
        print("Failed to retrieve app scopes")
        print(resp.status_code)
        print(resp.text)
    else:
        return resp.json()

def GetAppScopeId(scopes,name):
    try:
        return [scope["id"] for scope in scopes if scope["name"] == name][0]
    except:
        print("App Scope {name} not found".format(name=name))

def CreateInventoryFilters(rc,scopes):
    inventoryDict = {}
    ParentScope = input ("Which parent Scope (RootScope:SubScope) you want to define your inventory Filter: ") 
    NameSpace = input ("Which NameSpace in K8s you defined your apps: ")
    with open(args.yaml, 'r') as yaml_in:
        yaml_object = yaml.load_all(yaml_in) # yaml_object will be a list or a dict
        for doc in yaml_object:
            if doc is not None:
                if (doc['kind'] == 'Deployment'):
                    inventoryDict[doc['metadata']['name']] = {}
                    inventoryDict[doc['metadata']['name']]['app_scope_id'] = GetAppScopeId(scopes,ParentScope)
                    inventoryDict[doc['metadata']['name']]['name'] = doc['metadata']['name']
                    inventoryDict[doc['metadata']['name']]['short_query'] = {
                        "type" : "and",
                        "filters" : [
                            {
                                "type": "eq",
                                "field": "user_orchestrator_name",
                                "value": doc['metadata']['name']
                            },
                            {
                                "type": "eq",
                                "field": "user_orchestrator_system/namespace",
                                "value": NameSpace
                            }]
                    }
                    if inventoryDict[doc['metadata']['name']]['app_scope_id'] != GetAppScopeId(scopes,ParentScope):
                        print("Parent scope does not match previous definition")
                        continue

                if (doc['kind'] == 'Service'):
                    inventoryDict[doc['metadata']['name']] = {}
                    inventoryDict[doc['metadata']['name']]['app_scope_id'] = GetAppScopeId(scopes,ParentScope)
                    inventoryDict[doc['metadata']['name']]['name'] = doc['metadata']['name']
                    inventoryDict[doc['metadata']['name']]['short_query'] = {
                        "type" : "and",
                        "filters" : [
                            {
                                "type": "eq",
                                "field": "user_orchestrator_system/service_endpoint",
                                "value": doc['metadata']['name']
                            },
                            {
                                "type": "eq",
                                "field": "user_orchestrator_system/namespace",
                                "value": NameSpace
                            }]
                    }
                    if inventoryDict[doc['metadata']['name']]['app_scope_id'] != GetAppScopeId(scopes,ParentScope):
                        print("Parent scope does not match previous definition")
                        continue

    return inventoryDict

def PushInventoryFilters(rc,inventoryFilters):
    for inventoryFilter in inventoryFilters:
        req_payload = inventoryFilters[inventoryFilter]
        resp = rc.post('/filters/inventories', json_body=json.dumps(req_payload))
        if resp.status_code != 200:
            print("Error pushing InventorFilter")
            print(resp.status_code)
            print(resp.text)
        else:
            print("Inventory Filters successfully pushed for " + inventoryFilters[inventoryFilter]["name"])


def main():
    rc = CreateRestClient()
    scopes = GetApplicationScopes(rc)
    inventoryFilters = CreateInventoryFilters(rc,scopes)
    PushInventoryFilters(rc,inventoryFilters)

if __name__ == "__main__":
    main()
