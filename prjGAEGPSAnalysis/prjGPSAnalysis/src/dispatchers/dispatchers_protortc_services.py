'''
Created on Nov 12, 2014

@author: alantai
'''
from protorpc import messages, remote
from protorpc.wsgi import service

class MessageRequest(messages.Message):
    my_message = messages.StringField(1, required = True)
    
class MessageResponse(messages.Message):
    my_response = messages.StringField(1, required = True)
    
class MessageService(remote.Service):
    @remote.method(MessageRequest, MessageResponse)
    def handle_message(self, request):
        return MessageResponse( my_message = "The message is: {my_message}".format("my_message", request.my_message))
    
app = service.service_mappings([('/protortc/message_service/test', MessageService)])