from scans.daos import TumorCategoryDAO, TumorStageDAO, ScanRecordDAO
from users.daos import CustomUserDAO


class ScanRecordProcessService:
    def __init__(self, user_id: int, scan_data: dict, scan_id: int = None):
        self.scan_id = scan_id
        self.user_id = user_id
        self.scan_data = scan_data

    def update_scan(self):
        scan = {}
        by_user = CustomUserDAO().get(self.user_id)
        predicted_scan = self.scan_data.get('predicted_scan')
        tumor_class = self.scan_data.get('tumor_class')
        cat_index = 0
        stage_index = 1

        if tumor_class[0] in ['T1', 'T1C+', 'T2']:
            cat_index = 1
            stage_index = 0

        scan_category = self.get_category(tumor_class[cat_index])

        scan['tumor_category_ai'] = scan_category
        scan['by_user'] = by_user

        if len(tumor_class) == 2:
            tumor_stage = TumorStageDAO().get_by_name(tumor_class[1])
            scan['tumor_stage_ai'] = tumor_stage

        # if scan_category != '_NORMAL':
        #     scan['tumor_predicted'] = True
        # else:
        #     scan['tumor_predicted'] = False

        scan['predicted_image'] = predicted_scan
        new_scan = ScanRecordDAO().update(self.scan_id, scan)

        return new_scan

    def get_category(self, category_name: str):
        category = TumorCategoryDAO().get_by_name(category_name)

        if not category:
            new_category = TumorCategoryDAO().create({'name': category_name})

            return new_category
        else:
            return category[0]

    def execute(self):
        scan = self.update_scan()

        return scan
