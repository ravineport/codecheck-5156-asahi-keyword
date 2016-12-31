#!/usr/bin/env python

import urllib.request, urllib.parse
import json


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


def get_response(url):
    with urllib.request.urlopen(url) as res:
        json_res = json.loads(res.read().decode("utf-8"))
        return json_res


def print_for_test(ans):
    print("{\"name\":\"" + ans["name"] + "\",\"count\":" + str(ans["count"]) + "}")


def main(argv):
    ans_lst = []
    for keyword in argv:
        url = generate_url(keyword)
        # print(url)
        res = get_response(url)
        # print(res)
        ans = {"name":keyword, "count":int(res["response"]["result"]["numFound"])}
        ans_lst.append(ans)
    # print(ans_lst)
    print_for_test(max(ans_lst, key=lambda ans: int(ans["count"])))
