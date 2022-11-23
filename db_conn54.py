import pymysql

def open_db():
    conn = pymysql.connect(
        host="localhost",
        user="db_konkuk",
        password="6812",
        db="data_science",
        unix_socket="/tmp/mysql.sock",
    )
    cur = conn.cursor(pymysql.cursors.DictCursor)
    return conn, cur

def close_db(conn, cur):
    cur.close()
    conn.close()

def get_movie_url(cur):
    sql = """select url from naver_top_ranked_movie_list;"""
    cur.execute(sql)
    url = cur.fetchall()
    return url

def get_person_pid(cur):
    sql = """select distinct p_id from movie_person;"""
    cur.execute(sql)
    pid_list = cur.fetchall()
    return pid_list

# create table movie_person (
#     m_id int,
#     p_id int,
#     role varchar(100),
#     character_ varchar(100),
#     enter_date datetime default now(),    
#     index idx_mid_pid(m_id, p_id),
#     index idx_mid(m_id),
#     index idx_pid(p_id)
# );