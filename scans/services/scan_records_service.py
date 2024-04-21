from scans.daos import TumorCategoryDAO, TumorStageDAO, ScanRecordDAO
from users.daos import CustomUserDAO


class ScanRecordPService:
    def __init__(self, user_id: int, scan_id: int):
        self.scan_id = scan_id
        self.user_id = user_id

    def add_scan_images(self, scan_images: list):
        scan_record = ScanRecordDAO().update_scans(self.scan_id, {'scans': scan_images})

        return scan_record

    def set_tumor_category(self, tumor_category: str):
        tumor_category_obj = TumorCategoryDAO().get_by_name(tumor_category)[0]
        tumor_category_data = {}
        tumor_category_data['mean_tumor_category_ai'] = tumor_category_obj

        if tumor_category not in ['_NORMAL T1', '_NORMAL T2']:
            tumor_category_data['tumor_predicted'] = True

        else:
            tumor_category_data['tumor_predicted'] = False

        scan_record = ScanRecordDAO().update(self.scan_id, tumor_category_data)

        return scan_record
