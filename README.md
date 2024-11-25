# snyk-branch-prot-deploy
## Deploy Branch Protection rules across your repos for Snyk security checks
This script is designed to retrieve all targets in your Snyk environment and apply branch protection rules to them. Currently, Snyk's PR check names are in the format of `<check_type>/snyk (<org_name>)` making it difficult to apply rules across your Github repos quickly and easily. This tool takes into account which organizations your targets are imported into and creates the rulesets accordingly.

To get started:

1. update the `gh_token`, `snyk_token`, and `snyk_group` values at the top of of the script. The Github token needs to have permissions to create rulesets and the Snyk token should be for a user that has access to all of the organizations in your group
2. Adjust the payload as needed: 

![image](https://github.com/user-attachments/assets/14f073c0-5ad4-40a4-b097-7ae939821dc9)

To add or remove checks, adjust the `context` objects. To change the branch this ruleset relates to, change the values in the `inclued` list. For a full list of available configurations, check [here](https://docs.github.com/en/rest/repos/rules?apiVersion=2022-11-28#create-a-repository-ruleset)

## Caveats
1. The script currently only works for Github environments.
2. The script doesn't take into account if you actually have PR checks turned on for those Snyk organizations. If you do not, the Ruleset will get created but will hang since the check doesn't actually exist. When we expose the setting for Snyk Code in the API, a future consideration will be to check the organization configurations first
3. The script doesn't take into account repos imported into multiple Snyk orgs. If you have them imported multiple times, you may see duplicate or overwritten results.

