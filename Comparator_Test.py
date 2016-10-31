import unittest
from Comparator import sequence_alignment

class TestComparator(unittest.TestCase):
    def test_dp(self):
    	# typical test
        cost, match_result = sequence_alignment([2,4,1,2,2,3],[4,1,2,1,4,3], 0.1, 1, 1)
        self.assertEqual(3, cost)
        self.assertSequenceEqual([3,0,0,0,1,2,0], match_result)

        # edge test
        cost, match_result = sequence_alignment([1,2,3,4,5],[1,2,3,4,5], 0.1, 1, 1)
        self.assertEqual(0, cost)
        self.assertSequenceEqual([0,0,0,0,0], match_result)        

        # edge test
        cost, match_result = sequence_alignment([1,2,3,4,5],[6,7,8,9,10], 0.1, 1, 1)
        self.assertEqual(5, cost)
        self.assertSequenceEqual([1,1,1,1,1], match_result)

if __name__ == '__main__':
    unittest.main()