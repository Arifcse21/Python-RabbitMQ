import pika

conn_params = pika.ConnectionParameters('localhost')
connection = pika.BlockingConnection(conn_params)

channel = connection.channel()
channel.queue_declare(queue='letterbox')

message = "Hello! This is my first message"

channel.basic_publish(exchange='', routing_key='letterbox', body=message)

print(f"{message}")
connection.close()


