from collections import namedtuple

__all__ = ["TruckRecord", "PackageRecord", "PipelineRecord"]

TruckRecord = namedtuple("truck_record", ["equipment_id", "truck_id", "time_stamp", "action", "store_size"])
PackageRecord = namedtuple("package_record", ["equipment_id", "package_id", "time_stamp", "action"])
PipelineRecord = namedtuple("pipeline_record", ["pipeline_id", "queue_id", "package_id", "time_stamp", "action"])
SmallPackageRecord = namedtuple("small_package_record", ["equipment_id", "package_id", "small_id", "time_stamp", "action"])