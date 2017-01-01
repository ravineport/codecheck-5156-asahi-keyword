#!/usr/bin/env python

import urllib.request, urllib.parse
import json
import asyncio
import aiohttp


end_point = "http://54.92.123.84/search?"
api_key = "869388c0968ae503614699f99e09d960f9ad3e12"
params = {
    "q": "",
    "wt": "json",
    "ackey": api_key
}


def generate_url(keyword):
    params["q"] = "Body:" + str(keyword)
    return end_point + urllib.parse.urlencode(params)


async def get_response(keyword, url):
    response = await aiohttp.get(url)
    data = await response.text()
    json_data = json.loads(data)
    return responce2simple_json(keyword, json_data)


def responce2simple_json(keyword, res):
    return {"name": keyword, "count": int(res["response"]["result"]["numFound"])}


def calc_max_numFound(results):
    for result in results:
        print(result)


def print_for_test(ans):
    print("{\"name\":\"" + ans["name"] + "\",\"count\":" + str(ans["count"]) + "}")


def main(argv):
    urls = []

    for keyword in argv:
        url = generate_url(keyword)
        urls.append({'url': url, 'keyword': keyword})

    futures = [get_response(url['keyword'], url['url']) for url in urls]
    loop = asyncio.get_event_loop()
    tasks = loop.run_until_complete(asyncio.wait(futures))[0]
    print_for_test(max(tasks, key=lambda task: int(task.result()["count"])).result())
