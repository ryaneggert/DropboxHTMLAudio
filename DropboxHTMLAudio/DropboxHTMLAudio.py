import dropbox
import webbrowser


# Import app key and secret from external file
authDict = dict()
with open("auth.txt") as allAuth:
    for line in allAuth:
        elementName, element = line.rstrip().split(': ')
        authDict[elementName] = element
elementName = None
element = None
print authDict.keys()

# Get your app key and secret from the Dropbox developer website
app_key = authDict['app_key']
app_secret = authDict['app_secret']

# Ask for account to determine authentication method
whichDB = raw_input("Would you like to use the mockups dropbox? (y/n): ").strip()
if whichDB == 'n':
    # Use a different dropbox account. Use OAuth2 Authentication
    flow = dropbox.client.DropboxOAuth2FlowNoRedirect(app_key, app_secret)
    # Have the user sign in and authorize this token
    authorize_url = flow.start()
    print '1. Go to: ' + authorize_url
    print '2. Click "Allow" (you might have to log in first)'
    print '3. Copy the authorization code.'
    webbrowser.open_new_tab(authorize_url)
    code = raw_input("Enter the authorization code here: ").strip()

    # This will fail if the user enters an invalid authorization code
    access_token, user_id = flow.finish(code)
else:
    # Use the mockups dropbox account. We already have the access token
    access_token = authDict['CVaccesstoken']

client = dropbox.client.DropboxClient(access_token)
print 'linked account: ', client.account_info()


