
import unittest
from unittest.mock import MagicMock
from limit_order_agent import LimitOrderAgent

class TestLimitOrderAgent(unittest.TestCase):
    def setUp(self):
        self.mock_execution_client = MagicMock()
        self.agent = LimitOrderAgent(self.mock_execution_client)

    def test_basic_limit_order(self):
        self.agent.price_threshold = 100  
        self.agent.price_tick('IBM', 99) 
        self.mock_execution_client.execute_order.assert_called_once_with('IBM', 1000, 'BUY')

    def test_add_order(self):
        self.agent.add_order(buy_or_sell=True, product_id='AAPL', amount=500, limit=150)
        self.assertEqual(len(self.agent.orders), 1)
        self.assertEqual(self.agent.orders[0], {
            'product_id': 'AAPL',
            'amount': 500,
            'limit': 150,
            'order_type': 'BUY'
        })

    def test_price_tick_for_added_order(self):
        self.agent.add_order(buy_or_sell=True, product_id='AAPL', amount=500, limit=150)
        self.agent.price_tick('AAPL', 149) 
        self.mock_execution_client.execute_order.assert_called_once_with('AAPL', 500, 'BUY')

    def test_price_tick_for_sell_order(self):
        self.agent.add_order(buy_or_sell=False, product_id='AAPL', amount=300, limit=160)
        self.agent.price_tick('AAPL', 161)  
        self.mock_execution_client.execute_order.assert_called_once_with('AAPL', 300, 'SELL')





if __name__ == '__main__':
    unittest.main()
