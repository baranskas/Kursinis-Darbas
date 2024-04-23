import unittest
from src import game as game_module

class TestGame(unittest.TestCase):
    def test_removal_of_heart(self):
        game_module.Restaurant().remove_heart()
        self.assertEqual(game_module.Restaurant().hearts, 2, "The removal of hearts is wrong.")

    def test_VIPcustomer_point_add(self):
        game_module.Restaurant().points = 0
        game_module.Restaurant().add_points(game_module.VIPCustomer().points)
        self.assertEqual(game_module.Restaurant().points, 200, "The points of VIPCustomer are added incorrectly.")

    def test_RegularCustomer_point_add(self):
        game_module.Restaurant().points = 0
        game_module.Restaurant().add_points(game_module.RegularCustomer().points)
        self.assertEqual(game_module.Restaurant().points, 100, "The points of RegularCustomer are added incorrectly.")

if __name__ == '__main__':
    unittest.main()