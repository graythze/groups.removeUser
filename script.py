import requests
import time
import sys
import traceback

community_id = 000
vk_token = "token"


def timer():
    time.sleep(0.4)


def check_subs(data):
    try:
        max_ids = ''
        x = 0
        for i in range(0, len(data)-1):
            if len(data) <= 0:
                break
            else:
                max_ids += str(data[x]) + ','
                x += 1
        print(max_ids)

        sub = requests.post("https://api.vk.com/method/users.get", data={'user_ids':str(max_ids), 'v':'5.22', 'access_token':vk_token}).json()["response"]
        print(sub)

        i = 0
        while True:
            if sub[i]["first_name"] == "DELETED" or "deactivated" in sub[i]:
                remove_request = requests.get(
                            "https://api.vk.com/method/" + "groups.removeUser" + "?group_id=" + str(
                                community_id) + "&user_id=" + str(sub[i]["id"]) + "&v=5.122" + "&access_token=" + str(vk_token))
                print(remove_request.json())
                timer()
            else:
                print("Page #" + str(sub[i]["id"]), "is alive")
            i += 1
    except:
        traceback.print_exc()


offset = 0

while True:
    request = requests.get("https://api.vk.com/method/" + "groups.getMembers" + "?group_id=" + str(
            community_id) + "?sort=id_asc" + "?&offset=" + str(offset) + "&count=1000" + "&v=5.122" + "&access_token=" + str(vk_token))
    if len(request.json()["response"]["items"]) <= 0:
        break
    check_subs(request.json()["response"]["items"])
    timer()
    offset += 1000
