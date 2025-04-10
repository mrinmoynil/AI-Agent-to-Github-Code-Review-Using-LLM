from urllib.parse import urlparse
import requests
import base64


def get_owner_repo_name(url):
    url_parsed=urlparse(url)
    #print(f"parsed url get_owner_repo_name :{url_parsed}")
    url_path_elements=url_parsed.path.strip("/").split("/")
    if(len(url_path_elements)>=2):
        owner,repo_name=url_path_elements[0],url_path_elements[1]
        #print(owner,repo_name)   
        return owner,repo_name
    return None,None


def fetch_pr_files(url,pr_number, github_token=None):
    owner,repo_name=get_owner_repo_name(url)
    #print(f"fetch_pr_files owner:{owner}, reponame:{repo_name}")
    files_url=f"http://api.github.com/repos/{owner}/{repo_name}/pulls/{pr_number}/files"
    headers = {"Authorization": f"token {github_token}"} if github_token else {}
    response = requests.get(files_url, headers=headers)
    response.raise_for_status()
    return response.json()

def fetch_file_contents(url,file_path, github_token=None):
    #print(f" url fetch_file_contents :{url}")
    owner,repo_name=get_owner_repo_name(url)  
    file_url=f"https://api.github.com/repos/{owner}/{repo_name}/contents/{file_path}"
    headers = {"Authorization": f"token {github_token}"} if github_token else {}
    response = requests.get(file_url, headers=headers)
    response.raise_for_status()
    contents=response.json()
    return base64.b64decode(contents["content"]).decode()
    
#print(fetch_file_contents(url,file_path="fx_rates/models.py"))
