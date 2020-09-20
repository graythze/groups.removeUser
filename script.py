import requests
import time
import sys
import json

community_id = 000
vk_token = "token"


def timer():
    time.sleep(0.4)


def get_subs():
    first_request = requests.get("https://api.vk.com/method/" + "groups.getMembers" + "?group_id=" + str(
        community_id) + "?sort=id_asc" + "?offset=0" + "?count=1000" + "?&v=5.122" + "&access_token=" + str(
        vk_token))
    if 'error' in first_request.json():
        print("Error in first_request")
        pass
    else:
        print(first_request.json())
        data = first_request.json()["response"]["items"]
        print(data)
        timer()

        offset = 1000
        while len(requests.get("https://api.vk.com/method/" + "groups.getMembers" + "?group_id=" + str(
                community_id) + "?sort=id_asc" + "?&offset=" + str(
            offset) + "&count=1000" + "&v=5.122" + "&access_token=" + str(vk_token)).json()["response"][
                      "items"]) > 0:
            request_api = requests.get("https://api.vk.com/method/" + "groups.getMembers" + "?group_id=" + str(
                community_id) + "?sort=id_asc" + "?&offset=" + str(
                offset) + "&count=1000" + "&v=5.122" + "&access_token=" + str(vk_token)).json()["response"]["items"]
            print(request_api)
            data += request_api
            offset += 1000
            timer()

        return data


subs_dict = get_subs()


def check_subs(data):
    for i in data:
        sub = requests.get(
            "https://api.vk.com/method/" + "users.get" + "?user_ids=" + str(i) + "&v=5.122" + "&access_token=" + str(vk_token))
        timer()
        try:
            if sub.json()["response"][0]["first_name"] == "DELETED" or "deactivated" in sub.json()["response"][0]:
                remove_request = requests.get("https://api.vk.com/method/" + "groups.removeUser" + "?group_id=" + str(community_id) + "&user_id=" + str(i) + "&v=5.122" + "&access_token=" + str(vk_token))
                print(remove_request.json())
                timer()
            else:
                print("Page #" + str(i), "is alive")
                timer()
        except:
            pass


check_subs(subs_dict)