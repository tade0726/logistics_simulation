from collections import namedtuple
from sqlalchemy.types import String, Integer, Text

__all__ = ["TruckRecord", "PackageRecord", "PipelineRecord", "PathRecord",
           "TruckRecordDict", "PackageRecordDict", "PipelineRecordDict", "PathRecordDict",
           "OutputTableColumnType", "not_right_on_time"]

TruckRecord = namedtuple("truck_record",
                         ["equipment_id", "truck_id", "truck_type", "time_stamp", "action", "store_size"])
PackageRecord = namedtuple("package_record", ["equipment_id", "parcel_id", "small_id", "parcel_type",
                                              "time_stamp", "action"])
PipelineRecord = namedtuple("pipeline_record", ["pipeline_id", "queue_id", "parcel_id", "small_id", "parcel_type",
                                                "time_stamp", "action"])
PathRecord = namedtuple("path_record", ["parcel_id", "small_id", "parcel_type", "start_node", "ident_des_zno",
                                        "sorter_type", "dest_type", "ret_path"])


class TruckRecordDict(dict):
    pass


class PackageRecordDict(dict):
    pass


class PipelineRecordDict(dict):
    pass


class PathRecordDict(dict):
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

    path_columns = dict(
        parcel_id=String(length=32, ),
        small_id=String(length=32, ),
        parcel_type=String(length=32,),
        start_node=String(length=32, ),
        ident_des_zno=String(length=32, ),
        sorter_type=String(length=32, ),
        dest_type=String(length=32, ),
        ret_path=Text(),
    )


def not_right_on_time(now:float, close_time_zones: list):
    """判断是否在关机的时间区间"""

    if close_time_zones:
        return None

    match_time_zone = [time_zone for time_zone in close_time_zones if (now >= time_zone[0] ) & (now <=time_zone[1])]
    return match_time_zone