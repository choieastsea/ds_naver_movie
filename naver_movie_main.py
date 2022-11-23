from db_conn54 import *
from selenium import webdriver
from crawl_naver_movie_ranking_list import *
from crawl_movie_person import *
from crawl_person import *

if __name__ == "__main__":
    conn, cur = open_db()
    chromedriver_file = './chromedriver'
    driver = webdriver.Chrome(chromedriver_file)
    """ make top ranked movie list """
    # crawl_naver_top_ranked_movie_list()

    url_list = get_movie_url(cur)
    # print(len(url_list))

    #movie person test
    # crawl_movie_person(conn, cur, 'https://movie.naver.com/movie/bi/mi/detail.naver?code=192608', driver)

    """MOVIE PERSON"""
    # for url in url_list:
        # crawl_movie_person(conn, cur, url['url'], driver)
    
    """PERSON"""
    # test
    # '104700'도 해보기 ~
    # crawl_person(conn, cur, '5159', driver) #적당한 데이터
    # crawl_person(conn, cur, '104700', driver) #거의 없는 데이터
    # crawl_person(conn, cur, '59818', driver) #많은 데이터
    # crawl_person(conn, cur, '39130', driver) #summary


    pid_list = get_person_pid(cur)
    for pid in pid_list:
        print(pid['p_id'])
        if pid['p_id'] > 0:
            crawl_person(conn, cur, pid['p_id'], driver)

    close_db(conn, cur)