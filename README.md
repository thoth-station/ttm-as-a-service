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

## Local Testing

The application is developed using flask. Use the following step to setup local env for Testing.
1. Install and Set python env.
 `pipenv install`
 `pipenv shell`
2. Run the app.
 `python wsgi.py`

## Deployment

This project is managed with kustomize.
Use the following command to deploy on OpenShift cluster.
`kustomize build manifests/overlays/test | oc apply -f -`

### Latest Updates
TTM project is being archived. Latest information on TTM related projects can be found over here:  https://github.com/redhat-et/time-to-merge-tool

If a user wants to self host the TTM tooling instead of have it run through GitHub servers, follow the steps below:
1. Train and host model (detailed steps can be found [here](https://github.com/oindrillac/ocp-ci-analysis/tree/thoth-deployment/notebooks/time-to-merge-prediction))
2. Fork and alter [GitHub app's](https://github.com/thoth-station/ttm-as-a-service) model url located [here](https://github.com/thoth-station/ttm-as-a-service/blob/main/app.py#L40)
3. [Create a Github app](https://github.com/settings/apps/new) and use keys to populate [env](https://github.com/thoth-station/ttm-as-a-service/blob/main/.env.example) vars
4. Host app as desired
