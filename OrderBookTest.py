from OrderBook import OrderBook
import unittest
import numpy as np
import time




class TestOrderBook(unittest.TestCase):
    """
    Unit-tests for the Orber Book functionality
    """
    def test_valid_orders_buy_and_sell_count(self):

        testOrdersNum = 1000000
        testBuyOrdersList = [ str(time.time())+' B '+ str(i) + ' ' + str(i/7.0) for i in range(1, testOrdersNum + 1)]
        testSellOrdersList = [ str(time.time())+' S '+ str(i + testOrdersNum/2) +' '+ str(i/7.0) for i in range(1, testOrdersNum + 1)]

        testOrdersList = testBuyOrdersList + testSellOrdersList
        np.random.shuffle(testOrdersList)
        

        order = OrderBook()
        for i in testOrdersList:
            order.processOrder(i)

        self.assertTrue(order.getTotalBuyOrdersCount() == testOrdersNum)
        self.assertTrue(order.getTotalSellOrdersCount() == testOrdersNum)
        self.assertTrue(order.getTotalOrdersCount() == testOrdersNum*2)

    def test_valid_remaining_buy_and_sell_orders(self):
        testOrdersList =   ['1000 B 100 17.0',
                            '2000 B 101 11.0',
                            '2200 B 102 12.0',
                            '2400 S 103 13.0',
                            '2500 S 104 10.0',
                            '4000 B 105 11.0',
                            '6000 S 106 11.0',
                            '6000 S 107 12.0',
                            '6200 B 109 13.0',
                            '7000 S 110 20.0',
                            ]

        order = OrderBook()
        for i in testOrdersList:
            order.processOrder(i)
        
        self.assertTrue(order.getOutstandingBuyOrdersCount() == 2)
        self.assertTrue(order.getOutstandingSellOrdersCount() == 2)

    def test_valid_order_extra_input(self):
        testOrdersList =   ['1000 B 100 17.0',
                            '2000 S 101 11.0 6'
                            ]
        
        with self.assertRaises(ValueError):
            order = OrderBook()
            for i in testOrdersList:
                order.processOrder(i)

    def test_valid_order_price(self):
        testOrdersList =   ['1000 B 100 aa',
                            '2000 S 101 11.0'
                            ]
        
        with self.assertRaises(ValueError):
            order = OrderBook()
            for i in testOrdersList:
                order.processOrder(i)

    def test_valid_order_operation_type(self):
        testOrdersList =   ['1000 B 100 17.0',
                            '2000 C 101 11.0',
                            '2200 B 102 12.0',
                            '2400 S 103 13.0',
                            '2500 S 104 10.0',
                            ]
        
        with self.assertRaises(ValueError):
            order = OrderBook()
            for i in testOrdersList:
                order.processOrder(i)


if __name__ == "__main__":
    unittest.main()
