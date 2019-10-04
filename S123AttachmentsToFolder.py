################################################################
# This script takes an input ESRI Feature Service, retrieves the online attachments, stores them on a local server. 
# Additionally, if you have setup a SharePoint Online location to "Sync" with a local C:\ drive location, the attachments can be 
# automatically synced to O365 via the OneDrive Sync application. 
# # Developed by John Stowell, 2019
#
# Call this script with     python "..\S123AttachmentsToSharepoint.py"
#
# Attachment URL structure: https://services5.arcgis.com/###/arcgis/rest/services/{FEATURE_NAME}/FeatureServer/0/OBJECTID/attachments/ATTACHMENTID?token=###
# Eg. https://services6.arcgis.com/Whb8vGWSmNkavSpL/ArcGIS/rest/services/service_3c1b58d6f75846c7bd82f3e2c3e71a99/FeatureServer/0/9/attachments/1?token=###
#
# Customise these variables in the code below: 
# username, password, fs_base_*, outfolder_*
################################################################

import os
import os.path
import json
import urllib
import urllib.request
import requests
import subprocess

# Generate a temporary API token for accessing the REST endpoints
def generateToken():
    try:
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
        return tokenJson['token']
    except Exception as token_ex:
        print("\t\t Error generating token : Code " + str(tokenResponse.text) + " : " + str(token_ex))
        pass

token = generateToken()
print('Token generated: ' + str(token))
print()
# Enter the FeatureServer URL that you want to sync/download attachments from, with a trailing slash /.
# Eg. r"https://services3.arcgis.com/za4HjpHWqnA4SFnH/arcgis/rest/services/service_22d11beafd254fd2852807d4062144bc/FeatureServer/0/"
# In the example below, I have two separate surveys that I want to sync attachments from. The retrieveAttachments() function below allows us to use mutliple inputs.
fs_base_WQ = r"<FeatureServer URL # 1>"
fs_base_RFWL = r"<FeatureServer URL # 2>"
definitionQuery = r"?objectIds=&globalIds=&definitionExpression=1%3D1&attachmentsDefinitionExpression=&attachmentTypes=&size=&keywords=&resultOffset=&resultRecordCount=&f=pjson&token="
attachURL_WQ = fs_base_WQ + "queryAttachments" + definitionQuery + str(token)
attachURL_RFWL = fs_base_RFWL + "queryAttachments" + definitionQuery + str(token)
outfolder_WQ = r"C:\Users\<user>\<Office 365 org name>\<folder where SharePoint Online is syncing # 1>"
outfolder_RFWL = r"C:\Users\<user>\<Office 365 org name>\<folder where SharePoint Online is syncing # 2>"

# Variables commented out below ... 
# Instead we're relying on the OneDrive sync client for automated syncing between a local C: location and SharePoint Online.

#outfolder_WQ = r"\\<server>\Survey123 Data\S123 Images - Water Quality"
#outfolder_RFWL = r"\\<server>\Survey123 Data\S123 Images - Rainfall and Water Level"
#sharepoint_WQ = r"<sharepoint online URL>"
#sharepoint_RFWL = r"<sharepoint online URL>"


################################################################
# Do not customise below this line
################################################################

# Define the retrieveAttachments() function:
# Read the json response from our GeoJSON URL, change the JSON string into a JSON object (data)
# Then retrieve the relevant attachments and store in our output folder.

def retrieveAttachments(attach_url, base_url, out_folder, token):
    jsonResponse = urllib.request.urlopen(attach_url)
    data = json.loads(jsonResponse.read())
    print('JSON response retrieved and converted to object')
    print()
    for parentObject in data['attachmentGroups']:
        for attachmentInfo in parentObject['attachmentInfos']:
            try:
                print('OID: ' + str(parentObject['parentObjectId']) + ' (Attachment ID: '+str(attachmentInfo.get('id')) + ')  -  ' + str(attachmentInfo.get('name')))
                img_url = (str(base_url) + str(parentObject['parentObjectId']) + '/attachments/' + str(attachmentInfo.get('id')) + '?token=' + str(token))
                file_name = ('OID' + str(parentObject['parentObjectId']) + '-' + str(attachmentInfo.get('name'))) # attachmentInfo.get('globalId')
                #print('Compiled Image URL:')
                #print(img_url)
                if os.path.exists(out_folder+'\\'+file_name):
                    print('File already exists in output location.')
                    print()
                else:
                    urllib.request.urlretrieve(img_url, out_folder+'\\'+file_name)
                    print('>>> Downloaded file to server, syncing with SharePoint momentarily.')
                    print()
            except Exception as retrieve_ex:
                print("\t\t Error retrieving image : " + str(parentObject['parentObjectId']) + ' : ' + str(attachmentInfo) + " : " + str(retrieve_ex))
                continue


# Run the functions to get attachments for our respective survey forms
retrieveAttachments(attachURL_RFWL, fs_base_RFWL, outfolder_RFWL, token)
retrieveAttachments(attachURL_WQ, fs_base_WQ, outfolder_WQ, token)

# Attachments downloaded are stored in the local SharePoint sync folder, and will be 
# synced online automatically as long as our onedrive service is running.

print('Finished')
print()
