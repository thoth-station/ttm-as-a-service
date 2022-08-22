# Time to Merge (TTM) as a Service

TTM is a model that classifies a GitHub PR into 1 of 10 time categories ranging from under a minute to over 4 days.

- Model training: https://github.com/aicoe-aiops/ocp-ci-analysis/tree/master/notebooks/time-to-merge-prediction/thoth-station
- Model usage: https://github.com/aicoe-aiops/ocp-ci-analysis/tree/master/models/thoth-support-github-ttm

This repo takes the TTM model and turns it into a service. This repo hosts a bot that uses GitHub webhooks to respond to pull requests.
Currently, any user that installs the bot is assigned to use the Thoth trained bot. In the future, there will be a flow that 
auto-trains on an org or set of repos.

## Output classes
- 0-1 mins 
- 1-2 mins
- 2-5 mins
- 5-10 mins
- 10-30 mins
- < 2 hours
- 2-8 hours
- 8-17 hours
- < 4 days
- \> 4 days