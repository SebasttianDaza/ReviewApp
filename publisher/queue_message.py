from ReviewApp.queue_client import QueueMessageService


class QueueMessagePublisher(QueueMessageService):
    def __init__(self, queue_name="publisher"):
        super().__init__(queue_name)