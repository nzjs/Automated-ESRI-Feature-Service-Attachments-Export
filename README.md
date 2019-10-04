## Automated ESRI Feature Service Attachments Export
This script takes an input ESRI Feature Service, retrieves the online attachments, and stores them on a local server if they don't already exist (only download the latest images). It's also compatible with privately shared services by generating an ESRI token during runtime.

Additionally, if you have setup a SharePoint Online location to "Sync" with a local C:\ drive location, the attachments can be automatically synced to O365 via the OneDrive Sync application. 

Written for Python v3 and above.

### How to get started
- Customise these variables in the code: 
username, password, fs_base (base URL), outfolder_ (output location for images)
- Customise the retrieveAttachments() function to use your variable names
- Add more or remove FeatureService layer endpoints if required (script example comes with two)

### How do I get the OneDrive/SharePoint Online part working?
If you have an Office 365 subscription and also wish to replicate image attachments into a OneDrive folder or SharePoint Online library, this is what you need to do: 
- Create the folder location on OneDrive/SharePoint Online
- When viewing the folder contents in your web browser, click the "Sync" button
(The "Sync" process should now start between Office 365 and your machine)
- Now you effectively have a C:\ drive location which is a two-way replication of the OneDrive/SharePoint Online folder
- Simply use this C:\ path in the script parameters, and as long as OneDrive sync service is running on your server or machine, it will take care of the rest by adding new photos from this C:\ folder into your OneDrive/SharePoint Online location.
- Example path: `C:\Users\<your user>\<Office 365 org name>\<folder name of SharePoint Online>`

### Sample output for a single FeatureService layer:
```
Token generated: <AGOL token>

JSON response retrieved and converted to object

OID: 1 (Attachment ID: 1)  -  photo1-20190820-225444.jpg
>>> Downloaded file to server, syncing with SharePoint momentarily.

OID: 1 (Attachment ID: 2)  -  sketch-fb7b27d4a18244928de001999480babf.jpg
>>> Downloaded file to server, syncing with SharePoint momentarily.

OID: 6 (Attachment ID: 3)  -  photo1-20190912-033606.jpg
>>> Downloaded file to server, syncing with SharePoint momentarily.

OID: 7 (Attachment ID: 6)  -  photo1-20190912-015614.jpg
File already exists in output location.

OID: 7 (Attachment ID: 7)  -  sketch-dbaef0325ada45d3b8cbda642a1295a5.jpg
File already exists in output location.
```