from trading_framework.execution_client import ExecutionClient
from trading_framework.price_listener import PriceListener


class LimitOrderAgent(PriceListener):

    def __init__(self, execution_client: ExecutionClient) -> None:
        """

        :param execution_client: can be used to buy or sell - see ExecutionClient protocol definition
        """
        super().__init__()

        self.execution_client = execution_client
        self.orders = []  # List to store orders

        self.basic_product_id = 'IBM'
        self.basic_amount = 1000
        self.basic_threshold = 100.0



    def on_price_tick(self, product_id: str, price: float):
        # see PriceListener protocol and readme file
        if product_id == self.basic_product_id and price < self.basic_threshold:
            self.execution_client.execute_order(product_id, self.basic_amount, 'BUY')

        # Handle dynamic limit orders
        for order in self.orders:
            if order['product_id'] == product_id:
                if (order['order_type'] == 'BUY' and price <= order['limit']) or \
                   (order['order_type'] == 'SELL' and price >= order['limit']):
                    self.execution_client.execute_order(product_id, order['amount'], order['order_type'])
                    self.orders.remove(order)


    def add_order(self, buy_or_sell: bool, product_id: str, amount: int, limit: float):
        """
        Add a new order to the list of orders to be processed.
        :param buy_or_sell: True for buy, False for sell
        :param product_id: ID of the product to trade
        :param amount: Amount to buy/sell
        :param limit: Price limit for the order
        """
        order_type = 'BUY' if buy_or_sell else 'SELL'
        self.orders.append({
            'product_id': product_id,
            'amount': amount,
            'limit': limit,
            'order_type': order_type
        })
