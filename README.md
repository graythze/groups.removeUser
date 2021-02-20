# 🗑️ groups.removeUser
A python script which deletes blocked or deleted members from community

### ✅ Checklist to do before deleting
*   Your community has **not more than 1M subscribers**. Deleting for big communities may cause errors because of VK API restriction (run this script for two or more times after 24 hours for full deletion)
*   Members who have **"DELETED" in name** or **"banned" in 'deactivated' line will be removed from community**
*   Your role in community is **moderator and above**.

### 🛠 Setup
You need to set variables in settings.py:
*   `community_id` is ID (without `-`) of community.
*   `vk_token` is VK API [Implicit Flow][0] access_token.
*   If you have pages that **should not be deleted**, add page ID in `whitelist` dictionary.


### 🔌 Run script
*   Set required variables
*   Type `python script.py` to launch.


[0]: https://vk.com/dev/implicit_flow_user?f=3.%20Receiving%20access_token "Implicit Flow for User Access Token"
