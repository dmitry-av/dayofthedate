import os
from PIL import Image
from io import BytesIO
from django.conf import settings


def add_watermark(image):
    watermark_path = settings.MEDIA_ROOT / 'watermark.png'

    with Image.open(image) as img, Image.open(watermark_path) as watermark:
        watermark = watermark.resize((img.width // 2, img.height // 2))
        watermark_layer = Image.new('RGBA', img.size, (0, 0, 0, 0))
        watermark_layer.paste(
            watermark, (img.width - watermark.width, img.height - watermark.height))
        watermarked_image = Image.alpha_composite(
            img.convert('RGBA'), watermark_layer)
        output_buffer = BytesIO()
        watermarked_image.save(output_buffer, format='PNG')
        output_buffer.seek(0)

    return output_buffer
