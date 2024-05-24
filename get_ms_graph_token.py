import msal
import requests
import webbrowser
from flask import Flask, request

app = Flask(__name__)

# Azure AD credentials
client_id = 'YOUR_CLIENT_ID'
client_secret = 'YOUR_CLIENT_SECRET'
tenant_id = 'YOUR_TENANT_ID'
authority = f'https://login.microsoftonline.com/{tenant_id}'
redirect_uri = 'http://localhost:5000/getAToken'
scopes = ['Files.ReadWrite.All', 'User.Read']

# Create a MSAL confidential client application
msal_app = msal.ConfidentialClientApplication(
    client_id,
    authority=authority,
    client_credential=client_secret
)

@app.route('/')
def homepage():
    auth_url = msal_app.get_authorization_request_url(scopes, redirect_uri=redirect_uri)
    return f'<a href="{auth_url}">Click here to authenticate</a>'

@app.route('/getAToken')
def authorized():
    code = request.args.get('code')
    result = msal_app.acquire_token_by_authorization_code(code, scopes=scopes, redirect_uri=redirect_uri)
    if "access_token" in result:
        access_token = result['access_token']
        return f"Access token acquired: {access_token}"
    else:
        return f"Failed to acquire token: {result.get('error')}, {result.get('error_description')}"

if __name__ == '__main__':
    webbrowser.open('http://localhost:5000')
    app.run(port=5000)

# Additional functionality can be added here to use the acquired access token for API calls.
