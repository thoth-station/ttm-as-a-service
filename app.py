import asyncio
import os
import aiohttp
from aiohttp import web
import cachetools
from gidgethub import aiohttp as gh_aiohttp
from gidgethub import routing
from gidgethub import sansio
from gidgethub.apps import get_installation_access_token

import ttm_github_pr


GITHUBAPP_ID = os.environ["GITHUBAPP_ID"]
GITHUBAPP_SECRET = os.environ["GITHUBAPP_SECRET"]
GITHUBAPP_KEY = os.environ["GITHUBAPP_KEY"]

router = routing.Router()
cache = cachetools.LRUCache(maxsize=500)
routes = web.RouteTableDef()


@routes.post("/")
async def webhook(request):
    try:
        body = await request.read()
        event = sansio.Event.from_http(request.headers, body, secret=GITHUBAPP_SECRET)
        async with aiohttp.ClientSession() as session:
            gh = gh_aiohttp.GitHubAPI(session, "ttm-as-a-service", cache=cache)
            await asyncio.sleep(1)
            await router.dispatch(event, gh)
        return web.Response(status=200)
    except Exception as ex:
        print(ex)
        return web.Response(status=500)


@router.register("pull_request", action="opened")
async def opened_pr(event, gh, *arg, **kwargs):
    model_url = "http://thoth-github-ttm-ds-ml-workflows-ws.apps.smaug.na.operate-first.cloud/predict"
    pull_request = event.data["pull_request"]
    installation_access_token = await get_installation_access_token(
        gh,
        installation_id=event.data["installation"]["id"],
        app_id=GITHUBAPP_ID,
        private_key=GITHUBAPP_KEY,
    )
    prediction = ttm_github_pr.get_ttm(
        model_url,
        pull_request["head"]["repo"]["id"],
        event.data["number"],
        installation_access_token["token"],
    )
    url = f"/repos/{pull_request['head']['repo']['full_name']}/issues/{event.data['number']}/comments"
    await gh.post(
        url,
        data={
            "body": f"{prediction}",
        },
        oauth_token=installation_access_token["token"],
    )


@router.register("installation", action="created")
async def install_app():
    print("installed")


@router.register("installation", action="deleted")
async def uninstall_app():
    print("uninstalled")


if __name__ == "__main__":
    app = web.Application()
    app.router.add_routes(routes)
    port = os.environ.get("PORT")
    if port is not None:
        port = int(port)
    web.run_app(app, port=port)
