from concurrent import futures

import grpc
import time

import proto.chat_pb2 as chat
import proto.chat_pb2_grpc as rpc
import logging as log

log.basicConfig(filename='./logs/app.log', format='%(asctime)s - %(message)s', level=log.INFO)

class ChatServer(rpc.ChatServerServicer):

    def __init__(self):
        self.chats = []

    def ChatStream(self, request_iterator, context):
        lastindex = 0
        # each client has a loop
        while True:
            while len(self.chats) > lastindex:
                n = self.chats[lastindex]
                lastindex += 1
                yield n

    def SendNote(self, request: chat.Note, context):
        print("[{}] {}".format(request.name, request.message))
        log.info("{}".format(request.message))
        
        self.chats.append(request)
        return chat.Empty()


if __name__ == '__main__':
    port = 11912
    # 10 clients can connect to server at the same time.
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    rpc.add_ChatServerServicer_to_server(ChatServer(), server)
    
    print('Starting server. Listening...')
    server.add_insecure_port('[::]:' + str(port))
    server.start()
    while True:
        pass