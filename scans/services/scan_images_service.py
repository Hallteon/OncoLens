from scans.daos import ScanImageDAO, TumorCategoryDAO, TumorStageDAO, TumorTypeDAO


class ScanImageProcessService:
    def __init__(self, user_id: int, scan_image_data: dict):
        self.user_id = user_id
        self.scan_image_data = scan_image_data

    def create_scan_image(self):
        scan = {}
        base_image = self.scan_image_data.get('base_image')
        processed_scan = self.scan_image_data.get('predicted_scan')
        tumor_class = self.scan_image_data.get('tumor_class')
        tumor_type = self.scan_image_data.get('tumor_type')
        scan_category = self.get_category(tumor_class, tumor_type)

        scan['base_image'] = base_image
        scan['processed_image'] = processed_scan
        scan['tumor_category_ai'] = scan_category
        scan_image = ScanImageDAO().create(scan)

        return scan_image

    def get_category(self, category_name: str, tumor_type_name: str):
        category = TumorCategoryDAO().get_by_name(category_name)
        tumor_type = TumorTypeDAO().get_by_name(tumor_type_name)

        if not category:
            new_category = TumorCategoryDAO().create({'name': category_name,
                                                      'tumor_type': tumor_type})

            return new_category
        else:
            return category[0]

