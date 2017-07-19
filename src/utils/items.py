from collections import namedtuple

__all__ = ["TruckRecord", "PackageRecord"]

TruckRecord = namedtuple("truck_record", ["machine_id", "truck_id", "time_stamp", "action"])
PackageRecord = namedtuple("package_record", ["machine_id", "package_id", "time_stamp", "action"])