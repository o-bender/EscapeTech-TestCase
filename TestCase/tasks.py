# main/tasks.py

from django.core.mail import send_mail
from ImageUpload.celery import app
from django.dispatch import receiver
from django.db.models import signals
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image
from io import BytesIO
from . import models


@app.task
def save_images(foto_id):
    foto = models.Foto.objects.get(id=foto_id)
    if foto:
        foto.middle = thumbnail_image(foto.foto, 600, 600)
        foto.thumbnail = thumbnail_image(foto.foto, 200, 200)
        foto.save()


def thumbnail_image(image, w, h):
    img = Image.open(image.file)
    buffer = BytesIO()
    img.thumbnail((w, h))
    img.save(fp=buffer, format='JPEG')
    return InMemoryUploadedFile(buffer, None, image.name, 'image/jpeg', buffer.tell, None)


@receiver(signals.post_save, sender=models.Foto)
def save_foto(sender, instance, *args, **kwargs):
    send_mail(
        'Foto was added to %s album' % instance.album,
        '',
        'from@example.com',
        [instance.user.email],
        fail_silently=True,
    )
