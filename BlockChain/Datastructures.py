import time
import json
from threading import Lock
import uuid
import BlockChain.ProofOfWork

mutex = Lock()


def recurseJsonUpdate(target, source):
    ret = {}
    for key, element in source.items():

        if isinstance(element, dict):
            if key in target:
                if isinstance(target[key], dict):
                    ret[key] = recurseJsonUpdate(target[key], source[key])
                else:
                    ret[key] = target[key]
            else:
                ret = target
                # ret[key] = source[key]
        elif isinstance(element, list):
            if key in target:
                if isinstance(target[key], dict):
                    ret[key] = recurseJsonUpdate(target[key], source[key])
                else:
                    ret[key] = element + target[key]
                    target[key] = ret[key]
                    ret[key] = target

            # Combine list
        else:
            ret = target
            # Select target if it exists
    return ret


class Node:
    def __init__(self, data, current_hash, prev_hash):
        self.data = data
        self.current_hash = current_hash
        self.prev_hash = prev_hash
        self.timestamp = int(time.time())
        self.next = None
        self.prev = None


class NotIntact(Exception):
    pass


class ElementContainer(object):
    def __init__(self):
        self.head = None
        self.tail = None
        self.prev_hash = self.genesis()
        self.start_up()

    def start_up(self):
        """
        Will add the data from the json file to the linked list at startup
        """
        try:
            if self.is_empty() is not True:
                with open("data.json", "r")as fp:
                    loaded_json = json.load(fp)
                    for key, element in loaded_json.items():
                        string = element["Validated_string"]
                        di = {key: element}
                        self.add(di, string, key, state=True)
            else:
                pass
        except json.JSONDecodeError as e:
            print(e)

    @staticmethod
    def genesis():
        """
        First part of the chain
        :return:
        """
        return hash("This is the first link in the chain" + str(time.time()))

    def hash_func(self, data, string):
        """
        this function has to be called after self.prev_hash is initialized
        Will hash data
        the hash will be used in the final data set
        will create and return current_hash
        it will also give prev_hash a new value for the next chain
        :param string:
        :param data:
        :return:
        """
        data = str(data) + string
        if self.head is None:
            x = hash(data)
            current_hash = x
            self.prev_hash = x

        else:
            x = hash(data)
            self.prev_hash = x
            current_hash = x
        return current_hash

    def id(self):
        """
        Will create an id for the data
        :return:
        """
        id_ = str(uuid.uuid1())
        current_node = self.head
        while current_node is not None:
            if current_node.data.keys != id_:
                current_node = current_node.next
            else:
                id_ = str(uuid.uuid4())
                current_node = self.head
        return id_

    def add_to_data(self, data, prev_hash, current_hash, string, id_=None):
        """
        Will add current and previous data to the dict that will be put in the chain

        :param string:
        :param id_: If the id already exists
        :param data: Unfinished data
        :param prev_hash: origin hash func
        :param current_hash: origin hash func
        :return: the complete data set
        """
        if id_ is None:
            id_ = self.id()
        new_dict = {
            id_: {"prev_hash": prev_hash,
                  "current_hash": current_hash,
                  "Validated_string": string,
                  "timestamp": int(time.time()),
                  "data": data}}
        return new_dict

    def add(self, data, string, id_=None, state=False):
        """
        Will add data to the linked list
        and add the hash to the hash list
        it will also save the data to a json file for later use

        :param string:
        :param id_:
        :param data:
        :param state:
        :return:
        """
        prev_hash = self.prev_hash
        current_hash = self.hash_func(data, string)

        if state is True:
            data_ = self.add_to_data(data, prev_hash, current_hash, string, id_)
        if state is False:
            data_ = self.add_to_data(data, prev_hash, current_hash, string)

        data = data_
        if not isinstance(data, Node):
            data = Node(data, current_hash, prev_hash)

        if self.head is None:
            self.head = data
            data.next = None
            data.prev = None
            self.tail = data
            if state is False:
                self.save(data_)

        else:
            self.tail.next = data
            data.prev = self.tail
            self.tail = data
            feed = None
            if state is False:
                self.save(data_)
        for a in data_.keys():
            a = a
        return a

    def save(self, data_):
        """
        Will save data to a json file for later use

        :param data_:
        :return:
        """
        mutex.acquire()
        try:
            data = data_

            if self.is_empty() is True:
                with open("data.json", mode="w", encoding="utf-8") as feedsjson:
                    json.dump(data, feedsjson, indent=4)

            else:
                with open("data.json", mode='r', encoding='utf-8') as feedsjson:
                    feeds = json.load(feedsjson)
                    feed = feeds
                    x = recurseJsonUpdate(data, feed)
                    feed.update(x)

                with open("data.json", mode="w", encoding="utf-8") as feedsjson:
                    json.dump(feed, feedsjson, indent=4)

        except json.JSONDecodeError:
            try:
                with open("data.json", mode="w", encoding="utf-8") as feedsjson:
                    json.dump(feeds, feedsjson)
            except json.JSONDecodeError:
                pass

        finally:
            mutex.release()

    @staticmethod
    def is_empty():
        """
        Will check if the json file is empty
        And return True if it is

        :return:
        """
        with open("data.json", mode="r") as f:
            try:
                json.loads(f.read())
                return False
            except json.JSONDecodeError:
                return True

    def get_all(self):
        """
        Will get all of the elements in the linked list
        and return it in a list
        :return:
        """
        result = []
        current_node = self.head
        while current_node is not None:
            result.append(current_node.data)
            current_node = current_node.next
        return result

    def get_by_hash(self, key):
        """
        NOT done
        Will get a element in the linked list with the hash


        :param key:
        :return:

        """
        raise NotImplementedError
        current_node = self.head
        current_hash = hash(key)

        while current_node is not None:
            if current_hash == current_node.hash:
                return current_node.data

            current_node = current_node.next

    def get_all_hashes(self):
        """
        Will get all of the hashes from the the text document
        :return:
        """
        current_node = self.head
        temp_list = []
        while current_node is not None:
            if current_node.current_hash not in temp_list:
                temp_list.append(current_node.current_hash)
            current_node = current_node.next
        return temp_list

    def get_first(self):
        """
        Will get the first element in the linked list
        :return:
        """
        if self.head is not None:
            return self.head.data
        else:
            return None

    def get_by_index(self, index):
        """
        Will get data from the linked list with index
        Will return data
        :param index:
        :return:
        """
        current_index = 0
        current_node = self.head

        while current_node is not None:
            if current_index == index:
                return current_node.data

            current_node = current_node.next
            current_index += 1
        return None

    def get_last(self):
        """
        Will get the last element in the linked list
        will return data

        :return:
        """
        current_node = self.head
        last_node = None
        while current_node is not None:
            last_node = current_node
            current_node = current_node.next
        last = last_node
        return last

    def get_node(self, receipt):
        current_node = self.head
        response = None
        while current_node is not None:
            print(next(iter(current_node.data)), receipt)
            if next(iter(current_node.data)) == receipt:
                response = current_node.data
                break
            current_node = current_node.next
        if response is None:
            response = "The receipt did not exist"
        return response

    def get_hashes(self):
        current_node = self.head
        list_ = []
        while current_node is not None:
            list_.append(str(current_node.current_hash) + " - " + str(current_node.prev_hash))
            current_node = current_node.next
        return list_

    def validate_chain(self):
        print("start")
        current_node = self.head

        while current_node is not None:
            a = current_node.current_hash
            current_node = current_node.next
            if current_node is not None:
                b = current_node.prev_hash
                if a != b:
                    raise NotIntact
        print("Done")

x = ElementContainer()
x.validate_chain()


class Element(ElementContainer):
    def __init__(self):
        super(Element, self).__init__()

    @staticmethod
    def create_data(data):
        """
        Will create data that will be able to be put in the linked list

        Needs data and name if the name already exist the data will join the existing name

        :param data:
        :return:
        """

        timestamp = int(time.time())
        data_list = [data]
        data = {"event": data_list}
        return data

    def add_element(self, data, string):
        """
        Will call the Add function from the ElementContainer
        It will also call the create_data function

        :param data:
        :param name:
        :return:
        """

        data = self.create_data(data)
        x = self.add(data, string)
        return x
