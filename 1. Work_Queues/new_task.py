import pika
import sys


conn_params = pika.ConnectionParameters(host='localhost')
connection = pika.BlockingConnection(conn_params)
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)
"""
Message durability
We have learned how to make sure that even if the consumer dies, 
the task isn't lost. But our tasks will still be lost if RabbitMQ server stops.

When RabbitMQ quits or crashes it will forget the queues and messages unless you tell it not to. 
Two things are required to make sure that messages aren't lost: 
we need to mark both the queue and messages as durable.
"""


message = ' '.join(sys.argv[1:]) or "Hello World"

channel.basic_publish(
    exchange='',
    routing_key='task_queue',
    properties=pika.BasicProperties(
        delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
    ),
    body=message.encode('utf-8')
)
"""
    At that point we're sure that the task_queue queue won't be lost even if RabbitMQ restarts. 
    Now we need to mark our messages as persistent - 
    by supplying a delivery_mode property with the value of pika.spec.PERSISTENT_DELIVERY_MODE
"""

"""
    Note on message persistence
    Marking messages as persistent doesn't fully guarantee that a message won't be lost. 
    Although it tells RabbitMQ to save the message to disk, 
    there is still a short time window when RabbitMQ has accepted a message and hasn't saved it yet. 
    Also, RabbitMQ doesn't do fsync(2) for every message -- it may be just saved to 
    cache and not really written to the disk. 
    The persistence guarantees aren't strong, 
    but it's more than enough for our simple task queue. 
    If you need a stronger guarantee then you can use publisher confirms.
"""
print(f"[x] Sent: {message}")

connection.close()
