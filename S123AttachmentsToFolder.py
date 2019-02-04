"""
This script takes an input ESRI Feature Service, retrieves the online attachments, and exports them to a specified location.
(It's also compatible with private services by generating a token for the service.)
Developed by John Stowell, 2018

Call this script with:  python "..\S123AttachmentsToFolder.py"

Attachment URL structure: https://services5.arcgis.com/###/arcgis/rest/services/{FEATURE_NAME}/FeatureServer/0/OBJECTID/attachments/ATTACHMENTID?token=###

Customise these variables in the code below: 
username, password, dataset, and outFolder
"""

import os
import json
import urllib
import requests
import subprocess

# Generate a temporary API token for accessing the REST endpoints
tokenURL = 'https://www.arcgis.com/sharing/rest/generateToken?f=pjson' 
payload = { 'username': 'ARCGIS ONLINE USERNAME',
            'password': 'ARCGIS ONLINE PASSWORD',
            'referer': 'https://www.arcgis.com'
            }     # Set POST fields here 
                    # Eg. &username=user&password=password&referer=https://www.arcgis.com

tokenResponse = requests.post(tokenURL, data=payload)
# Enable printing below for testing
#print(response.text) #TEXT/HTML
#print(response.status_code, response.reason) #HTTP
tokenJson = tokenResponse.json()
token = tokenJson['token']

dataset = r"https://services6.arcgis.com/Whb8vGWSmNkavSpL/ArcGIS/rest/services/service_3c1b58d6f75846c7bd82f3e2c3e71a99/FeatureServer/0/"
s123GeoJSON = dataset + "query?where=objectid+%3D+objectid&outfields=*&f=json&token="
s123dataURL = s123GeoJSON + token
attachmentsGeoJSON = dataset + "queryAttachments?objectIds=&globalIds=&definitionExpression=1%3D1&attachmentsDefinitionExpression=&attachmentTypes=&size=&keywords=&resultOffset=&resultRecordCount=&f=pjson&token="
attachURL = attachmentsGeoJSON + token
outFolder = r"\\<SERVER>\Extracts\ArcGIS\Survey123\Attachments"  

print 'Token generated: ' + token
print ''
################################################################
# Do not customise below this line
################################################################

# Read the json response from our GeoJSON URL, 
# then change the JSON string into a JSON object (data)
jsonResponse = urllib.urlopen(attachURL)
data = json.loads(jsonResponse.read())

print 'JSON response retrieved and converted'
print ''

for parentObject in data['attachmentGroups']:
    for attachmentInfo in parentObject['attachmentInfos']:
        print('ID: '+str(attachmentInfo.get('id')) + '  -  ' + str(attachmentInfo.get('globalId')))
        print 'Compiled Image URL:'
        imageURL = (dataset + str(parentObject['parentObjectId']) + '/attachments/' + str(attachmentInfo.get('id')) + '?token=' + token)
        fileName = ('OID' + str(parentObject['parentObjectId']) + '-' + str(attachmentInfo.get('name')))
        print imageURL
        urllib.urlretrieve(imageURL, outFolder+'\\'+fileName)
        print outFolder+fileName
        print ''

print 'Finished, exported images to: \n' +  outFolder
print ''
