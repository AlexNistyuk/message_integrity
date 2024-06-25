import json

from application.use_cases.mails.mails import MailUseCase
from application.use_cases.users.users import UserUseCase
from channels.generic.websocket import AsyncWebsocketConsumer
from django.shortcuts import render
from rest_framework.views import APIView


class MailAPIView(APIView):
    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk")

        return render(request, "mails.html", {"pk": pk})


class MailWebsocket(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def receive(self, text_data: str):
        text_data_json = json.loads(text_data)
        user_id = text_data_json["user_id"]

        user_use_case = UserUseCase()
        mail_use_case = MailUseCase(user_use_case, self.send)

        await mail_use_case.check_and_upload_mails(user_id)

    async def disconnect(self, close_code):
        pass
