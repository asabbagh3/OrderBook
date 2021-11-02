from OrderBook import OrderBook
import unittest
import numpy as np




class TestNextNum(unittest.TestCase):
    """
    Unit-tests for the next_num functionality
    """
    def test_valid_returned_value(self):
        testOrdersList = ['1000 I 100 10.0',
                          '2000 I 101 13.0',
                          '2200 I 102 13.0',
                          '2400 E 101',
                          '2500 E 102',
                          '4000 E 100']
        order = OrderBook()
        for i in testOrdersList:
            order.processOrder(i)
        

        return_value = order.getTimeWeightedAverage()
        self.assertTrue(return_value == 10.5)

    def test_valid_returned_value_empty_periods(self):
        testOrdersList = ['1000 I 100 10.0',
                          '2000 I 101 13.0',
                          '2200 I 102 13.0',
                          '2400 E 101',
                          '2500 E 102',
                          '4000 E 100',
                          '6000 I 105 16.0',
                          '6000 I 106 20.0',
                          '6000 E 106',
                          '6200 E 105',
                          ]
        order = OrderBook()
        for i in testOrdersList:
            order.processOrder(i)
        

        return_value = order.getTimeWeightedAverage()
        self.assertTrue(return_value == 10.84375)

    def test_valid_order_extra_input(self):
        testOrdersList = ['1000 I 100 10.0 1',
                          '2000 I 101 13.0',
                          ]
        
        with self.assertRaises(ValueError):
            order = OrderBook()
            for i in testOrdersList:
                order.processOrder(i)

    def test_valid_order_operation_type(self):
        testOrdersList = ['1000 I 100 10.0',
                          '2000 S 101 13.0',
                          ]
        
        with self.assertRaises(ValueError):
            order = OrderBook()
            for i in testOrdersList:
                order.processOrder(i)

    def test_valid_delete_order(self):
        testOrdersList = ['1000 E 100',
                          '2000 I 100 13.0',
                          ]
        
        with self.assertRaises(ValueError):
            order = OrderBook()
            for i in testOrdersList:
                order.processOrder(i)

    def test_valid_order_count(self):
        testOrdersList = ['1000 I 100 10.0',
                          '2000 I 101 13.0',
                          '2200 I 102 13.0',
                          '2400 E 101',
                          '2500 E 102'
                          ]
        order = OrderBook()
        for i in testOrdersList:
            order.processOrder(i)

        return_value = order.getOrdersCount()
        self.assertTrue(return_value == 1)

    def test_valid_highest_order_price(self):
        testOrdersList = ['1000 I 100 10.0',
                          '2000 I 101 13.0',
                          '2200 I 102 13.0',
                          '2400 E 101',
                          '2500 E 102'
                          ]
        order = OrderBook()
        for i in testOrdersList:
            order.processOrder(i)

        return_value = order.getHighestPrice()
        self.assertTrue(return_value == 10.0)

    def test_valid_order_list_empty(self):
        order = OrderBook()

        with self.assertRaises(ValueError):
            return_value = order.getTimeWeightedAverage()

if __name__ == "__main__":
    unittest.main()