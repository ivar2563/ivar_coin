from BlockChain.ProofOfWork import is_valid
import pickle


def validate(string_):
    """
    Will validate the proof of work string
    :param string_:
    :return:
    """
    if is_valid(string_):
        if check_if_empty() is False:
            with open('proof_of_work_list.txt', 'rb') as fp:
                list_ = pickle.load(fp)
                print(list_)
        if check_if_empty() is True:
            list_ = []
        if string_ not in list_:
            list_.append(string_)
            with open("proof_of_work_list.txt", "wb") as fp:
                pickle.dump(list_, fp)
            print(True)
            return True
        else:
            print(False)
            return False
    else:
        print(False)
        return False


def check_if_empty():
    """
    Will check if the pickle list is empty
    :return:
    """
    try:
        with open('proof_of_work_list.txt', 'rb') as fp:
            list_ = pickle.load(fp)
        return False
    except EOFError:
        return True
