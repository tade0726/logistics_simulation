from collections import namedtuple
from sqlalchemy.types import String, Integer


__all__ = ["TruckRecord", "PackageRecord", "PipelineRecord", "OutputTableColumnType"]

TruckRecord = namedtuple("truck_record", ["equipment_id", "truck_id", "time_stamp", "action", "store_size"])
PackageRecord = namedtuple("package_record", ["equipment_id", "package_id", "time_stamp", "action"])
PipelineRecord = namedtuple("pipeline_record", ["pipeline_id", "queue_id", "package_id", "time_stamp", "action"])


class OutputTableColumnType:

    truck_columns = dict(
        equipment_id=String(length=32, ),
        truck_id=String(length=32, ),
        action=String(length=32, ),
        store_size=Integer(),
    )

    package_columns = dict(
        equipment_id=String(length=32, ),
        package_id=String(length=32, ),
        action=String(length=32, ),
    )

    pipeline_columns = dict(
        pipeline_id=String(length=32, ),
        queue_id=String(length=32, ),
        package_id=String(length=32, ),
        action=String(length=32, ),
    )