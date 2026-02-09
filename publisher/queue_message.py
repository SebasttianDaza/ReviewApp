from ReviewApp.queue_client import QueueMessageService


class QueueMessagePublisher(QueueMessageService):
    def __init__(self, queue_name="publisher"):
        super().__init__(queue_name)

    def add_message(self, message):
        import base64
        self.queue_client.send_message(base64.b64encode(message.encode('utf-8')))