import vk
from vk.exceptions import VkAPIError
import time

source_id = 122483091

# 2
# target_id = 29204850

# 3
target_id = 156776622

# 4
# target_id = 11844704

app_id = '7308564'
vk_login = '+79154179464'
vk_pass = 'mnx4xkue1996pass'
chain = []
processed_users = []


def get_friends(user_id):
    while True:
        try:
            return api.friends.get(user_id=str(user_id), v='5.103')["items"]
        except VkAPIError as e:
            if e.code == 6:
                time.sleep(0.2)
            else:
                return []
        except:
            return []


def find_chain(start_list: list, target_list: list):
    start = time.time()
    sample_time = time.time()

    while True:
        compare_start = time.time()
        friend_start = start_list[0]
        friend_target = target_list[0]
        for user in start_list:
            if user == target_id:
                user_info = api.users.get(user_ids=user, v='5.103')[0]
                name = user_info["first_name"] + " " + user_info["last_name"]
                print(f"Chain found! Target: {name}")
                return

        compare_end = time.time()
        request_start = time.time()

        if friend_start not in processed_users:
            friends = get_friends(friend_start)
            start_list.extend(friends)
            processed_users.append(friend_start)
            start_list.remove(friend_start)

            if not len(processed_users) % 10:
                print(f"Processed {len(processed_users)} users, to be processed: {len(start_list)}")
                request_end = time.time()
                end = time.time() - sample_time
                print(f"Time elapsed: {round((time.time() - start), 3)} sec")
                print(f"Comparing time: {round(compare_end - compare_start, 5)}")
                print(f"Requesting time: {round(request_end - request_start, 5)}")
                print(f"Total time elapsed: {round(end // 60)} min {round(end % 60)} sec")
                print()
                start = time.time()
        else:
            start_list.remove(friend_start)


session = vk.AuthSession(app_id=app_id, user_login=vk_login, user_password=vk_pass)
api = vk.API(session)

start_friends = get_friends(source_id)
target_friends = get_friends(target_id)

find_chain(start_friends, target_friends)
