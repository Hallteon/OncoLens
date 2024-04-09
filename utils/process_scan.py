import io

import numpy as np
from PIL import Image
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from ultralytics import YOLO


class ScanAIProcessor:
    def __init__(self, id, scan):
        self.id = id
        self.scan = scan

    def detect_tumor(self):
        scan_image = Image.open(self.scan)
        model = YOLO('tumor_detector.pt')
        results = model(scan_image)[0]

        im_bgr = results.plot()
        im_rgb = Image.fromarray(im_bgr[..., ::-1])

        image_io = io.BytesIO()
        im_rgb.save(image_io, format='PNG')

        image_content = ContentFile(image_io.getvalue())
        processed_image_name = f'predicted_{self.id}.png'
        processed_image = InMemoryUploadedFile(
            file=image_content,
            field_name='Image',
            name=processed_image_name,
            content_type='image/png',
            size=image_io.tell(),
            charset=None
        )

        return processed_image

    def classify_tumor(self):
        scan_image = Image.open(self.scan)
<<<<<<< HEAD
        model = YOLO('tumor_classifier3.pt')
=======
        model = YOLO('tumor_classifier.pt')
>>>>>>> 12de791440e059ac6fefbeffd0d2e1aa7ee81359
        results = model(scan_image)
        classes = results[0].names
        probs = results[0].probs.numpy()

        return classes[probs.top1]
