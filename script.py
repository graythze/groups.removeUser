import requests
import time

community_id = 000
vk_token = "token"
whitelist = [0]

v = '5.124'
removed = 0
checked = 0
removed_pages = {}


def timer():
    time.sleep(0.36)  # set this value between 3.6 and 4


def show_removed_pages():
    if len(removed_pages) > 0:
        print('These pages were removed from community cause of: ')
        for id, reason in removed_pages.items():
            print('vk.com/id' + str(id) + " " + reason)
    else:
        print('<Empty>')


def check_subs(data):
    global checked, removed
    max_ids = ''
    for i in range(0, len(data)):
        max_ids += str(data[i]) + ','
    print(max_ids)
    sub = requests.post("https://api.vk.com/method/users.get",
                        data={'user_ids': max_ids,
                              'v': v,
                              'access_token': vk_token}).json()["response"]
    print(len(sub))

    for k in sub:
        if k["first_name"] == "DELETED":
            remove_request = requests.post("https://api.vk.com/method/groups.removeUser", data={
                'group_id': community_id,
                'user_id': str(k["id"]),
                'v': v,
                'access_token': vk_token}).json()
            print('DELETED PAGE: ' + str(remove_request))
            removed_pages[k["id"]] = "is completely deleted"
            removed += 1
            checked += 1
            timer()
        if "deactivated" in k:
            if k["deactivated"] == "banned":
                if k["id"] in whitelist:
                    print("ID " + k["id"] + "is whitelisted")
                    checked += 1
                    timer()
                else:
                    remove_request = requests.post("https://api.vk.com/method/groups.removeUser", data={
                        'group_id': str(community_id),
                        'user_id': str(k["id"]),
                        'v': v,
                        'access_token': vk_token}).json()
                    print('BANNED PAGE: ' + str(remove_request))
                    removed_pages[k["id"]] = "is banned"
                    removed += 1
                    checked += 1
                    timer()
        else:
            print("Page #" + str(k["id"]), "is alive")
            checked += 1


offset = 0

while True:
    request = requests.post("https://api.vk.com/method/groups.getMembers",
                            data={'group_id': str(community_id),
                                  'offset': str(offset),
                                  'count': '1000',
                                  'v': v,
                                  'access_token': vk_token}).json()
    print(request)
    if "response" in request:
        if len(request["response"]["items"]) > 0:
            check_subs(request["response"]["items"])
            offset += 1000
        else:
            break

show_removed_pages()
