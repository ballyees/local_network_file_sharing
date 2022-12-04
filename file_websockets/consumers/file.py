import json
from datetime import datetime as dt
from channels.generic.websocket import AsyncWebsocketConsumer
from os import remove as os_remove, path as os_path
from pathlib import Path


class FileContent(list):
    def iter_content(self):
        for chunk in self:
            yield chunk

class ReceiveFileConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.session = self.scope['url_route']['kwargs']['session']
        await self.accept()
        self.session_data = FileContent()
        self.done = False
        
    async def disconnect(self, code):
        if self.done is False:
            try:
                os_remove(os_path.join(self.dirs, self.path))
            except:
                pass
        return await super().disconnect(code)

    # Receive message from WebSocket
    async def receive(self, text_data=None, bytes_data=None):
        # text data for internal trigger
        if bytes_data:
            data = bytes_data
        else:
            data = json.loads(text_data)
        if type(data) == bytes:
            self.session_data.append(data)
        else:
            now = dt.now().isoformat()[:10]
            dirs = os_path.join("file_download", now)
            Path(dirs).mkdir(parents=True, exist_ok=True)
            name = data.get('name')
            self.path = f"{name}"
            self.done = data.get('done', False)
            with open(os_path.join(dirs, self.path), 'wb') as f:
                for d in self.session_data:
                    f.write(d)
            # print('done:', name)
            await self.send(text_data=json.dumps({'done': True, 'filename': name}))
            
class ReceiveFileStreamConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.session = self.scope['url_route']['kwargs']['session']
        await self.accept()
        self.done = False
        now = dt.now().isoformat()[:10]
        self.dirs = os_path.join("file_download", now)
        Path(self.dirs).mkdir(parents=True, exist_ok=True)
        
    async def disconnect(self, code):
        if self.done is False:
            try:
                self.file.close()
            except:
                pass
            try:
                os_remove(os_path.join(self.dirs, self.path))
            except:
                pass
        return await super().disconnect(code)

    # Receive message from WebSocket
    async def receive(self, text_data=None, bytes_data=None):
        # text data for internal trigger
        if bytes_data:
            data = bytes_data
        else:
            data = json.loads(text_data)
        if type(data) == bytes:
            self.file.write(data)
        else:
            if data.get("is_start", False):
                name = data.get('name')
                self.path = f"{name}"
                self.file = open(os_path.join(self.dirs, self.path), 'wb')
            elif data.get("done", False):
                self.file.close()
                self.done = True
                await self.send(text_data=json.dumps({'done': True, 'filename': self.path}))
                