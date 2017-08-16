from collections import namedtuple

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
