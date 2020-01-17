import unittest
from IvarCoin import BlockChain
from IvarCoin import ProofOfWork
import requests
import ast
import json

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

    def test_add_and_validate(self):
        string = proof_of_work.generate(email, bits)
        data = {
            "data": ["car", "bus"],
            "string": string
        }
        x = requests.post("http://127.0.0.1:5000/api/add_node/", json=data)
        response_id = str(x.content)
        response_id = response_id.replace("b", "", 1)
        response_id = response_id.replace("'", "")
        string = {"receipt": response_id}
        response = requests.post("http://127.0.0.1:5000/api/get_node/", json=string)
        a = response.content
        response_data = dict(ast.literal_eval(a.decode('utf-8')))[response_id]
        self.assertAlmostEqual(data["data"], response_data["data"])

    def test_check_validating_string(self):
        string = proof_of_work.generate(email, bits)
        proof = proof_of_work.is_valid(string)
        self.assertTrue(proof)


if __name__ == "__main__":
    unittest.main()
