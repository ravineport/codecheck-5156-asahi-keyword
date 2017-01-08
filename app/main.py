#!/usr/bin/env python

import urllib.request, urllib.parse
import json
import asyncio
import aiohttp


end_point = "http://54.92.123.84/search?"
api_key = "869388c0968ae503614699f99e09d960f9ad3e12"


def generate_url(keyword):
    '''
    keywordを含む記事を検索するAPIを生成
    '''
    params = {
        'q': 'Body:' + str(keyword),
        'wt': 'json',
        'ackey': api_key
    }
    return end_point + urllib.parse.urlencode(params)


async def get_response(keyword, url):
    '''
    keywordとそれに対応するAPIのURLを叩いて結果をいい感じのJSONにする
    '''
    response = await aiohttp.get(url)
    data = await response.text()
    json_data = json.loads(data)
    return responce2simple_json(keyword, json_data)


def responce2simple_json(keyword, res):
    '''
    返ってきたJSONから必要な部分だけを抽出
    '''
    return {"name": keyword, "count": int(res["response"]["result"]["numFound"])}


def calc_max_numFound(tasks):
    '''
    すべての結果(Taskのset)からnumFoundが最大のものをdictとして返す
    '''
    return max(tasks, key=lambda task: int(task.result()["count"])).result()


def print_for_test(ans):
    '''
    ans(Dict型)をテストで求められる形式に変換
    '''
    print("{\"name\":\"" + ans["name"] + "\",\"count\":" + str(ans["count"]) + "}")


def main(argv):
    urls = []

    for keyword in argv:
        url = generate_url(keyword)
        urls.append({'url': url, 'keyword': keyword})

    futures = [get_response(url['keyword'], url['url']) for url in urls]
    loop = asyncio.get_event_loop()
    tasks = loop.run_until_complete(asyncio.wait(futures))[0]
    print_for_test(calc_max_numFound(tasks))
