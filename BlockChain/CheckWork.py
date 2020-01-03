from BlockChain.ProofOfWork import is_valid
import pickle


def validate(string_):
    print("start")
    if is_valid(string_):
        with open('proof_of_work_list.txt', 'rb') as fp:
            list_ = pickle.load(fp)
        if string_ not in list_:
            with open("proof_of_work_list.txt", "wb") as fp:
                pickle.dump(string_, fp)
            print(True)
            return True
        else:
            print(False)
            return False
    else:
        print(False)
        return False
