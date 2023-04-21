import pika


def callback(ch, method, properties, body):
    print(f"[x] {body}")


conn_params = pika.ConnectionParameters(host='localhost')
conn = pika.BlockingConnection(conn_params)
channel = conn.channel()
channel.exchange_declare(
    exchange='logs',
    exchange_type='fanout'
)

result = channel.queue_declare(
    queue='',
    exclusive=True      # once the consumer connection is closed, the queue should be deleted.
)
queue_name = result.method.queue
print(f"queue name: {queue_name}")

"""
    we need to tell the exchange to send messages to our queue. 
    That relationship between exchange and a queue is called a binding.
"""
channel.queue_bind(exchange='logs', queue=queue_name)
print(' [*] Waiting for logs. To exit press CTRL+C')

channel.basic_consume(
    queue=queue_name,
    on_message_callback=callback,
    auto_ack=True
)
channel.start_consuming()

