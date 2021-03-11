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


def counter():
    print(str(removed) + ' out of ' + str(checked) + ' were removed')


def show_removed_pages():
    print('These pages were removed from community cause of: ')

    for id, reason in removed_pages.items():
        print(str(id) + " " + str(reason))


def check_subs(data):
    global checked, removed
    max_ids = ''
    for i in range(0, len(data)):
        max_ids += str(data[i]) + ','
    print(max_ids)
    sub = requests.post("https://api.vk.com/method/users.get",
                        data={'user_ids': str(max_ids),
                              'v': v,
                              'access_token': vk_token}).json()["response"]
    print(len(sub))
    i = 0
    while i <= len(data) - 1:
        print(i)
        if sub[i]["first_name"] == "DELETED":
            remove_request = requests.get("https://api.vk.com/method/groups.removeUser" +
                                          "?group_id=" + str(community_id) +
                                          "&user_id=" + str(sub[i]["id"]) +
                                          "&v=" + v +
                                          "&access_token=" + str(vk_token))
            print('DELETED PAGE: ' + str(remove_request.json()))
            removed_pages[sub[i]["id"]] = "is completely deleted"
            i += 1
            removed += 1
            checked += 1
            timer()
            continue
        if "deactivated" in sub[i]:
            if sub[i]["deactivated"] == "banned":
                if sub[i]["id"] in whitelist:
                    print("ID " + sub[i]["id"] + "is whitelisted")
                    checked += 1
                    timer()
                else:
                    remove_request = requests.get("https://api.vk.com/method/groups.removeUser" +
                                                  "?group_id=" + str(community_id) +
                                                  "&user_id=" + str(sub[i]["id"]) +
                                                  "&v=" + v +
                                                  "&access_token=" + str(vk_token))
                    print('BANNED PAGE: ' + str(remove_request.json()))
                    removed_pages[sub[i]["id"]] = "is banned"
                    i += 1
                    removed += 1
                    checked += 1
                    timer()
                    continue
        print("Page #" + str(sub[i]["id"]), "is alive")
        i += 1
        checked += 1


offset = 0

while True:
    request = requests.post("https://api.vk.com/method/groups.getMembers",
                            data={'group_id': str(community_id),
                                  'sort': 'id_asc',
                                  'offset': str(offset),
                                  'count': '900',
                                  'v': v,
                                  'access_token': str(vk_token)})
    if "response" in request.json():
        if len(request.json()["response"]["items"]) > 0:
            check_subs(request.json()["response"]["items"])
            timer()
            offset += 900
        else:
            break
    else:
        break

show_removed_pages()
counter()
