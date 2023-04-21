import pika
import time


def callback(ch, method, properties, body):
    print(f"[x] Received: {body}")
    time.sleep(body.count(b'.'))
    print("[x] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)  # proper acknowledgment from the worker
    """
    Forgotten acknowledgment
    It's a common mistake to miss the *basic_ack*. 
    It's an easy error, but the consequences are serious. 
    Messages will be redelivered when your client quits (which may look like random redelivery), 
    but RabbitMQ will eat more and more memory as it won't be able to release any unacked messages.
    """


conn_params = pika.ConnectionParameters(host="localhost")
connection = pika.BlockingConnection(conn_params)
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)
print("[*] Waiting for messages. To exit press CTRL+C")
channel.basic_qos(prefetch_count=1)
"""
    Fair dispatch
    You might have noticed that the dispatching still doesn't work exactly as we want. 
    For example in a situation with two workers, 
    when all odd messages are heavy and even messages are light, 
    one worker will be constantly busy and the other one will do hardly any work. 
    Well, RabbitMQ doesn't know anything about that and will still dispatch messages evenly.
    
    This happens because RabbitMQ just dispatches a message when the message enters the queue. 
    It doesn't look at the number of unacknowledged messages for a consumer. 
    It just blindly dispatches every n-th message to the n-th consumer.
"""

channel.basic_consume(queue='task_queue', on_message_callback=callback)
channel.start_consuming()
