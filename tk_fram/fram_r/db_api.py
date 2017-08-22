from .frame_r_view import CHECK_BTN_ENTRY_DIC, DATABASES, \
    CACHE_INSTANCE_DICT, DAY_TIME_DICT
from pymysql import connect


class Mysql(object):

    def __init__(self,):
        self.db_config = DATABASES

    @property
    def connect(self):
        return connect(host=self.db_config['HOST'],
                       user=self.db_config['USER'],
                       passwd=self.db_config['PASSWORD'],
                       db=self.db_config['NAME'])


def init_btn_entry_val_from_sql():
    """"""
    conn = Mysql().connect
    with conn as cur:
        cur.execute(
            "select equipment_port, equipment_status from i_equipment_io "
            "WHERE LEFT(equipment_port, 1) IN ('a', 'r', 'm', 'j', 'u', 'h')"
        )
        result = cur.fetchall()
    for item in result:
        CACHE_INSTANCE_DICT[item[0]]['status'] = item[1]
    with conn as cur:
        cur.execute(
            "select resource_id, resource_limit from i_resource_limit "
            "where resource_id like 'man_%' and resource_id not like 'man_x%'"
        )
        result = cur.fetchall()
    for item in result:
        CACHE_INSTANCE_DICT[item[0].replace('man_', '')]['num'] = int(item[1])
    return

def init_day_time():
    conn = Mysql().connect
    with conn as cur:
        cur.execute(
            "SELECT p.`start_time`, p.`end_time` "
            "FROM `i_equipment_io` AS p GROUP BY p.`start_time`,p.`end_time`"
        )
        result = cur.fetchall()
    for i in result:
        start_time, end_time = i
        day, start = str(start_time).split(' ')
        end = str(end_time).split(' ')[1]
        during_time = start + '-' + end
        DAY_TIME_DICT[day].append(during_time)

def update_on_off(cursor, start_time, run_arg):
    # equipment_port 需要确定
    for key, value in CACHE_INSTANCE_DICT.items():
        cursor.execute(
            "update i_equipment_io set equipment_status=%s where "
            "equipment_port='%s' and start_time='%s'" %
            (value['status'], key, start_time)
        )
    cursor.execute("update i_equipment_io set inserted_on='%s'" % run_arg)


def insert_package(cursor, num: str, run_arg):
    if num == 'all':
        num = '100000000'
    # ============================ 插入陆侧数据 ===============================
    cursor.execute("truncate i_od_parcel_landside")
    cursor.execute("truncate i_od_small_landside")

    cursor.execute('select count(1) from i_od_parcel_landside_day')
    land = int(cursor.fetchone()[0])
    cursor.execute('select count(1) from i_od_parcel_airside_day')
    air = int(cursor.fetchone()[0])

    land_num = int(int(num) * land / (land + air))
    land_parcel_num = int(land_num * 0.88)
    land_nc_num = int(land_num * 0.07)
    land_small_num = land_num - land_parcel_num - land_nc_num

    air_num = int(num) - land_num
    air_parcel_num = int(air_num * 0.88)
    air_nc_num = int(air_num * 0.07)
    air_small_num = air_num - air_parcel_num - air_nc_num
    cursor.execute(
        "insert into i_od_parcel_landside "
        "(parcel_id, src_dist_code, src_type, dest_dist_code, dest_zone_code,"
        " dest_type, plate_num, parcel_type, limit_type_code, arrive_time, "
        "send_time, inserted_on, modified_on) "
        "select "
        "parcel_id, src_dist_code, src_type, dest_dist_code, dest_zone_code, "
        "dest_type, plate_num, parcel_type, limit_type_code, arrive_time, "
        "send_time, inserted_on, modified_on "
        "from i_od_parcel_landside_day "
        "where parcel_type='parcel' "
        "limit %s" % land_parcel_num
    )
    cursor.execute(
        "insert into i_od_parcel_landside "
        "(parcel_id, src_dist_code, src_type, dest_dist_code, dest_zone_code,"
        " dest_type, plate_num, parcel_type, limit_type_code, arrive_time, "
        "send_time, inserted_on, modified_on) "
        "select "
        "parcel_id, src_dist_code, src_type, dest_dist_code, dest_zone_code, "
        "dest_type, plate_num, parcel_type, limit_type_code, arrive_time, "
        "send_time, inserted_on, modified_on "
        "from i_od_parcel_landside_day "
        "where parcel_type='nc' "
        "limit %s" % land_nc_num
    )
    cursor.execute(
        "insert into i_od_parcel_landside "
        "(parcel_id, src_dist_code, src_type, dest_dist_code, dest_zone_code,"
        " dest_type, plate_num, parcel_type, limit_type_code, arrive_time, "
        "send_time, inserted_on, modified_on) "
        "select "
        "parcel_id, src_dist_code, src_type, dest_dist_code, dest_zone_code, "
        "dest_type, plate_num, parcel_type, limit_type_code, arrive_time, "
        "send_time, inserted_on, modified_on "
        "from i_od_parcel_landside_day "
        "where parcel_type='small' "
        "limit %s" % land_small_num
    )
    cursor.execute(
        "INSERT into i_od_small_landside "
        "(small_id, parcel_id, src_dist_code, src_type, dest_dist_code, "
        "dest_zone_code, put_package_to_cage_tm, ident_des_zno, dest_type, "
        "plate_num, parcel_type, limit_type_code, arrive_time, send_time, "
        "inserted_on, modified_on) "
        "SELECT "
        "small_id, parcel_id, src_dist_code, src_type, dest_dist_code, "
        "dest_zone_code, put_package_to_cage_tm, ident_des_zno, dest_type, "
        "plate_num, parcel_type, limit_type_code, arrive_time, send_time, "
        "inserted_on, modified_on "
        "FROM `i_od_small_landside_day` AS s "
        "WHERE s.`parcel_id` IN "
        "( SELECT DISTINCT t.parcel_id "
        "FROM"
        "( SELECT f.parcel_id "
        "FROM i_od_parcel_landside_day AS f "
        "WHERE f.`parcel_type`='small' "
        "LIMIT %s) AS t)" % land_small_num
    )
    # ============================ 插入空侧数据 ===============================
    cursor.execute("truncate i_od_parcel_airside")
    cursor.execute("truncate i_od_small_airside")
    cursor.execute(
        "insert into i_od_parcel_airside "
        "(parcel_id, src_dist_code, src_type, dest_dist_code, dest_zone_code,"
        " dest_type, plate_num, parcel_type, limit_type_code, arrive_time, "
        "send_time, inserted_on, modified_on) "
        "select "
        "parcel_id, src_dist_code, src_type, dest_dist_code, dest_zone_code, "
        "dest_type, plate_num, parcel_type, limit_type_code, arrive_time, "
        "send_time, inserted_on, modified_on "
        "from i_od_parcel_airside_day "
        "where parcel_type='parcel' "
        "limit %s" % air_parcel_num
    )
    cursor.execute(
        "insert into i_od_parcel_airside "
        "(parcel_id, src_dist_code, src_type, dest_dist_code, dest_zone_code,"
        " dest_type, plate_num, parcel_type, limit_type_code, arrive_time, "
        "send_time, inserted_on, modified_on) "
        "select "
        "parcel_id, src_dist_code, src_type, dest_dist_code, dest_zone_code, "
        "dest_type, plate_num, parcel_type, limit_type_code, arrive_time, "
        "send_time, inserted_on, modified_on "
        "from i_od_parcel_airside_day "
        "where parcel_type='nc' "
        "limit %s" % air_nc_num
    )
    cursor.execute(
        "insert into i_od_parcel_airside "
        "(parcel_id, src_dist_code, src_type, dest_dist_code, dest_zone_code,"
        " dest_type, plate_num, parcel_type, limit_type_code, arrive_time, "
        "send_time, inserted_on, modified_on) "
        "select "
        "parcel_id, src_dist_code, src_type, dest_dist_code, dest_zone_code, "
        "dest_type, plate_num, parcel_type, limit_type_code, arrive_time, "
        "send_time, inserted_on, modified_on "
        "from i_od_parcel_airside_day "
        "where parcel_type='small' "
        "limit %s" % air_small_num
    )
    cursor.execute(
        "INSERT into i_od_small_airside "
        "(small_id, parcel_id, src_dist_code, src_type, dest_dist_code, "
        "dest_zone_code, put_package_to_cage_tm, ident_des_zno, dest_type, "
        "uld_num, plate_num, parcel_type, limit_type_code, arrive_time, "
        "send_time, inserted_on, modified_on) "
        "SELECT "
        "small_id, parcel_id, src_dist_code, src_type, dest_dist_code, "
        "dest_zone_code, put_package_to_cage_tm, ident_des_zno, dest_type, "
        "uld_num, plate_num, parcel_type, limit_type_code, arrive_time, "
        "send_time, inserted_on, modified_on "
        "FROM `i_od_small_airside_day` AS s "
        "WHERE s.`parcel_id` IN (SELECT DISTINCT t.parcel_id "
        "FROM(SELECT f.parcel_id FROM i_od_parcel_airside_day AS f "
        "WHERE f.`parcel_type`='small' "
        "LIMIT %s) AS t)" % air_small_num
    )
    cursor.execute("update i_od_parcel_landside set inserted_on='%s'" % run_arg)
    cursor.execute("update i_od_small_airside set inserted_on='%s'" % run_arg)


def update_person(cursor, start_time, run_arg):
    # 需要指定 resource_id 范围
    for key, value in CACHE_INSTANCE_DICT.items():
        cursor.execute("update i_resource_limit set resource_limit={} where "
                       "resource_id='man_{}' and "
                       "start_time='{}'".format(value['num'], key, start_time))
    cursor.execute("update i_resource_limit set inserted_on='%s'" % run_arg)


def read_result(cursor):
    cursor.execute(
        "select min(cast(real_time_stamp as datetime)), "
        "max(cast(real_time_stamp as datetime)) from o_machine_table where "
        "action='wait' and (equipment_id like 'r%' or equipment_id like 'a%')")

    fast_time, later_time = cursor.fetchone()
    cursor.execute(
        "select "
        "max(cast(real_time_stamp as datetime)), "
        "(max(time_stamp)-min(time_stamp))/3600 "
        "from o_machine_table "
        "where action='wait'"
    )
    last_solve_time, total_solve_time = cursor.fetchone()
    return {
        'fast_time': fast_time,
        'later_time': later_time,
        'last_solve_time': last_solve_time,
        'total_solve_time': total_solve_time
    }


def save_to_past_run(cursor):
    cursor.execute(
        "insert into i_equipment_io_past_run "
        "(run_time, equipment_port, equipment_id, process_time, "
        "allocate_rule, equipment_status, inserted_on, modified_on) "
        "select "
        "inserted_on, equipment_port, equipment_id, process_time, "
        "allocate_rule, equipment_status, inserted_on, modified_on "
        "from i_equipment_io"
    )

    cursor.execute(
        "insert into i_od_parcel_landside_past_run "
        "(run_time, parcel_id, src_dist_code, src_type, dest_dist_code, "
        "dest_zone_code, dest_type, plate_num, parcel_type, "
        "limit_type_code, arrive_time, send_time, inserted_on, modified_on) "
        "select "
        "inserted_on, parcel_id, src_dist_code, src_type, dest_dist_code, "
        "dest_zone_code, dest_type, plate_num, parcel_type, "
        "limit_type_code, arrive_time, send_time, inserted_on, modified_on "
        "from i_od_parcel_landside"
    )

    cursor.execute(
        "insert into i_resource_limit_past_run "
        "(run_time, resource_id, resource_name, resource_limit, "
        "capacity_per_resource, resource_on_number, resource_number, "
        "inserted_on, modified_on) "
        "select "
        "inserted_on, resource_id, resource_name, resource_limit, "
        "capacity_per_resource, resource_on_number, resource_number, "
        "inserted_on, modified_on "
        "from i_resource_limit"
    )

    cursor.execute(
        "insert into o_truck_table_past_run "
        "(equipment_id, truck_id, truck_type, time_stamp, action, store_size, "
        "real_time_stamp, run_time) "
        "select "
        "equipment_id, truck_id, truck_type, time_stamp, action, store_size, "
        "real_time_stamp, run_time "
        "from o_truck_table"
    )

    cursor.execute(
        "insert into o_pipeline_table_past_run "
        "(pipeline_id, queue_id, parcel_id, small_id, parcel_type, time_stamp, "
        "action, real_time_stamp, run_time)"
        "select "
        "pipeline_id, queue_id, parcel_id, small_id, parcel_type, time_stamp, "
        "action, real_time_stamp, run_time "
        "from o_pipeline_table"
    )

    cursor.execute(
        "insert into o_machine_table_past_run "
        "(equipment_id, parcel_id, small_id, parcel_type, time_stamp, action, "
        "real_time_stamp, run_time) "
        "select "
        "equipment_id, parcel_id, small_id, parcel_type, time_stamp, action, "
        "real_time_stamp, run_time "
        "from o_machine_table"
    )
    cursor.execute(
        "insert into o_path_table_past_run "
        "(parcel_id, small_id, parcel_type, start_node, ident_des_zno, "
        "sorter_type, dest_type, ret_path, run_time)"
        "select "
        "parcel_id, small_id, parcel_type, start_node, ident_des_zno, "
        "sorter_type, dest_type, ret_path, run_time "
        "from o_path_table"
    )

def delete_index(cursor):
    cursor.execute("drop index ix_o_machine_run_time_packageid on "
                   "o_machine_table;")

    cursor.execute("drop index ix_o_machine_table_equipment_id on "
                   "o_machine_table;")

    cursor.execute("drop index ix_o_pipeline_run_time_packageid on "
                   "o_pipeline_table;")


def create_index(cursor):
    cursor.execute("create index ix_o_machine_run_time_packageid on "
                   "o_machine_table (`package_id`)")

    cursor.execute("create index ix_o_machine_table_equipment_id on "
                   "o_machine_table (`equipment_id`)")

    cursor.execute("create index ix_o_pipeline_run_time_packageid on "
                   "o_pipeline_table(`package_id`)")
