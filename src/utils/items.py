from collections import namedtuple
from sqlalchemy.types import String, Integer

__all__ = ["TruckRecord", "PackageRecord", "PipelineRecord",
           "TruckRecordDict", "PackageRecordDict", "PipelineRecordDict"]

TruckRecord = namedtuple("truck_record",
                         ["equipment_id", "truck_id", "truck_type", "time_stamp", "action", "store_size"])
PackageRecord = namedtuple("package_record", ["equipment_id", "parcel_id", "small_id", "parcel_type",
                                              "time_stamp", "action"])
PipelineRecord = namedtuple("pipeline_record", ["pipeline_id", "queue_id", "parcel_id", "small_id", "parcel_type",
                                                "time_stamp", "action"])


class TruckRecordDict(dict):
    pass


class PackageRecordDict(dict):
    pass


class PipelineRecordDict(dict):
    pass


# data format for mysql
class OutputTableColumnType:

    truck_columns = dict(
        equipment_id=String(length=32, ),
        truck_id=String(length=32, ),
        truck_type=String(length=32, ),
        action=String(length=32, ),
        store_size=Integer(),
    )

    package_columns = dict(
        equipment_id=String(length=32, ),
        parcel_id=String(length=32, ),
        small_id=String(length=32, ),
        parcel_type=String(length=32, ),
        action=String(length=32, ),
    )

    pipeline_columns = dict(
        pipeline_id=String(length=32, ),
        queue_id=String(length=32, ),
        parcel_id=String(length=32, ),
        small_id=String(length=32, ),
        parcel_type=String(length=32, ),
        action=String(length=32, ),
    )