import dropbox
import webbrowser
import Tkinter as tk
import tkFileDialog
import re



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

def getAudioFileInfo(audioFileDBLink):
    """
    Takes in direct Dropbox link of the form https://dl.dropboxusercontent.com/.../filename.filetype
    """

    # Reset variable values
    SongNumber = ''
    VariationLevel = ''
    VariationType = ''
    VariationNumber = ''
    fileType = ''

    #Remove all but filename.filetype
    dontcare2, audioFileName = audioFileDBLink.rsplit('/', 1)
 
    #Split the filename.filetype
    splitFileName = re.split("[_\.]", audioFileName)
    numFileNameParts = len(splitFileName)
    fileType = splitFileName[-1] # The last item in the list will be the filetype (e.g. mp3, wav)
    # insert error checker here?
    SongNumber = getSongNumber(splitFileName[0])
    VariationLevel = getVarLevel(splitFileName[1])
    if numFileNameParts == 4:
        if splitFileName[2].isalpha():
            # It is a variation type
            VariationType = getVarType(splitFileName[2])
        else:
            #It is a variation number
            VariationNumber = getVarNum(splitFileName[2])
    
    if numFileNameParts == 5:
        VariationType = getVarType(splitFileName[2])
        VariationNumber = getVarNum(splitFileName[3])

    #HTML filename synthesis
    htmlFileName = "play"+ VariationLevel + VariationNumber + VariationType + "song" + SongNumber + ".html"
    return htmlFileName

def getSongNumber(fn):
    sn =  fn.strip('song')
    return sn

def getVarLevel(fn):
    vl = fn
    return vl + '_'

def getVarType(fn):
    vt = fn
    return vt + '_'

def getVarNum(fn):
    vn = fn
    return vn + '_'

    
def futureErrorChecker():
    match = re.match('song\d+', splitFileName[0])
    if match:
        sn =  splitFileName[0].strip('song')
    return True

# Import app key and secret from external file
authDict = dict()
with open("auth.txt") as allAuth:
    for line in allAuth:
        elementName, element = line.rstrip().split(': ')
        authDict[elementName] = element
elementName = None
element = None

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
linkedAccountInfo = client.account_info()

print "Linked account --"

for key in linkedAccountInfo:
    print '\t' + key + " : " + str(linkedAccountInfo[key])

print

# Select audio files
audioFileNames = []
audioDropboxPaths = []
root = tk.Tk()
root.withdraw()
audioFilePaths = tkFileDialog.askopenfilenames(title='Select audio files')
audioFilePathsList = root.tk.splitlist(audioFilePaths)
for item in audioFilePathsList:
    print '\n' + item
    dontCare, audioFileName = item.rsplit('/', 1)
    audioFileNames.append(audioFileName)
    audioDropboxPaths.append('Audioplayer/audio files/'+audioFileName)
    print "Opening", audioFileName
    with open(item, 'rb') as audioUpload:
        print "Uploading", audioFileName
        uploadResponse = client.put_file(audioDropboxPaths[-1], audioUpload)

# Get & transform audio file links
audioLinks = []
for item in audioDropboxPaths:
    resdict = client.share(item, short_url=False)
    x, dirtyLink = resdict.items()[0]
    cleanLink = str(dirtyLink)
    audioLinks.append(dbLinkTransform(cleanLink))

# Create HTML filenames from audio filenames
filenames = {}
for item in audioLinks:
    htmlName = getAudioFileInfo(item)
    filenames[item] = htmlName # filenames is a dictionary with audio dropbox direct link keys and html file values

# Add links to HTML template
# Open dropbox html template
templateObject = client.get_file('Audioplayer/template/htmlaudiotemplate.html')
template = templateObject.read()

HTMLDropboxPaths = []
print '\nUploading HTML files...'
with client.get_file('Audioplayer/template/htmlaudiotemplate.html') as templateObject:
    template = templateObject.read()
    for key in filenames:
        updatedTemplate = template.replace('INSERTDROPBOXDIRECTLINKHERE', key)
        HTMLDropboxPaths.append('Audioplayer/HTML files/'+ filenames[key])
        print "\nUploading to \"Audioplayer/HTML files/" + filenames[key] + "\""
        uploadhtmlResponse = client.put_file(HTMLDropboxPaths[-1], updatedTemplate)
        

    
# Get & transform HTML document links
HTMLLinks = []
for item in HTMLDropboxPaths:
    resdict = client.share(item, short_url=False)
    x, dirtyLink = resdict.items()[0]
    cleanLink = str(dirtyLink)
    HTMLLinks.append(dbLinkTransform(cleanLink))

# Output transformed HTML links

# Text file
outputTextFile = open("OutputLinks.txt", 'w+')
HTMLLinksNewlines = [x + '\n' for x in HTMLLinks]
audioLinksNewlines = [x + '\n' for x in audioLinks]
outputTextFile.write("-" * 30 + "LINKS TO HTML FILES" + "-" * 31 + '\n')
outputTextFile.writelines(HTMLLinksNewlines)
outputTextFile.write('-' * 80 + '\n' *2)
outputTextFile.write("-" * 30 + "LINKS TO AUDIO FILES" + "-" * 30 + '\n')
outputTextFile.writelines(audioLinksNewlines)
outputTextFile.write('-' * 80)
outputTextFile.close()


# Console display
print '\n'* 10
print "-" * 30 + "LINKS TO HTML FILES" + "-" * 31
print
for item in HTMLLinks:
    print item

print '-' * 80
print '\n' * 3
print "For a text file of these output links, please see \"OutputLinks.txt\" \n in this script's root directory"