from pymysql import connect
import csv
import os
from collections import defaultdict

from tk_fram.frame_config import DATABASES
from .frame_view import CACHE_INSTANCE_DICT, DAY_TIME_DICT, CURRENT, \
    INIT_INSTANCE_DICT


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
    for date, times in DAY_TIME_DICT.items():
        for time in times:
            instance_status_num_dict = defaultdict(dict)
            init_instance_dict = defaultdict(dict)
            start_time = date + ' ' + time.split('-')[0]
            conn = Mysql().connect
            with conn as cur:
                cur.execute(
                    "select equipment_port, equipment_status "
                    "from i_equipment_io "
                    "WHERE start_time='{}' "
                    "and LEFT(equipment_port, 1) "
                    "IN ('a', 'r', 'm', 'j', 'u', 'h')".format(
                        start_time)
                )
                result = cur.fetchall()
            for item in result:
                instance_status_num_dict[item[0]]['status'] = item[1]
                init_instance_dict[item[0]]['status'] = item[1]
            with conn as cur:
                cur.execute(
                    "select resource_id, resource_limit "
                    "from i_resource_limit "
                    "where resource_id like 'man_%' "
                    "and start_time='{}' "
                    "and resource_id not like 'man_x%'".format(
                        start_time)
                )
                result = cur.fetchall()
            for item in result:
                instance_status_num_dict[item[0].replace('man_', '')]['num']\
                    = int(item[1])
                init_instance_dict[item[0].replace('man_', '')]['num'] \
                    = int(item[1])
            CACHE_INSTANCE_DICT[start_time] = instance_status_num_dict
            INIT_INSTANCE_DICT[start_time] = init_instance_dict
    return


def init_day_time():
    conn = Mysql().connect
    with conn as cur:
        cur.execute(
            "SELECT p.`start_time`, p.`end_time` "
            "FROM `i_equipment_io` AS p GROUP BY p.`start_time`,p.`end_time`"
        )
        result = cur.fetchall()
    for index, value in enumerate(result):
        start_time, end_time = value
        day, start = str(start_time).split(' ')
        end = str(end_time).split(' ')[1]
        period = start + '-' + end
        DAY_TIME_DICT[day].append(period)
        if index == 0:
            CURRENT['TIME']['date'] = day
            CURRENT['TIME']['time'] = period
            CURRENT['TIME']['start_time'] = str(start_time)
    with conn as cur:
        cur.execute(
            "select inserted_on from i_equipment_io_past_run "
            "ORDER BY inserted_on desc limit 1"
        )
        last_run_time = cur.fetchone()[0]
    CURRENT['TIME']['last_run_time'] = str(last_run_time)


def update_on_off(cursor, start_time, instance_dict, run_arg):
    # equipment_port 需要确定
    for key, value in instance_dict.items():
        cursor.execute(
            "update i_equipment_io set equipment_status=%s where "
            "equipment_port='%s' and start_time='%s'" %
            (value['status'], key, start_time)
        )
        INIT_INSTANCE_DICT[start_time][key]['status'] = value['status']
    cursor.execute("update i_equipment_io set inserted_on='%s'" % run_arg)


def create_columns(cursor, table):
    cursor.execute("show columns from %s" % table)
    column_tuple = cursor.fetchall()
    columns = ' ,'.join(i[0] for i in column_tuple)
    return columns


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

    columns_parcel_landside = create_columns(cursor, 'i_od_parcel_landside')
    columns_small_landside = create_columns(cursor, 'i_od_small_landside')

    columns_parcel_airside = create_columns(cursor, 'i_od_parcel_airside')
    columns_small_airside = create_columns(cursor, 'i_od_small_airside')
    cursor.execute(
        "insert into i_od_parcel_landside "
        "(%s) "
        "select "
        "%s "
        "from i_od_parcel_landside_day "
        "where parcel_type='parcel' "
        "order by arrive_time "
        "limit %s" %
        (columns_parcel_landside, columns_parcel_landside, land_parcel_num)
    )
    cursor.execute(
        "insert into i_od_parcel_landside "
        "(%s) "
        "select "
        "%s "
        "from i_od_parcel_landside_day "
        "where parcel_type='nc' "
        "order by arrive_time "
        "limit %s" %
        (columns_parcel_landside, columns_parcel_landside, land_nc_num)
    )
    cursor.execute(
        "insert into i_od_parcel_landside "
        "(%s) "
        "select "
        "%s "
        "from i_od_parcel_landside_day "
        "where parcel_type='small' "
        "order by arrive_time "
        "limit %s" %
        (columns_parcel_landside, columns_parcel_landside, land_small_num)
    )
    cursor.execute(
        "INSERT into i_od_small_landside "
        "(%s) "
        "SELECT "
        "%s "
        "FROM `i_od_small_landside_day` AS s "
        "WHERE s.`parcel_id` IN "
        "( SELECT DISTINCT t.parcel_id "
        "FROM"
        "( SELECT f.parcel_id "
        "FROM i_od_parcel_landside_day AS f "
        "WHERE f.`parcel_type`='small' "
        "order by arrive_time "
        "LIMIT %s) AS t)" %
        (columns_small_landside, columns_small_landside, land_small_num)
    )
    # ============================ 插入空侧数据 ===============================
    cursor.execute("truncate i_od_parcel_airside")
    cursor.execute("truncate i_od_small_airside")
    cursor.execute(
        "insert into i_od_parcel_airside "
        "(%s) "
        "select "
        "%s "
        "from i_od_parcel_airside_day "
        "where parcel_type='parcel' "
        "limit %s" %
        (columns_parcel_airside, columns_parcel_airside, air_parcel_num)
    )
    cursor.execute(
        "insert into i_od_parcel_airside "
        "(%s) "
        "select "
        "%s "
        "from i_od_parcel_airside_day "
        "where parcel_type='nc' "
        "limit %s" %
        (columns_parcel_airside, columns_parcel_airside, air_nc_num)
    )
    cursor.execute(
        "insert into i_od_parcel_airside "
        "(%s) "
        "select "
        "%s "
        "from i_od_parcel_airside_day "
        "where parcel_type='small' "
        "limit %s" %
        (columns_parcel_airside, columns_parcel_airside, air_small_num)
    )
    cursor.execute(
        "INSERT into i_od_small_airside "
        "(%s) "
        "SELECT "
        "%s "
        "FROM `i_od_small_airside_day` AS s "
        "WHERE s.`parcel_id` IN (SELECT DISTINCT t.parcel_id "
        "FROM(SELECT f.parcel_id FROM i_od_parcel_airside_day AS f "
        "WHERE f.`parcel_type`='small' "
        "LIMIT %s) AS t)" %
        (columns_small_airside, columns_small_airside, air_small_num)
    )
    cursor.execute("update i_od_parcel_landside set inserted_on='%s'" % run_arg)
    cursor.execute("update i_od_small_landside set inserted_on='%s'" % run_arg)
    cursor.execute("update i_od_parcel_airside set inserted_on='%s'" % run_arg)
    cursor.execute("update i_od_small_airside set inserted_on='%s'" % run_arg)


def update_person(cursor, start_time, instance_dict, run_arg):
    # 需要指定 resource_id 范围
    for key, value in instance_dict.items():
        cursor.execute("update i_resource_limit set resource_limit={} where "
                       "resource_id='man_{}' and "
                       "start_time='{}'".format(value['num'], key, start_time))
        INIT_INSTANCE_DICT[start_time][key]['num'] = value['num']
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


def average_time(cursor):
    # 票均时间
    cursor.execute(
        "select max(time_stamp) - min(time_stamp) "
        "from o_machine_table group by small_id"
    )
    result = cursor.fetchall()
    time_sum = sum(float(i[0]) for i in result)
    average = time_sum / len(result)
    return average


def success_percent(cursor):
    # 时效达成率
    cursor.execute(
        "select count(case when a.real_time_stamp<=b.plan_disallow_tm then "
        "a.small_id else null end)/count(a.small_id) "
        "from (select small_id,max(real_time_stamp) real_time_stamp "
        "from o_machine_table group by small_id) a "
        "join (select small_id ,plan_disallow_tm from i_od_small_airside "
        "union all "
        "select parcel_id,plan_disallow_tm "
        "from i_od_parcel_airside union all "
        "select small_id ,plan_disallow_tm "
        "from i_od_small_landside union all "
        "select parcel_id,plan_disallow_tm "
        "from i_od_parcel_landside) b on a.small_id=b.small_id"
    )
    result = cursor.fetchone()[0]
    return result


def discharge(cursor):
    cursor.execute(
        "select (sum(case when action='start' "
        "then time_stamp else 0 end)-sum(case when action='wait' "
        "then time_stamp else 0 end))/count(distinct small_id) "
        "from o_machine_table where equipment_id like 'r%'"
    )
    result = cursor.fetchone()[0]
    return result


def save_to_past_run(cursor):
    columns_equipment_io = create_columns(cursor, 'i_equipment_io')
    columns_resource_limit = create_columns(cursor, 'i_resource_limit')
    columns_parcel_landside = create_columns(cursor, 'i_od_parcel_landside')
    columns_parcel_airside = create_columns(cursor, 'i_od_parcel_airside')
    columns_small_landside = create_columns(cursor, 'i_od_small_landside')
    columns_small_airside = create_columns(cursor, 'i_od_small_airside')
    columns_truck = create_columns(cursor, 'o_truck_table')
    columns_pipeline = create_columns(cursor, 'o_pipeline_table')
    columns_machine = create_columns(cursor, 'o_machine_table')
    columns_path = create_columns(cursor, 'o_path_table')
    cursor.execute(
        "insert into i_equipment_io_past_run "
        "(run_time, %s) "
        "select "
        "inserted_on, %s "
        "from i_equipment_io" %
        (columns_equipment_io, columns_equipment_io)
    )

    cursor.execute(
        "insert into i_resource_limit_past_run "
        "(run_time, %s) "
        "select "
        "inserted_on, %s "
        "from i_resource_limit" %
        (columns_resource_limit, columns_resource_limit)
    )

    cursor.execute(
        "insert into i_od_parcel_landside_past_run "
        "(run_time, %s) "
        "select "
        "inserted_on, %s "
        "from i_od_parcel_landside" %
        (columns_parcel_landside, columns_parcel_landside)
    )

    cursor.execute(
        "insert into i_od_small_landside_past_run "
        "(run_time, %s) "
        "select "
        "inserted_on, %s "
        "from i_od_small_landside" %
        (columns_small_landside, columns_small_landside)
    )

    cursor.execute(
        "insert into i_od_parcel_airside_past_run "
        "(run_time, %s) "
        "select "
        "inserted_on, %s "
        "from i_od_parcel_airside" %
        (columns_parcel_airside, columns_parcel_airside)
    )

    cursor.execute(
        "insert into i_od_small_airside_past_run "
        "(run_time, %s) "
        "select "
        "inserted_on, %s "
        "from i_od_small_airside" %
        (columns_small_airside, columns_small_airside)
    )

    cursor.execute(
        "insert into o_truck_table_past_run "
        "(%s) "
        "select "
        "%s "
        "from o_truck_table" %
        (columns_truck, columns_truck)
    )

    cursor.execute(
        "insert into o_pipeline_table_past_run "
        "(%s)"
        "select "
        "%s "
        "from o_pipeline_table" %
        (columns_pipeline, columns_pipeline)
    )

    cursor.execute(
        "insert into o_machine_table_past_run "
        "(%s) "
        "select "
        "%s "
        "from o_machine_table" %
        (columns_machine, columns_machine)
    )
    cursor.execute(
        "insert into o_path_table_past_run "
        "(%s)"
        "select "
        "%s "
        "from o_path_table" % (columns_path, columns_path)
    )


def csv_into_mysql(cursor):

    def creat_generator(csv_reader):
        # 读取 csv.reader 对象，返回指定内容长度的生成器，x 控制内容长度
        while True:
            line_list = []
            x = 1
            for value in csv_reader:
                line_list.append(value)
                x += 1
                if x == 1000000:
                    break
            yield line_list

    project_path = os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    )
    file_path_dict = {
        'o_machine_table': os.path.join(
            project_path, r'simpy_lib\hangzhou_simpy\out\machine_table.csv'),
        # 'o_path_table': os.path.join(
        #     project_path, r'simpy_lib\hangzhou_simpy\out\path_table.csv'),
        # 'o_pipeline_table': os.path.join(
        #     project_path, r'simpy_lib\hangzhou_simpy\out\pipeline_table.csv'),
        # 'o_truck_table': os.path.join(
        #     project_path, r'simpy_lib\hangzhou_simpy\out\truck_table.csv'),
                      }
    for table, file_path in file_path_dict.items():
        files = csv.reader(open(file_path))
        columns = ''
        lenth = 0
        for i, v in enumerate(files):
            if i == 0:
                columns = ', '.join(v)
                lenth = len(v)
                break
        for item in creat_generator(files):
            if item:
                cursor.executemany(
                    "insert into {} ({}) values "
                    "(%s".format(table, columns) + ', %s' * (lenth - 1) + ')',
                    item)
            else:
                break


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
