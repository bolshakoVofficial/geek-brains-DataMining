import time
import vk
from vk.exceptions import VkAPIError
from pymongo import MongoClient


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


def get_user_info(user_id: int):
    """
    get user dict(id, name) by id
    handling 'too many requests' API error by sleeping some time

    :param user_id: int type user id
    :return: dict with user_id and user_name OR empty list if access denied or some error
    """
    while True:
        try:
            user_info = api.users.get(user_ids=user_id, v='5.103')[0]
            name = user_info["first_name"] + " " + user_info["last_name"]
            return {
                "id": user_id,
                "name": name
            }

        except VkAPIError as e:
            if e.code == 6:
                time.sleep(0.2)
            else:
                return []
        except:
            return []


def find_chain(source, target):
    """
    function moves in two directions: from two edge points (source and target)
    to some central point in chain (common friend of both persons)

    :param source: int type user id
    :param target: int type user id
    :return: list of dicts(ids, names)
    """
    start = time.time()
    sample_time = time.time()
    nodes_start = []
    nodes_target = []
    processed_users = []
    common_friends = []

    # initial list of friends (depth = 1)
    # new friends of friends will be continuously appended to it later
    start_list = get_friends(source)
    target_list = get_friends(target)

    # saving all nodes as dict(parent, child)
    for friend in start_list:
        nodes_start.append({source: friend})

    for friend in target_list:
        nodes_target.append({target: friend})

    while True:
        compare_start = time.time()

        # first of all, check if the left-sided user's list of friends
        # has common ids with right-sided user's list of friends
        intersection = list(set(start_list).intersection(target_list))
        for person in intersection:
            if person not in common_friends:
                common_friends.append(person)

        # if so, let this list of common friends fill up with some other common friends
        # also this is the end condition of infinite while cycle
        if len(common_friends) > 5:
            chains_between_users = form_chain(common_friends, nodes_start, nodes_target)
            chains_of_names = name_users(chains_between_users)
            return chains_of_names

        compare_end = time.time()
        request_start = time.time()

        # first users to be in the lists are processed and removed from list
        # by concept, these lists are similar to LIFO queues
        try:
            friend_start = start_list[0]
            friend_target = target_list[0]
        except IndexError as e:
            print()
            print("User has no friends! Error:", e)
            return None

        # if user has already been processed and his friends are on the list
        # then remove his id from list of users-to-process
        if friend_start not in processed_users:
            friends_start = get_friends(friend_start)
            start_list.extend(friends_start)
            processed_users.append(friend_start)
            start_list.remove(friend_start)

            # add new possible nodes of chain
            for friend in friends_start:
                nodes_start.append({friend_start: friend})
        else:
            start_list.remove(friend_start)

        # same with users from another side of chain
        if friend_target not in processed_users:
            friends_target = get_friends(friend_target)
            target_list.extend(friends_target)
            processed_users.append(friend_target)
            target_list.remove(friend_target)

            for friend in friends_target:
                nodes_target.append({friend_target: friend})
        else:
            target_list.remove(friend_target)

        # some measurements and info output
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


def form_chain(common_friends: list, left_nodes: list, right_nodes: list):
    """
    form chain, moving from its center to sides

    :param common_friends: list of ids of users
    :param left_nodes: list of dicts(parent_node, child_node)
    :param right_nodes: list of dicts(parent_node, child_node)
    :return: list of chains of ids
    """
    list_of_chains = []

    for person in common_friends:

        # here person is central node of chain (in most cases)
        left_chain = []
        left_side_person = person
        left_chain.append(left_side_person)

        right_chain = []
        right_side_person = person
        right_chain.append(right_side_person)

        # forming chain from center to left side
        while left_side_person != source_id:
            this_level_node_found = False
            for node in left_nodes:
                for k, v in node.items():
                    if v == left_side_person:
                        left_chain.append(k)
                        left_side_person = k
                        this_level_node_found = True
                        break
                if this_level_node_found:
                    break

        # forming chain from center to right side
        while right_side_person != target_id:
            this_level_node_found = False
            for node in right_nodes:
                for k, v in node.items():
                    if v == right_side_person:
                        right_chain.append(k)
                        right_side_person = k
                        this_level_node_found = True
                        break
                if this_level_node_found:
                    break

        # forming full chain and removing duplicates of central node if exist
        chain = left_chain[::-1] + right_chain
        list_of_chains.append(list(dict.fromkeys(chain)))

    list_of_chains.sort(key=len)

    desired_chains = []
    shortest_length = len(list_of_chains[0])

    # return only the shortest chains
    for chain in list_of_chains:
        if len(chain) <= shortest_length:
            desired_chains.append(chain)

    return desired_chains


def name_users(list_of_chains: list):
    """
    get list of user_names by list of user_ids

    :param list_of_chains: list of chains of ids
    :return: list of chains of names
    """
    named_chains = []

    for chain in list_of_chains:
        named_chain = []
        for person in chain:
            named_chain.append(get_user_info(person))

        named_chains.append(named_chain)
    return named_chains


if __name__ == '__main__':
    total_time = time.time()

    mongo_client = MongoClient()
    database = mongo_client["gb_data_mining_course_project"]
    collection = database["vk_handshake"]

    source_id = 122483091
    target_id = 125254232

    # specify these parameters by your credentials
    app_id = '___'
    vk_login = '___'
    vk_pass = '___'

    session = vk.AuthSession(app_id=app_id, user_login=vk_login, user_password=vk_pass)
    api = vk.API(session)

    chains_found = find_chain(source_id, target_id)

    if chains_found:
        for chain in chains_found:
            chain_of_ids = []
            chain_of_names = []
            chain_of_urls = []

            # printing chains found
            for person in chain[:-1]:
                print(f"{person['name']} -> ", end='')
            print(chain[-1]['name'])
            print(f"Chain length: {len(chain) - 1}")

            # preparing some data for storage in db
            for person in chain:
                chain_of_ids.append(person["id"])
                chain_of_names.append(person["name"])
                chain_of_urls.append(f"https://vk.com/id{person['id']}")

            # final structure
            document = {
                "source_id": source_id,
                "source_username": get_user_info(source_id)["name"],
                "source_url": f"https://vk.com/id{source_id}",
                "target_id": target_id,
                "target_username": get_user_info(target_id)["name"],
                "target_url": f"https://vk.com/id{target_id}",
                "chain_of_ids": chain_of_ids,
                "chain_of_names": chain_of_names,
                "chain_of_urls": chain_of_urls,
            }
            collection.insert_one(document)

        print("Total time: ", time.time() - total_time)
