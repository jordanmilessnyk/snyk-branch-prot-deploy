import requests
import json

# Example usage
gh_token = "<GH_TOKEN>"

snyk_token = "<SNYK_TOKEN>"
snyk_group = "<SNYK_GROUP>"

def get_snyk_orgs():
    
    data = []
    url = f"https://api.snyk.io/rest/groups/{snyk_group}/orgs?version=2024-08-25"
    headers = {
        "Authorization": f"token {snyk_token}",
        "Content-Type": "application/vnd.api+json"
    }

    while url:

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data.extend(response.json()["data"])
            try:
                url = f"https://api.snyk.io{response.json()["links"]["next"]}" if response.json()["links"]["next"] else None

            except KeyError:
                print(f"No next link found for orgs in group {snyk_group}.")
                url = None
        else:
            print(f"Failed to retrieve org for org {org_id}: {response.status_code}")
            data.extend([])
            url = None
    
    return data


def get_snyk_targets(org_id):
    
    data = []
    url = f"https://api.snyk.io/rest/orgs/{org_id}/targets?version=2024-08-25"
    headers = {
        "Authorization": f"token {snyk_token}",
        "Content-Type": "application/vnd.api+json"
    }


    while url:
        
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data.extend(response.json()["data"])
            try:
                url = f"https://api.snyk.io{response.json()["links"]["next"]}" if response.json()["links"]["next"] else None
            except KeyError:
                print(f"No next link found for targets in org {org_id}.")
                url = None
        else:
            print(f"Failed to retrieve targets for org {org_id}: {response.status_code}")
            data.extend([])
            url = None
    
    return data


def get_all_orgs_and_targets():
    
    orgs = get_snyk_orgs()
    all_orgs = {}

    for org in orgs:
        org_id = org["id"]
        targets = get_snyk_targets(org_id)
        if targets:
            all_orgs[org_id] = {"org_name": org["attributes"]["name"], "targets": targets}
    return all_orgs

def create_required_status_check(repo_name, org_name):
    
    url = f"https://api.github.com/repos/{repo_name}/rulesets"
    headers = {
        "Authorization": f"token {gh_token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version":"2022-11-28"
    }
    payload = {
        "name": "Required Status Checks",
        "target": "branch",
        "enforcement": "active",
        "conditions": {
            "ref_name": {
                "include": ["refs/heads/master"],
                "exclude": []
            }
        },
        "rules": [
            {
                "type": "required_status_checks",
                "parameters": {
                    "required_status_checks": [
                        {
                            "context": f"security/snyk ({org_name})"
                        },
                        {
                            "context": f"code/snyk ({org_name})"
                        }
                    ],
                    "strict_required_status_checks_policy": False
                }
            }
        ]
    }

    print("Payload:", json.dumps(payload, indent=2))

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 201:
        print(f"Ruleset created successfully for {repo_name}.")
    else:
        print(f"Failed to create ruleset: {response.status_code}")
        print(response.json())




if __name__== "__main__":
    
    all_orgs = get_all_orgs_and_targets()
    
    for org_id in all_orgs:
        org_info = all_orgs[org_id]
        for target in org_info["targets"]:
            create_required_status_check(target["attributes"]["display_name"], org_info["org_name"])