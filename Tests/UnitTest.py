import unittest
from IvarCoin import BlockChain
from IvarCoin import ProofOfWork
import requests

x = BlockChain.Element()

proof_of_work = ProofOfWork

email = "Unit.test@gmail.com"
bits = 20

print(">>>>>>>>>", x.is_empty(), "<<<<<<<<")


class ListUnitTest(unittest.TestCase):

    def setUp(self) -> None:
        print("Hello from setup")

    def tearDown(self) -> None:
        print("Hello from teardown")

    def test_empty_func2(self):
        xs = x.is_empty()
        self.assertFalse(xs)

    def test_Test(self):
        self.assertEqual(1, 1)

    def test_get_first(self):
        xp = x.get_first()
        print(xp)
        self.assertNotEqual(len(xp), 0)

    def add_and_validate(self):
        string = proof_of_work.generate(email, bits)
        data = {
            "data": ["car", "bus"],
            "string": string
        }
        x = requests.post("http://127.0.0.1:5000/api/add_node/", json=data)
        respons = x.content

        self.assertin(data, )




    def check_validating_string(self):
        pass


if __name__ == "__main__":
    unittest.main()
