# GCP-Admin-SDK-API

0. Enable Google Workspace Admin SDK API through GCP Console.

1. Create a Service Account and Download key.json 
Create a Service Account from the Google Cloud Console.

Download the JSON key file (key.json) for authentication.

2. Domain-wide Delegation Setup
Domain-wide delegation is required.  

Steps: Log in to Google Admin Console using a super admin account.  

Navigate to: Home > Security > API Controls > Domain-wide Delegation  

Click Add New API Client  

Client ID: Use the client ID from your Service Account (visible in the GCP Console).  

OAuth Scopes: https://www.googleapis.com/auth/admin.directory.group.readonly
Note: You’ll need to manage where the key.json file is securely stored for API access.  

3. Data to Retrieve
- Group List
Retrieve metadata about Google Groups in the domain.

- Member List
Requires group ID to query.

Member data should be linked with corresponding group info (e.g., via join with the group table).  

🔎 Reference Links
Python example using Google Admin SDK:
https://developers.google.com/workspace/admin/directory/v1/quickstart/python

Domain-wide delegation documentation:
https://developers.google.com/classroom/guides/key-concepts/domain-wide-delegation

Admin SDK Group API reference:
https://developers.google.com/workspace/admin/directory/reference/rest/v1/groups/list
