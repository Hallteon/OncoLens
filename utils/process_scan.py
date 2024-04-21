import io

import numpy as np
from PIL import Image
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from ultralytics import YOLO


class ScanAIProcessor:
    def __init__(self, id, scan, tumor_type):
        self.id = id
        self.scan = scan
        self.tumor_type = tumor_type

    def detect_tumor(self):
        scan_image = Image.open(self.scan)
        scan_image = scan_image.resize((512, 512))
        model = None
        print(self.tumor_type)

        if self.tumor_type == 'brain':
            model = YOLO('brain_tumor_segmentation.pt')

        elif self.tumor_type == 'lung':
            model = YOLO('lung_tumor_detection.pt')

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
        scan_image = scan_image.resize((512, 512))
        model = None

        if self.tumor_type == 'brain':
            model = YOLO('brain_tumor_classification.pt')

        elif self.tumor_type == 'lung':
            model = YOLO('lung_tumor_classification.pt')

        results = model(scan_image)
        classes = results[0].names
        probs = results[0].probs.numpy()

        return classes[probs.top1]
