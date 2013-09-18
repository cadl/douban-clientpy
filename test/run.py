import test_shuo
import unittest


def suite():
    suite = unittest.TestSuite()
    suite.addTest(test_shuo.TestApiShuo('test_statuses_not_with_img'))
    suite.addTest(test_shuo.TestApiShuo('test_statuses_with_img'))
    suite.addTest(test_shuo.TestApiShuo('test_statuses_home_timeline'))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
