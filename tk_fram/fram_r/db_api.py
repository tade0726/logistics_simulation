from .frame_r_view import CHECK_BTN_ENTRY_DIC, DATABASES, BTN_ENTRY_DICT
from pymysql import connect


def init_btn_entry_val_from_sql():
    """"""
    conn = connect(
        host=DATABASES['HOST'],
        user=DATABASES['USER'],
        passwd=DATABASES['PASSWORD'],
        db=DATABASES['NAME']
    )
    cur = conn.cursor()
    cur.execute("select equipment_port, equipment_status from i_equipment_io "
                "where equipment_id like 'r%'")
    result = cur.fetchall()
    for item in result:
        BTN_ENTRY_DICT[item[0]] = item[1]
    cur.close()
    conn.close()
    return BTN_ENTRY_DICT

def update_on_off(cursor, run_arg):
    # equipment_port 需要确定
    for key, value in CHECK_BTN_ENTRY_DIC.items():
        cursor.execute(
            "update i_equipment_io set equipment_status=%s where "
            "equipment_port='%s'" % (value.var.get(), key)
        )
    cursor.execute("update i_equipment_io set inserted_on='%s'" % run_arg)


def insert_package(cursor, num: str, run_arg):
    cursor.execute("truncate i_od_parcel_landside")
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
        "limit %s" % num
    )
    cursor.execute("update i_od_parcel_landside set inserted_on='%s'" % run_arg)


def update_person(cursor, num: str, run_arg):
    # 需要指定 resource_id 范围
    cursor.execute("update i_resource_limit set resource_limit={} where "
                   "resource_id like 'man_m%' ".format(num))
    cursor.execute("update i_resource_limit set inserted_on='%s'" % run_arg)


def read_result(cursor):
    cursor.execute(
        "select min(cast(real_time_stamp as datetime)), "
        "max(cast(real_time_stamp as datetime)) from o_machine_table where "
        "action='wait' and equipment_id like 'r%'")

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
        "(equipment_id, truck_id, time_stamp, action, store_size, "
        "real_time_stamp, run_time) "
        "select "
        "equipment_id, truck_id, time_stamp, action, store_size, "
        "real_time_stamp, run_time "
        "from o_truck_table"
    )

    cursor.execute(
        "insert into o_pipeline_table_past_run "
        "(pipeline_id, queue_id, package_id, time_stamp, action, "
        "real_time_stamp, run_time)"
        "select "
        "pipeline_id, queue_id, package_id, time_stamp, action, "
        "real_time_stamp, run_time "
        "from o_pipeline_table"
    )

    cursor.execute(
        "insert into o_machine_table_past_run "
        "(equipment_id, package_id, time_stamp, action, real_time_stamp, "
        "run_time) "
        "select "
        "equipment_id, package_id, time_stamp, action, real_time_stamp, "
        "run_time "
        "from o_machine_table"
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
