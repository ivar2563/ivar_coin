from IvarCoin.ProofOfWork import is_valid
import pickle
import os


def validate_(string_):
    """
    Will validate the proof of work string
    :param string_:
    :return:
    """
    if is_valid(string_):
        if check_if_empty() is False:
            with open(get_path(), 'rb') as fp:
                list_ = pickle.load(fp)

        if check_if_empty() is True:
            list_ = []

        if string_ not in list_:
            list_.append(string_)
            with open(get_path(), "wb") as fp:
                pickle.dump(list_, fp)
            return True
        else:
            return False
    else:
        return False


def check_if_empty():
    """
    Will check if the pickle list is empty
    :return:
    """
    try:
        with open(get_path(), 'rb') as fp:
            list_ = pickle.load(fp)
        return False
    except EOFError:
        return True
    except FileNotFoundError:
        with open(get_path(), "wb") as fp:
            empty_list = []
            pickle.dump(empty_list, fp)
            return True


def get_path():
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, "Data/proof_of_work_list.txt")
    return file_path
