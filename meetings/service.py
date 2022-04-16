from math import radians, sin, acos, cos

from PIL import Image
from django.conf import settings
from django.core.mail import send_mass_mail


def set_watermark(
        avatar,
        watermark_path
) -> None:
    watermark = Image.open(watermark_path).convert("RGBA")
    img = Image.open(avatar.file)
    img.paste(watermark, (img.size[0] - watermark.size[0], img.size[1] - watermark.size[1]), watermark)
    image = img.resize((1400, 560), Image.ANTIALIAS)
    image.save('{0}/{1}'.format(settings.MEDIA_ROOT, avatar.name), quality=80)


def send_mails(first_user, second_user) -> None:
    message1 = (
        "Someone liked you", f"{first_user.first_name} liked you. Email's client is {first_user.email}",
        "from@example.com", [second_user.email]
    )
    message2 = (
        "Someone liked you", f"{second_user.first_name} liked you. Email's client is {second_user.email}",
        "from@example.com", [first_user.email]
    )

    send_mass_mail((message1, message2), fail_silently=False)


def avatar_file_name(instance, filename: str) -> str:
    return '/'.join(["avatars", instance.username, filename])


def calculate_distance(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    return 6371 * (
        acos(sin(lat1) * sin(lat2) + cos(lat1) * cos(lat2) * cos(lon1 - lon2))
    )
