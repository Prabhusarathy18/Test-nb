import requests
import datetime
import json
from base64 import b64encode
from base64 import b64decode



# # response = get('https://api.github.com/user', auth=('username', 'e52c121f8680c8ab7d5ae02d538b6f1c8655f61b'))
# response = get('https://api.github.com/user', auth=('Prabhusarathy18', 'praeng@16'))
token="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"
headers = {'Authorization': 'token ' + token}
#check token is valid
def get_user_name(token):
    headers = {'Authorization': 'token ' + token}
    response=requests.get("https://api.github.com/user",headers=headers)
    if response.status_code==200:
        for key, value in response.json().items():
            print(key, value)




def token_validator(token):
    headers = {'Authorization': 'token ' + token}
    response=requests.get("https://api.github.com/user",headers=headers)
    if response.status_code==200:
        for key, value in response.json().items():
            if key=="login":
                return value
    elif response.status_code==401:
        return  "Unauthorized"

#method to list repos
def list_repos():
    response = requests.get('https://api.github.com/user/repos', headers=headers)
    data=(response.json())
    repos=[]
    for iterator in range(len(data)):
        for key, value in data[iterator].items():
            if key=="full_name":
                repos.append(value)
    print(repos)


#method to list branches of specified repo
def list_branches(repo_name):
    url="https://api.github.com/repos/"+repo_name+"/branches"
    response = requests.get(url, headers=headers)
    branches=[]
    for iterator in range(len(response.json())):
        for key, value in response.json()[iterator].items():
            if key=="name":
                branches.append(value)

    print(branches)


#method to commit and push the code
def commit_and_push(commitMessage,localFileName,remoteFilepath,branch,user,repo_name):

    #File into byte
    with open(localFileName, 'rb') as open_file:
        byte_content = open_file.read()
    base64_bytes = b64encode(byte_content)
    base64_string_file = base64_bytes.decode('utf-8')

    url="https://api.github.com/repos/"+user+"/"+repo_name+"/contents/"+remoteFilepath
    try:
        response = requests.get(url, headers=headers)
        #To update in existing file
        if len(response.json())>2:
            for key,value in response.json().items():
                if key=="sha":
                    sha_value=value
                    commit_response=requests.put(url,headers=headers,data = json.dumps(
                        {
                            'message': commitMessage, 'content':base64_string_file,'sha':sha_value,'branch':branch
                        }
                    ))
                    if commit_response.status_code==200:
                        print("Successfully commited")
                    else :
                        print("Failed with code ", commit_response.status_code)

        #To create a new file
        else:
            commit_response= requests.put(url, headers=headers, data=json.dumps(
                {
                    'message': commitMessage, 'content': base64_string_file,'branch': branch
                }
            ))
            if commit_response.status_code ==200:
                print("Successfully commited")
            elif commit_response.status_code ==201:
                print("Successfully created")
            else:
                print("Failed with code",commit_response.status_code)
    except:
        print("Got Exception")


def create_file():
    headers = {'Authorization': 'Zoho-oauthtoken ' + "1000.66728eb6dced6be7b11faf0a28c9da12.9060aa96f5233eef55803ab467d4e500"}
    url="https://apidocs.zoho.com/files/v1/upload".strip()
    response=requests.post(url,headers=headers,data = json.dumps(
        {
           'filename':'dummy.txt',"content":"Hii im prahu"
        }
    )
    )
    print((response.json()))


PATH_FOR_NOTEBOOK = "/Users/prabhu-pt3030/NAAS/Notebook-subs/"
def pull():
    user = "Prabhusarathy18"
    repo = "Test-nb"
    branch= "main"
    file_path="mk/dummy.py"
    interm = file_path.rfind('/')
    file_name = (file_path[interm + 1:])

    url="https://api.github.com/repos/"+user+"/"+repo+"/contents/"+file_path+"?ref="+branch
    response = requests.get(url, headers=headers)
    file_content=(response.json()['content'])
    file_content_encoded = b64decode(file_content)
    file_obj = open(PATH_FOR_NOTEBOOK+file_name, "w+")
    file_obj.write(file_content_encoded.decode('utf-8'))


final_reponse = []
def get_file_list():
    global  final_reponse;
    final_reponse = []
    user = "Prabhusarathy18"
    repo = "Test-nb"
    branch= "main"
    url = "https://api.github.com/repos/"+user+"/"+repo+"/contents?ref="+branch
    response = requests.get(url,headers=headers)
    for paths in response.json():
        if paths['type'] == 'file':
            if (paths['path'][paths['path'].rfind('.'): ]) == ".ipynb" :
                final_reponse.append(paths['path'])
        elif paths['type'] == 'dir':
            file_from_folder(user,repo,branch,paths['path'])
    print(final_reponse)


def file_from_folder(user,repo,branch,folder):
    global final_reponse;
    user = user
    repo = repo
    branch= branch
    url = "https://api.github.com/repos/"+user+"/"+repo+"/contents/"+folder+"?ref="+branch
    response = requests.get(url,headers=headers)
    for paths in response.json():
        if paths['type'] == 'file' :
            final_reponse.append(paths['path'])
        elif paths['type'] == 'dir':
            file_from_folder(user,repo,branch,paths['path'])

get_file_list()

# pull()
#Inserted line by first push
