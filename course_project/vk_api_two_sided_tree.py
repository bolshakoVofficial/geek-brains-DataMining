import vk
from vk.exceptions import VkAPIError
import time
from anytree import Node

source_id = 122483091

# 2
# target_id = 29204850

# 3
# target_id = 156776622

# 4
target_id = 11844704

# target_id = 163834

app_id = '7308564'
vk_login = '+79154179464'
vk_pass = 'mnx4xkue1996pass'
chain = []
processed_users = []


def get_friends(user_id: int):
    """
    get list of friends of user specified by input parameter - id
    handling 'too many requests' API error by sleeping some time

    :param user_id: int type user id
    :return: list of friends OR empty list if access denied or some error
    """
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


def find_chain(source, target):
    start = time.time()
    sample_time = time.time()
    chain_nodes = dict()

    start_list = get_friends(source)
    start_node = Node(source)
    start_depth = 1
    for friend in start_list:
        # chain_nodes[f"start_l{start_depth}_node"] = Node(friend, parent=start_node)
        start_node = Node(friend, Node(source))

    target_list = get_friends(target)
    target_node = Node(target)
    target_depth = 1

    while True:
        compare_start = time.time()

        friend_start = start_list[0]
        friend_target = target_list[0]
        common_friends = list(set(start_list).intersection(target_list))

        if len(common_friends) > 0:
            user_info = api.users.get(user_ids=common_friends[0], v='5.103')[0]
            name = user_info["first_name"] + " " + user_info["last_name"]
            print(f"Chain found! Middle: {name}")
            return

        compare_end = time.time()
        request_start = time.time()

        if friend_start not in processed_users:
            friends_start = get_friends(friend_start)
            start_list.extend(friends_start)
            processed_users.append(friend_start)
            start_list.remove(friend_start)
        else:
            start_list.remove(friend_start)

        if friend_target not in processed_users:
            friends_target = get_friends(friend_target)
            target_list.extend(friends_target)
            processed_users.append(friend_target)
            target_list.remove(friend_target)
        else:
            target_list.remove(friend_target)

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


session = vk.AuthSession(app_id=app_id, user_login=vk_login, user_password=vk_pass)
api = vk.API(session)

find_chain(source_id, target_id)
