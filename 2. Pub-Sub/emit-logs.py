import pika
import sys

conn_params = pika.ConnectionParameters(host='localhost')
conn = pika.BlockingConnection(conn_params)

channel = conn.channel()
channel.exchange_declare(exchange='logs', exchange_type='fanout')

"""
    The default exchange
    In previous parts of the tutorial we knew nothing about exchanges, 
    but still were able to send messages to queues. 
    That was possible because we were using a default exchange, 
    which we identify by the empty string ("").
    
    Recall how we published a message before:
    
    channel.basic_publish(exchange='',
                          routing_key='hello',
                          body=message)
    The exchange parameter is the name of the exchange. 
    The empty string denotes the default or nameless 
    exchange: messages are routed to the queue with the name 
    specified by routing_key, if it exists.
"""

message = " ".join(sys.argv[1:]) or "Info: hello world"
channel.basic_publish(
    exchange='logs',
    routing_key='',
    body=message.encode('utf-8')
)
print(f"Sent: {message}")

conn.close()
