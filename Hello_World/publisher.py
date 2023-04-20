import pika

conn_params = pika.ConnectionParameters('localhost')
connection = pika.BlockingConnection(conn_params)

channel = connection.channel()
channel.queue_declare(queue='hello')

message = b"Hello! This is my first message"

channel.basic_publish(exchange='', routing_key='hello', body=message)

print(f"{message}")
connection.close()


