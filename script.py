import requests
import time
import sys
import traceback

community_id = 000
vk_token = "token"
removed = 0
checked = 0


def timer():
    time.sleep(0.4)


def counter():
    print('Removed: ' + str(removed) + ' Checked: ' + str(checked))


def check_subs(data):
    global checked, removed
    try:
        max_ids = ''
        for i in range(0, len(data)):
            max_ids += str(data[i]) + ','
        print(max_ids)
        sub = requests.post("https://api.vk.com/method/users.get",
                            data={'user_ids': str(max_ids),
                                  'v': '5.124',
                                  'access_token': vk_token}).json()["response"]
        print(sub)

        i = 0
        while i <= len(data)-1:
            print(i)
            if "first_name" in sub[i]:
                if sub[i]["first_name"] == "DELETED":
                    remove_request = requests.get(
                        "https://api.vk.com/method/" + "groups.removeUser" + "?group_id=" + str(
                            community_id) + "&user_id=" + str(sub[i]["id"]) + "&v=5.124" + "&access_token=" + str(
                            vk_token))
                    print('DELETED: ' + str(remove_request.json()))
                    i += 1
                    removed += 1
                    checked += 1
                    timer()
                    continue
            if "deactivated" in sub[i]:
                if sub[i]["deactivated"] == "banned":
                    remove_request = requests.get(
                        "https://api.vk.com/method/" + "groups.removeUser" + "?group_id=" + str(
                            community_id) + "&user_id=" + str(sub[i]["id"]) + "&v=5.124" + "&access_token=" + str(
                            vk_token))
                    print('BANNED: ' + str(remove_request.json()))
                    i += 1
                    removed += 1
                    checked += 1
                    timer()
                    continue
            print("Page #" + str(sub[i]["id"]), "is alive")
            i += 1
            checked += 1
    except:
        traceback.print_exc()


offset = 0

while True:
    request = requests.post("https://api.vk.com/method/groups.getMembers",
                            data={'group_id': str(community_id),
                                  'sort': 'id_asc',
                                  'offset': str(offset),
                                  'count': '900',
                                  'v':'5.124',
                                  'access_token': str(vk_token)})
    if len(request.json()["response"]["items"]) <= 0:
        break
    check_subs(request.json()["response"]["items"])
    timer()
    offset += 900

counter()
