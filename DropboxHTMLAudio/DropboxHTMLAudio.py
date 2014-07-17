import dropbox
import webbrowser
import Tkinter as tk
import tkFileDialog


def dbLinkTransform(inLink):
    """
    takes a input dropbox link [inLink] (string) of form
    "https://www.dropbox.com/.../filename.txt"
    and transforms it to the direct link of form
    "https://dl.dropboxusercontent.com/.../filename.txt".
    This is output as a string.
    """
    outLink = inLink.replace('www.dropbox','dl.dropboxusercontent')
    return outLink



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

# Construct a dropbox client instance 
client = dropbox.client.DropboxClient(access_token)
print 'linked account: ', client.account_info()

# Select audio files
audioFileNames = []
root = tk.Tk()
root.withdraw()
audioFilePaths = tkFileDialog.askopenfilenames(title='Select audio files')
audioFilePathsList = root.tk.splitlist(audioFilePaths)
for item in audioFilePathsList:
    print item
    dontCare, audioFileName = item.rsplit('/', 1)
    audioFileNames.append(audioFileName)
    print "Opening", audioFileName
    with open(item, 'rb') as audioUpload:
        print "Uploading", audioFileName
        uploadResponse = client.put_file('Audioplayer/audio files/'+audioFileName, audioUpload)

# Get audio file links


# Transform audio links


# Add links to HTML template


# Get HTML document links


# Transform HTML links


#Output transformed HTML links
