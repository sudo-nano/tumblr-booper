import sys
import requests 
import json
from time import sleep

'''
Instructions: 
1. Paste your cookie into cookie.txt
2. Run the script and provide the name of the blog you want to boop
'''

# Boop requests appear to obtain the X-CSRF token from a previous GET request. 
# They've been observed fetching it from /api/v2/user/counts

def boop_user(user, x_csrf, session):
    if type(user) != str:
        raise TypeError("boop_user provided with non-string.")

    
    r = s.post(
        "https://www.tumblr.com/api/v2/boop",
        headers={
            "Host": "www.tumblr.com",
            "User-Agent": "car explosion with hammers",
            "Accept": "application/json;format=camelcase",
            "Accept-Language": "en-us",
            "Accept-Encoding": "gzip, deflate, br",
            "Authorization": "Bearer aIcXSOoTtqrzR8L8YEIOmBeW94c3FmbSNSWAUbxsny9KKx5VFh",
            "X-Ad-Blocker-Enabled": "0",
            "X-Version": "redpop/3/0//redpop/",
            "X-CSRF": x_csrf,
            "Origin": "https://www.tumblr.com",
            "DNT": "1",
            "Alt-Used": "www.tumblr.com",
            "Connection": "keep-alive",
            "Cookie": cookie,
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "Sec-GPC": "1",
            "TE": "trailers",
        },
        data={"receiver": user,"context":"lmao","type":"abnormal"},
    )

    return r

# Use the session cookie to get the anti cross site request forgery token
def get_x_csrf(cookie, session):
    r = session.get(
        "https://tumblr.com/api/v2/user/counts?unread=true&inbox=true&unread_messages=true&blog_notification_counts=true&", 
        headers={
            "Host": "www.tumblr.com",
            "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:131.0) Gecko/20100101 Firefox/131.0",
            "Accept": "application/json;format=camelcase",
            "Accept-Language": "en-us",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            # May need referer. If it needs referer, use format 
            # https://www.tumblr.com/blog-name-here
            "Referer": "https://www.tumblr.com/the-lucky-coin",
            "X-Ad-Blocker-Enabled": "0",
            "X-Version": "redpop/3/0//redpop/",
            "DNT": "1",
            "Cookie": cookie,
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "Authorization": "Bearer aIcXSOoTtqrzR8L8YEIOmBeW94c3FmbSNSWAUbxsny9KKx5VFh",
            "Connection": "keep-alive",
            "Sec-GPC": "1",
            "Priority": "u=4",
            "TE": "trailers",
        }
    )
    return r

# Initialize session and load cookie from file
cookie = open("cookie.txt").readline()
s = requests.Session()

x_csrf_req = get_x_csrf(cookie, s)

if x_csrf_req.status_code != 200:
    raise RuntimeError(f"Fetching X-CSRF failed. Status code: {x_csrf_req.status_code}")

else:
    x_csrf = x_csrf_req.headers["X-Csrf"]
    print("Initial X-CSRF fetched.")

# Parse arguments
if len(sys.argv) > 1:
    username = sys.argv[1]

else:
    username = input("Which user should be booped? ")

use_counter = False
if len(sys.argv) > 2:
    if "--counter" in sys.argv:
        use_counter = True

boop_counter = 0
too_many_requests_counter = 0
failure_counter = 0

def print_counter(successes, too_many, fails):
    print()
    print("Boops: " + str(successes))
    print("TMRs: " + str(too_many))
    print("Failures: " + str(fails))

while(failure_counter < 10):
    boop = boop_user(username, x_csrf, s)
    match boop.status_code:
        case 200:
            boop_counter += 1

            if use_counter:
                print_counter(boop_counter, too_many_requests_counter, failure_counter)

            else:
                print("Boop successful!")


        case 400:
            print("Received 400 bad request. Either your request parameters are messed up, or they haven't enabled booping.")
            exit()

        case 401:
            print("Received 401 unauthorized.")
            failure_counter += 1;

        case 404:
            print("Received 404 not found. Boops might be out of season.")
            exit()

        case 429:
            print("Received 429: Too many requests. Delaying.")
            too_many_requests_counter += 1
            sleep(1)

        case _:
            print(f"Uncaught failure. Code: {boop.status_code}")
            failure_counter += 1;

    sleep(0.5)