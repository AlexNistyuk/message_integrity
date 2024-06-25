from django.db import models


class Mail(models.Model):
    subject = models.CharField(max_length=100, null=True)
    sent_date = models.DateTimeField()
    received_date = models.DateTimeField()
    text = models.TextField(max_length=1000, null=True)
    uid = models.CharField(null=False, max_length=30)
    receiver = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="mails"
    )

    # TODO add "Поле для хранения списка прикреплённых файлов к письму"
