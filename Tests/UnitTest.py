import unittest
from IvarCoin import BlockChain

x = BlockChain.Element()

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

    def test_add_and_check(self):
        data = "sos"
        name = "Msg"
        xp = x.add_element(data, name)
        x2 = x.get_last()
        self.assertAlmostEqual(xp, x2)


if __name__ == "__main__":
    unittest.main()
