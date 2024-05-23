# Currently do not have admin provlages to aprove the Files.ReadWriteAll permission
# Will upload a script to search directory and return users with sufficient privlages after training

import xml.etree.ElementTree as ET
import msal
import requests

# Parse the XML file
tree = ET.parse('getCurrentTrainsXML.xml')
root = tree.getroot()

# Define the namespace used in the XML
namespace = {'ns': 'http://api.irishrail.ie/realtime/'}

# Find all TrainCode elements and save their text content to a list
train_codes = [train_code.text for train_code in root.findall('.//ns:TrainCode', namespace)]

# Save the train codes to a text file
filename = 'train_codes.txt'
with open(filename, 'w') as file:
    for code in train_codes:
        file.write(f"{code}\n")

# OneDrive authentication setup
client_id = '61271e58-ac6d-4c06-863c-1878c3fa4ccc'
client_secret = 'hWB8Q~CrdphxKAHTgcirOeCZqeHEOl3i9aNbxdCj'
tenant_id = '68818673-de12-4b6b-bed5-670dd7b7dff5'
authority = f'https://login.microsoftonline.com/{tenant_id}'
scopes = ['https://graph.microsoft.com/.default']

# Create a MSAL confidential client application
app = msal.ConfidentialClientApplication(
    client_id,
    authority=authority,
    client_credential=client_secret
)

# Acquire a token
result = app.acquire_token_for_client(scopes=scopes)

if "access_token" in result:
    # Upload the file to OneDrive using Microsoft Graph API
    with open(filename, 'rb') as file:
        response = requests.put(
            'https://graph.microsoft.com/v1.0/me/drive/root:/train_codes.txt:/content',
            headers={'Authorization': f'Bearer {result["access_token"]}'},
            data=file
        )
        if response.status_code == 201:
            print(f"File uploaded to OneDrive at: {response.json()['webUrl']}")
        else:
            print(f"Failed to upload file: {response.status_code}, {response.text}")
else:
    print("Failed to acquire token:", result.get("error"), result.get("error_description"))
