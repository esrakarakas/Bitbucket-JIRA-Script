import requests

def createProject(projectName, key):
  response = requests.post("localhost:8080/bitbucket/rest/api/1.0/projects", json={"name": "{}".format(projectName), "key": "{}".format(key)}, headers={"Content-Type": "application/json"})
  return response

def createRepository(repositoryName, key):
  response = requests.post("localhost:8080/bitbucket/rest/api/1.0/projects/{}/repos".format(key), json={"name": "{}".format(repositoryName), "scmId": "git", "forkable": "true"}, headers={"Content-Type": "application/json"})
  return response

def checkProjectExist(key):
    response = requests.get("localhost:8080/bitbucket/rest/api/1.0/projects/{}".format(key))
    if response.status_code == 404:
      return False
    else:
      return True

r = requests.get("localhost:8080/JIRA/rest/api/2/search?jql=project=BR AND statusCategory='To Do'")
r=r.json()
for issue in r['issues']:
  projectName = issue['fields']['customfield_10200']
  repositoryName = issue['fields']['customfield_10201']
  key = projectName.strip().replace(" ","")
  key2 = issue['key']
  if not checkProjectExist(key):
    responseCreateProject = createProject(projectName, key)
  responseCreateRepository = createRepository(repositoryName, key)
  if responseCreateRepository.status_code == 201:
    r = requests.post("localhost:8080/JIRA/rest/api/2/issue/{}/transitions?expand=transitions.fields".format(key2), json={"transition": {"id": "21"}}, headers={"Content-Type": "application/json"})
