import re
import requests
import json
import os
import time

main_input = input("Please, paste username (without @): ")

current_dir = os.path.dirname(os.path.abspath(__file__))

def get_tiktok_profile_info(nickname):
        folder = os.path.join(current_dir, nickname)
        path = os.path.join(folder, f"{nickname}.html")
        os.makedirs(folder, exist_ok=True)
        with open(path, "w+", encoding="utf-8") as file:
            url = f'https://www.tiktok.com/@{nickname}'
            response = requests.get(url).text
            file.write(response)
        with open(path, "r", encoding="utf-8") as file:
            html_code = file.read()
        description_match = re.search(r'"description":"(.*?)"', html_code)
        if description_match:
            description = description_match.group(1)
        else:
            description = 'No info'
        username_match = re.search(r'"@type":"Person","name":"(.*?)"', html_code)
        if username_match:
            username = username_match.group(1)
        else:
            username = 'No info'
        photo_match = re.search(r'meta data-rh="true" property="og:image" content="(.*?)"', html_code)
        if photo_match:
            photo = photo_match.group(1)
        else:
            photo = 'No info'
        userid = re.search(r'"authorId":"(.*?)"', html_code)
        if userid:
            user_id = userid.group(1)
        else:
            user_id = 'No info'

        fow_count = re.search(r'"followerCount":(\d+)', html_code)
        if fow_count:
            folowers = fow_count.group(1)
        else:
            folowers = 'No info'
        following_co = re.search(r'"followingCount":(\d+)', html_code)

        if following_co:
            follow_count = following_co.group(1)
        else:
            follow_count = "No info"
        hearts = re.search(r'"heart":(\d+)', html_code)
        if hearts:
            likes = hearts.group(1)
        else:
            likes = 'No info'
        a = '"followerCount":{},"followingCount":{},"heart":{},"heartCount":{},"videoCount":(\d+)'.format(folowers, follow_count, likes, likes)
        videos = re.search(r'{}'.format(a), html_code)
        if videos:
            videos_count = videos.group(1)
        else:
            videos_count = "No info"
        return username, description, photo, user_id, folowers, follow_count, likes, videos_count

profile_username, profile_description, photo, user_id, followers, follows_count, likess, videos_coun = get_tiktok_profile_info(main_input)

folder = os.path.join(current_dir, main_input)
print(f"Username: {profile_username}\nBio: {profile_description}\nPhoto: {photo}\nUserId: {user_id}\nFollowers Count: {followers}\nFollows Count: {follows_count}\nHearts (Likes?): {likess}\nVideos Count: {videos_coun}\nHTML User Data Path: {folder}")
choice = input("Select from menu what do you want\n\n1. Save as .json\n2. Get photo profile\n\n")

if choice == '1':
        data = {
            'Username': profile_username,
            'Bio': profile_description,
            'Photo': photo,
            'UserId': user_id,
            'Followers Count': followers,
            'Follows Count': follows_count,
            'Hearts': likess,
            'Videos Count': videos_coun
        }
        folder = os.path.join(current_dir, main_input)
        path = os.path.join(folder, f"data.json")
        os.makedirs(folder, exist_ok=True)
        with open(path, 'w+', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        print(f"Data saved as: {path}\n")
        time.sleep(3)
        exit()
if choice == '2':
        folder = os.path.join(current_dir, main_input)
        path_photo = os.path.join(folder, f"{main_input}.jpg")
        os.makedirs(folder, exist_ok=True)
        with open(path_photo, 'wb') as file:
            response = requests.get(photo)
            file.write(response.content)
        print(f'Photo saved as: {path_photo}\n')
        time.sleep(3)
        exit()