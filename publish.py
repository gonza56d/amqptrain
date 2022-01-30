
from dataclasses import asdict, dataclass
import json
import uuid

import pika


connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.exchange_declare(
    exchange='order',
    exchange_type='direct'
)


@dataclass
class Order:
    id: str
    user_email: str
    product: str
    quantity: int


order = Order(str(uuid.uuid4()), 'john.doe@example.com', 'Leather Jacket', 1)

channel.basic_publish(
    exchange='order',
    routing_key='order.notify',
    body=json.dumps({'user_email': order.user_email})
)

print(' [P] Order notification message sent.')

channel.basic_publish(
    exchange='order',
    routing_key='order.report',
    body=json.dumps(asdict(order))
)

print(' [P] Report message sent.')

connection.close()
