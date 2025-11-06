from azure.storage.queue import QueueClient, BinaryBase64EncodePolicy, BinaryBase64DecodePolicy
from ReviewApp.settings import env

class QueueMessageService:
    queue_client = None
    account_url = None
    queue_name = None
    def __init__(self, queue_name="default"):
        self.account_url = env('AZURITE_QUEUE_URL')
        self.queue_name = queue_name
        self.queue_client = QueueClient.from_connection_string(
            env('AZURITE_WEB_STORAGE'),
            queue_name=self.queue_name,
            message_encode_policy=BinaryBase64EncodePolicy(),
            message_decode_policy=BinaryBase64DecodePolicy()
        )
        try:
            self.queue_client.create_queue()
        except:
            print("Failed to create queue or already exists")
            pass



    def add_message(self, message):
        self.queue_client.send_message(message)

    def peek_messages(self, max_messages=100):
        return self.queue_client.peek_messages(max_messages)