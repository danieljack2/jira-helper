from jira import JIRA
from dotenv import load_dotenv
import os

load_dotenv()

JIRA_SERVER = os.getenv("JIRA_SERVER")
JIRA_USERNAME = os.getenv("JIRA_USERNAME")
JIRA_PASSWORD = os.getenv("JIRA_PASSWORD")

print("Jira:" + JIRA_SERVER)

# Create a Jira client
jira = JIRA(JIRA_SERVER, basic_auth=(JIRA_USERNAME, JIRA_PASSWORD))      

print("Authenticated, " + str(jira.myself()))

def transition_issue(issueKey: str, transitionName: str):
    transitionId = jira.find_transitionid_by_name(issueKey, transitionName)
    print(f'Transitioning issue {issueKey} to {transitionName} with transition id {transitionId}')
    jira.transition_issue(issueKey, transitionId)

def add_time(issueKey: str, time: str):
    jira.add_worklog(issueKey, time)

# Get all issues in the current sprint and all issues that i have logged time on in the current sprint
def get_my_issue_worklogs():
    current_user = jira.myself()
    # Get all issues assigned to the current user that are in the current sprint
    jql = f'(assignee = {current_user["accountId"]} AND sprint IN openSprints()) OR (worklogAuthor = currentUser() AND worklogDate >= -7d) ORDER BY created DESC'

    issueList = jira_search(jql)

    return format_issues(issueList, current_user)
    
#We want to prepare an object that looks like this:
# [{
#     "key": "SSEDXPD-6321",
#     "summary": "Create a new issue",
#     "status": "Done",
#     "parent": "SSEDXPD-6321",
#     "worklogs": {
#                   "worklogId": "1234567890",
#                   "started": "2025-01-24T14:11:31.220+1000",
#                   "timeSpentSeconds": 10800,
#               }
# }]
def format_issues(issueList: list, current_user: dict):
    issues = []

    for issue in issueList:
        # Get worklogs for each issue
        worklogList = jira.worklogs(issue.key)
        worklogs = []
            
        for worklog in worklogList:
            if str(worklog.author) == str(current_user["displayName"]):
                worklogs.append({
                    "worklogId": worklog.id,
                    "started": worklog.started,
                    "timeSpentSeconds": worklog.timeSpentSeconds
                    })
        
        # Get parent task if it exists
        parent = None
        if hasattr(issue.fields, 'parent'):
            parent = issue.fields.parent

        issues.append({
            "key": issue.key,
            "summary": issue.fields.summary,
            "status": issue.fields.status.name,
            "parent": parent,
            "worklogs": worklogs
        })

    return issues

    
def jira_search(jql: str):
    try:
        # Search for issues that match the JQL query
        issues = jira.search_issues(jql)

        return issues
    except Exception as e:
        print(f"Error: {e}")
        return []