import collections
import queue



class OrderBook:
    """"
    Class to maintain Order Book of outstanding orders 
    """
    def __init__(self, timestamp = None, operationType = None,  id = None,  price = None):
        self._timestamp = timestamp
        self._operationType = operationType
        self._id = id
        self._price = price

        self._total_orders_count = 0
        self._total_buy_orders_count = 0
        self._total_sell_orders_count = 0
        self._orders_buy_list = collections.defaultdict(float)      # order_price, queue(IDs)
        self._orders_sell_list = collections.defaultdict(float)     # order_price, queue(IDs)


    def checkBuyOrderMatch(self, price):
        """
        Returns if price matches one of the BUY orders
        """
        return price in self._orders_buy_list

    def checkSellOrderMatch(self, price):
        """
        Returns if price matches one of the SELL orders
        """
        return price in self._orders_sell_list

    def addBuyOrder(self, order_price, order_id):
        """
        Add matching order to BUY orders list
        """
        if(self.checkBuyOrderMatch(order_price)):
            self._orders_buy_list[order_price].put(order_id)
        else:
            self._orders_buy_list[order_price] = queue.Queue()
            self._orders_buy_list[order_price].put(order_id)
        

    def removeBuyOrder(self, order_price):
        """
        Remove matching order from BUY orders list
        """
        order_id = self._orders_buy_list[order_price].get()

        if (self._orders_buy_list[order_price].qsize() == 0):
            self._orders_buy_list.pop(order_price)


    def addSellOrder(self, order_price, order_id):
        """
        Add matching order to SELL orders list
        """
        if(self.checkSellOrderMatch(order_price)):
            self._orders_sell_list[order_price].put(order_id)
        else:
            self._orders_sell_list[order_price] = queue.Queue()
            self._orders_sell_list[order_price].put(order_id)


    def removeSellOrder(self, order_price):
        """
        Remove matching order from SELL orders list
        """
        order_id = self._orders_sell_list[order_price].get()

        if (self._orders_sell_list[order_price].qsize() == 0):
            self._orders_sell_list.pop(order_price)


    def insertOrder(self, order_timestamp, order_operation, order_id, order_price):
        """
        Insert new order into Order Book 
        """
        order = OrderBook(order_timestamp, order_operation, order_id, order_price)

        if(order.operation == 'B'):
            if(self.checkSellOrderMatch(order.price)):
                self.removeSellOrder(order.price)
            else:
                self.addBuyOrder(order.price,order.id)

            self.updateTotalBuyOrdersCount()
            self.updateTotalOrdersCount()

        elif(order.operation == 'S'):
            if(self.checkBuyOrderMatch(order.price)):
                self.removeBuyOrder(order.price)
            else:
                self.addSellOrder(order.price,order.id)

            self.updateTotalSellOrdersCount()
            self.updateTotalOrdersCount()
            
        else:
            raise ValueError("Invalid operation type!")

	
    def updateTotalOrdersCount(self):
        """
        Update total orders count
        """
        self._total_orders_count += 1

    def getTotalOrdersCount(self):
        """
        Returns total orders count
        """
        return self._total_orders_count

    def updateTotalBuyOrdersCount(self):
        """
        Update total orders count
        """
        self._total_buy_orders_count += 1

    def getTotalBuyOrdersCount(self):
        """
        Returns total BUY orders count
        """
        return self._total_sell_orders_count

    def updateTotalSellOrdersCount(self):
        """
        Update total orders count
        """
        self._total_sell_orders_count += 1

    def getTotalSellOrdersCount(self):
        """
        Returns total SELL orders count
        """
        return self._total_buy_orders_count

    def getOutstandingBuyOrdersCount(self):
        """
        Return outstanding BUY orders count
        """
        return len(self._orders_buy_list)

    def getOutstandingSellOrdersCount(self):
        """
        Return outstanding SELL orders count
        """
        return len(self._orders_sell_list)

    @property
    def timeStamp(self):
        """
        Returns order's timestamp
        """
        return self._timestamp
	
    @property
    def price(self):
        """
        Returns order's price
        """
        return self._price
	
    @property
    def id(self): 
        """
        Returns order's ID
        """
        return self._id
	
    @property
    def operation(self):
        """
        Returns order's operation type
        """
        return self._operationType


    def processOrder(self, order):
        """
        Process new orders
        """
        order = order.split()
        if(len(order) != 4):
            raise ValueError('Invalid order paramters count!')
        elif (float(order[3]) <= 0):
            raise ValueError('Invalid order price!')
        else:
            self.insertOrder(float(order[0]), order[1], float(order[2]), float(order[3]))
    
