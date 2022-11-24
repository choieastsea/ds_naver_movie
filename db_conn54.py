import pymysql

def open_db():
    conn = pymysql.connect(
        host="localhost",
        user="username",
        password="password",
        db="dbname",
        unix_socket="/tmp/mysql.sock",
    )
    cur = conn.cursor(pymysql.cursors.DictCursor)
    return conn, cur

def close_db(conn, cur):
    cur.close()
    conn.close()

def get_movie_list(cur):
    sql = """select * from naver_top_ranked_movie_list;"""
    cur.execute(sql)
    movie_list = cur.fetchall()
    return movie_list

def get_movie_url(cur):
    sql = """select url from naver_top_ranked_movie_list;"""
    cur.execute(sql)
    url = cur.fetchall()
    return url

def get_movie_id(cur):
    sql="""select m_id from naver_top_ranked_movie_list;"""
    cur.execute(sql)
    mid_list = cur.fetchall()
    return mid_list

def get_person_pid(cur):
    sql = """select distinct p_id from movie_person where p_id not in (select p_id from person);"""
    cur.execute(sql)
    pid_list = cur.fetchall()
    return pid_list
