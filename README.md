# Manifest2Inventory
This application helps to quickly convert K8s Manifest YAML File to Inventory Filters inside Tetration Analytics Scope.

## Table of contents
* [Installation](#Installation)
* [Screenshots](#screenshots)
* [How to Use](#UserGuide)
* [Files](#Files)
* [Steps to run](#Steps)
* [Feedback and Author](#Feedback)

## Installation

From sources

Download the sources from [Github](https://github.com/leeahnduk/Manifest2Inventory.git), extract and execute the following commands

```
$ pip3 install -r requirements.txt

```

## Screenshots
![Run screenshot](https://github.com/leeahnduk/Manifest2Inventory/blob/master/Manifest2Inv.jpg)
![Result screenshot](https://github.com/leeahnduk/Manifest2Inventory/blob/master/Result.jpg)
## UserGuide
How to use this application:
To access to the cluster you need to get the API Credentials with the following permissions
* `sensor_management` - option: SW sensor management: API to configure and monitor status of SW sensors
* `hw_sensor_management` - option: HW sensor management: API to configure and monitor status of HW sensors
* `flow_inventory_query` - option: Flow and inventory search: API to query flows and inventory items in Tetration cluster
* `user_role_scope_management` - option: Users, roles and scope management: API for root scope owners to read/add/modify/remove users, roles and scopes
* `app_policy_management` - option: 
 Applications and policy management: API to manage applications and enforce policies

Download the api_credentials.json locally and have it ready to get the information required for the setup.

A quick look for the help will list the current available options.
To start the script, just use: `python3 manifest2inventories.py --url https://tet-cluster-ip --credential api_credentials.json --yaml Manifest.yaml`

## Files
Need to prepare K8s Manifest YAML file. The sample Manifest file is in the github folder.


## Steps

Step 1: Issue `$ pip3 install -r requirements.txt` to install all required packages.

Step 2: To run the apps: `python3 manifest2inventories.py --url https://tet-cluster-ip --credential api_credentials.json --yaml Manifest.yaml`

Step 3: Answer all the questions about scope and namespace to create Inventory Filters.


## Feedback
Any feedback can send to me: Le Anh Duc (leeahnduk@yahoo.com or anhdle@cisco.com)
