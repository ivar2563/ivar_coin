import datetime
import time
import pickle
import json
import unittest
from threading import Lock

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
    def __init__(self, data, hash_):
        self.data = data
        self.hash = hash_
        self.next = None
        self.prev = None


class ElementContainer(object):
    def __init__(self):
        self.head = None
        self.tail = None
        self.prev_hash = None
        self.start_up()

    def start_up(self):
        """Wil clear the old hashes,
        and add the data from the json file to the linked list at startup"""
        try:
            with open("hash.txt", "wb") as rb:
                print("X")
                pickle.dump(None, rb)
            if self.is_empty() is not True:
                with open("data.json", "r")as fp:
                    loaded_json = json.load(fp)
                    for key, element in loaded_json.items():
                        di = {key: element}
                        print(di)
                        self.add(di, key, state=True)
            else:
                pass
        except json.JSONDecodeError as e:
            print(e)

    def new_hash_func(self, data):
        """
        In use
        Will hash the data with the previous hash
        :param data:
        :return: hash_
        """
        if self.head is None:
            hash_ = hash(str(data))
        else:
            current_node = self.head
            last = None
            while current_node is not None:
                last = current_node
                current_node = current_node.next
            previous = last.data
            to_be_hashed = str(previous) + str(data)
            hash_ = hash(to_be_hashed)

        return hash_

    @staticmethod
    def add_hash_to_data(data, name, hash_):
        new_dict = {name: {"prev_hash": hash_, "data": data}}
        print(new_dict)
        return new_dict

    def add(self, data, name, state=False):
        """
        Will add data to the linked list
        and add the hash to the hash list
        it will also save the data to a json file for late use

        :param name:
        :param data:
        :param state:
        :return:
        """
        hash_ = self.new_hash_func(data)
        data_ = self.add_hash_to_data(data, name, hash_)
        data = data_
        hash_list = [hash_]
        if not isinstance(data, Node):
            data = Node(data, hash_)

        if self.head is None:
            self.save_hash(hash_list)
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
            self.save_hash(hash_list)

    def save_hash(self, hash_):
        """
        Will save the hash in a text document for use in the hash function

        :param hash_:
        :return:
        """
        mutex.acquire()
        try:
            if self.head is None:
                with open("hash.txt", "wb") as fp:
                    pickle.dump(hash_, fp)
            else:
                with open("hash.txt", "rb") as rp:
                    list_ = pickle.load(rp)
                with open("hash.txt", "wb") as fp:
                    list_.append(hash_[0])
                    pickle.dump(list_, fp)
        except pickle.PicklingError as e:
            print(e)
        except pickle.UnpicklingError as e:
            print(e)
        finally:
            mutex.release()

    def save(self, data_):
        """
        Will save data to a json file for later use

        :param data_:
        :return:
        """
        mutex.acquire()
        try:
            data = data_
            print("data = ", data)
            if self.is_empty() is True:
                with open("data.json", mode="w", encoding="utf-8") as feedsjson:
                    print(data)
                    print(type(data))
                    json.dump(data, feedsjson, indent=4)

            else:
                with open("data.json", mode='r', encoding='utf-8') as feedsjson:
                    feeds = json.load(feedsjson)
                    feed = feeds
                    print("first feed = ", feed)
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

    @staticmethod
    def get_all_hashes():
        """
        Will get all of the hashes from the the text document
        :return:
        """
        try:
            with open("hash.txt", "rb") as rb:
                hashes = pickle.load(rb)
            return hashes
        except pickle.UnpicklingError as e:
            print(e)

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
        last = last_node.data

        return last


class Element(ElementContainer):
    def __init__(self):
        super(Element, self).__init__()

    @staticmethod
    def create_data(data):
        """
        Will create data that will be able to be put in the linked list

        Needs data and name if the name already exist the data will join the existing name

        :param data:
        :param name:
        :return:
        """

        timestamp = int(time.time())
        data_list = [data]
        data = {"event": data_list, "timestamp": timestamp}
        return data

    def add_element(self, data, name):
        """
        Will call the Add function from the ElementContainer
        It will also call the create_data function

        :param data:
        :param name:
        :return:
        """

        data = self.create_data(data)
        self.add(data, name)
