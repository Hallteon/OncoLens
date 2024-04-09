from scans.models import ScanRecord, TumorCategory, TumorStage


class ScanRecordDAO:
    __slots__ = ('_db',)

    def __init__(self):
        self._db = ScanRecord

    def get(self, scan_id: int):
        return self._db.objects.get(id=scan_id)

    def create(self, data: dict):
        return self._db.objects.create(**data)

    def update(self, scan_id: int, data: dict):
        scan = self.get(scan_id)

        for key, value in data.items():
            setattr(scan, key, value)

        scan.save()

        return scan


class TumorCategoryDAO:
    __slots__ = ('_db',)

    def __init__(self):
        self._db = TumorCategory

    def create(self, data: dict):
        category = self._db.objects.create(**data)

        return category

    def get(self, category_id: int):
        return self._db.objects.get(id=category_id)

    def get_by_name(self, category: str):
        return self._db.objects.filter(name=category)


class TumorStageDAO:
    __slots__ = ('_db',)

    def __init__(self):
        self._db = TumorStage

    def create(self, data: dict):
        return self._db.objects.create(**data)

    def get(self, stage_id: int):
        return self._db.objects.get(id=stage_id)

    def get_by_name(self, stage: str):
        return self._db.objects.filter(name=stage).first()


