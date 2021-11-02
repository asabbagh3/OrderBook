import numpy as np
import collections


class OrderBook:
    """"
    Class to maintain Order Book of outstanding orders 
    """
    def __init__(self, timestamp = 0, operationType = None,  id = 0,  price = 0):
        self._timestamp = timestamp
        self._operationType = operationType
        self._id = id
        self._price = price
        self._maxOrderPrice = 0

        
        self._orderList = collections.defaultdict()             # dict: int, OrderBook
        self._availablePrices = collections.defaultdict(int)    # dict: int,int: price,count
        self._periodsList = []                                  # list pair int,double
        self._availablePricesSet = set()


    def insertOrder(self, order_str):
        """
        Insert new order into Order Book and update the highest available order
        
        order_str:  Order string
        """
        order = OrderBook(float(order_str[0]), order_str[1], float(order_str[2]), float(order_str[3]))
        
        if (len(self._periodsList) == 0 or order.getPrice() > self.getHighestPrice()):
            self._orderList[order.getID()] = order  

            self.updatePeriodList(order.getTimeStamp(), order.getPrice())
            self.updateHighestPrice(order.getPrice())
		
        else:
            self._orderList[order.getID()] = order  
		
        self._availablePrices[order.getPrice()] += 1
        self._availablePricesSet.add(order.getPrice())

    def eraseOrder(self, timestamp, id):
        """
        Erase order from Order Book and find the next highest oreder value
        
        timestamp:   Order timestamp
        id           Order's ID
        """
        
        LAST_ORDER = -1
        
        if(id not in self._orderList ):
            raise ValueError('Order Not Found!')

		# check value is the current max AND max price not availabe in different order
        if (self._orderList[id].getPrice() == self.getHighestPrice() and self._availablePrices[self._orderList[id].getPrice()] == 1):
            if (self.getOrdersCount() > 1):
                self._availablePricesSet.remove(self.getHighestPrice())
                new_max_value = max(self._availablePricesSet)
                self.updateHighestPrice(new_max_value)

                self.updatePeriodList(timestamp, self.getHighestPrice())
			
            else: 
                self.updatePeriodList(timestamp, LAST_ORDER) 
		
		#update current available prices
        if(self._availablePrices[self._orderList[id].getPrice()] == 1):
            self._availablePrices.pop(self._orderList[id].getPrice())
        else:
            self._availablePrices[self._orderList[id].getPrice()] -= 1
        self._orderList.pop(id)
	

    def getTimeWeightedAverage(self):
        """
        Returns Time weight average
        """
        time_period = 0
        sum = 0
        LAST_ORDER = -1
        
        if (len(self._periodsList) == 0):
            raise ValueError('Order list is empty!')
        else:
            for i in range(len(self._periodsList) - 1):
                if (self._periodsList[i][1] == LAST_ORDER):
                    continue    

                sum += (self._periodsList[i + 1][0] - self._periodsList[i][0]) * self._periodsList[i][1]
                time_period += (self._periodsList[i + 1][0] - self._periodsList[i][0])

        return sum / time_period
	

    def updatePeriodList(self, timestamp, price):
        """
        Update Orders period list
        """
        self._periodsList.append((timestamp,price)) 
	
    def getOrdersCount(self):
        """
        Returns current orders count
        """
        return len(self._orderList)

    def getTimeStamp(self):
        """
        Returns order's timestamp
        """
        return self._timestamp
	

    def getPrice(self):
        """
        Returns order's price
        """
        return self._price
	

    def getID(self): 
        """
        Returns order's ID
        """
        return self._id
	

    def getOperation(self):
        """
        Returns order's operation type
        """
        return self._operationType
	

    def getHighestPrice(self): 
        """
        Returns current highest available order price
        """
        return self._maxOrderPrice if self._maxOrderPrice else np.nan
	

    def updateHighestPrice(self, price):
        """
        Update current highest available order price
        """
        self._maxOrderPrice = price


    def processOrder(self, order):
        """
        Process new orders
        """
        order = order.split()
        if(len(order) > 4):
            raise ValueError('Order paramters exceeds limits!')
        if (order[1] == 'I'):
            if(len(order) < 4):
                raise ValueError('Order paramters not sufficiet!')
            self.insertOrder(order)
        elif (order[1]  == 'E'):
            if(len(order) > 3):
                raise ValueError('Order paramters exceeds limits!')
            self.eraseOrder(int(order[0]), int(order[2]))
        else:
            raise ValueError('Wrong order operation!')
	