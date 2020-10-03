# 🗑️ groups.removeUser
A python script which deletes blocked or deleted members from community

### ✅ Check-list to do before deleting
* Your community has **not more than 1M members**. Deleting members from bigger communities may cause to errors
* Members who have **"DELETED" in name** and **"banned" in deactivated line will be removed from community**
* Your role in community is **moderator and above** 

### 🛠 Setup
You need to set variables in settings.py:
* `community_id` is ID (without `-`) of community.
* `vk_token` is VK API [Implicit Flow][0] access_token.


### 🔌 Run bot
* Type `python script.py` to launch.


[0]: https://vk.com/dev/implicit_flow_user?f=3.%20Receiving%20access_token "Implicit Flow for User Access Token"