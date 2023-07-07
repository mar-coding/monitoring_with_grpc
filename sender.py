import grpc
import proto.chat_pb2 as chat
import proto.chat_pb2_grpc as rpc

import threading

address = 'localhost'
port = 11912


class Sender:

    def __init__(self, u: str):
        self.username = u
        channel = grpc.insecure_channel(address + ':' + str(port))
        self.conn = rpc.ChatServerStub(channel)
    
    def send_msg(self, msg):
        n = chat.Note()
        n.name = self.username
        n.message = msg
        print("S[{}] {}".format(n.name, n.message))
        self.conn.SendNote(n)