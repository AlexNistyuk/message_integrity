from django.db import models


class Mail(models.Model):
    subject = models.CharField(max_length=200, null=True)
    sent_date = models.DateTimeField(null=True)
    received_date = models.DateTimeField(null=True)
    text = models.TextField(max_length=1000, null=True)
    uid = models.CharField(null=False, max_length=30)
    receiver = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="mails"
    )


def file_directory_path(instance, filename):
    return "{0}/{1}".format(instance.mail.id, filename)


class MailFiles(models.Model):
    mail = models.ForeignKey(
        "mails.Mail", on_delete=models.CASCADE, related_name="files"
    )
    file = models.FileField(upload_to=file_directory_path)
