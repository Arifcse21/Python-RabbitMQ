import pika


def on_msg_received(ch, method, properties, body):
    print(f"Received new message: {body}")


conn_params = pika.ConnectionParameters('localhost')
connection = pika.BlockingConnection(conn_params)

channel = connection.channel()
channel.queue_declare('letterbox')

channel.basic_consume(queue='letterbox', auto_ack=True, on_message_callback=on_msg_received)

print("Started Consuming...")
channel.start_consuming()

