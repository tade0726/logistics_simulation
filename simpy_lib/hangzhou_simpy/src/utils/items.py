from collections import namedtuple
from sqlalchemy.types import Integer, Text, DateTime, Float, VARCHAR
from sqlalchemy import Table, MetaData, Column

from simpy_lib.hangzhou_simpy.src.config import RemoteMySQLConfig

__all__ = ["TruckRecord", "PackageRecord", "PipelineRecord", "PathRecord",
           "TruckRecordDict", "PackageRecordDict", "PipelineRecordDict", "PathRecordDict",
           "SmallPackageRecordDict", "SmallPipelineRecordDict", "SmallPathRecordDict",
           "OutputTableColumnType", "machine_table_sche", "truck_table_sche", "pipeline_table_sche", "path_table_sche"]

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


class SmallPackageRecordDict(PackageRecordDict):
    pass


class SmallPipelineRecordDict(PipelineRecordDict):
    pass


class SmallPathRecordDict(PathRecordDict):
    pass


# data format for mysql
class OutputTableColumnType:

    truck_columns = dict(
        equipment_id=VARCHAR(length=32, ),
        truck_id=VARCHAR(length=32, ),
        truck_type=VARCHAR(length=32, ),
        action=VARCHAR(length=32, ),
        store_size=Integer(),
    )

    package_columns = dict(
        equipment_id=VARCHAR(length=32, ),
        parcel_id=VARCHAR(length=32, ),
        small_id=VARCHAR(length=32, ),
        parcel_type=VARCHAR(length=32, ),
        action=VARCHAR(length=32, ),
    )

    pipeline_columns = dict(
        pipeline_id=VARCHAR(length=32, ),
        queue_id=VARCHAR(length=32, ),
        parcel_id=VARCHAR(length=32, ),
        small_id=VARCHAR(length=32, ),
        parcel_type=VARCHAR(length=32, ),
        action=VARCHAR(length=32, ),
    )

    path_columns = dict(
        parcel_id=VARCHAR(length=32, ),
        small_id=VARCHAR(length=32, ),
        parcel_type=VARCHAR(length=32,),
        start_node=VARCHAR(length=32, ),
        ident_des_zno=VARCHAR(length=32, ),
        sorter_type=VARCHAR(length=32, ),
        dest_type=VARCHAR(length=32, ),
        ret_path=Text(),
    )


# tables schema
metadata = MetaData(bind=RemoteMySQLConfig.engine)

machine_table_sche = \
    Table(
        "o_machine_table",
        metadata,
        Column("equipment_id", VARCHAR(length=32, )),
        Column("parcel_id", VARCHAR(length=32, )),
        Column("small_id", VARCHAR(length=32, )),
        Column("parcel_type", VARCHAR(length=32, )),
        Column("time_stamp", Float(precision=2)),
        Column("action", VARCHAR(length=32, )),
        Column("real_time_stamp", DateTime()),
        Column("run_time", DateTime()),
    )

truck_table_sche = \
    Table(
        "o_truck_table",
        metadata,
        Column("equipment_id", VARCHAR(length=32, )),
        Column("truck_id", VARCHAR(length=32, )),
        Column("truck_type", VARCHAR(length=32, )),
        Column("time_stamp", Float(precision=2)),
        Column("action", VARCHAR(length=32, )),
        Column("store_size", Integer()),
        Column("real_time_stamp", DateTime()),
        Column("run_time", DateTime()),
    )

pipeline_table_sche = \
    Table(
        "o_pipeline_table",
        metadata,
        Column("pipeline_id", VARCHAR(length=32, )),
        Column("queue_id", VARCHAR(length=32, )),
        Column("parcel_id", VARCHAR(length=32, )),
        Column("small_id", VARCHAR(length=32, )),
        Column("parcel_type", VARCHAR(length=32, )),
        Column("time_stamp", Float(precision=2)),
        Column("action", VARCHAR(length=32, )),
        Column("real_time_stamp", DateTime()),
        Column("run_time", DateTime()),
    )

path_table_sche = \
    Table(
        "o_path_table",
        metadata,
        Column("parcel_id", VARCHAR(length=32, )),
        Column("small_id", VARCHAR(length=32, )),
        Column("parcel_type", VARCHAR(length=32, )),
        Column("start_node", VARCHAR(length=32, )),
        Column("ident_des_zno", VARCHAR(length=32, )),
        Column("sorter_type", VARCHAR(length=32, )),
        Column("dest_type", VARCHAR(length=32, )),
        Column("ret_path", Text()),
        Column("run_time", DateTime()),
    )
