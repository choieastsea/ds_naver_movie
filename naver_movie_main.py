from db_conn54 import *
from selenium import webdriver
from crawl_naver_movie_ranking_list import *
from naver_login import *
from crawl_movie import *
from crawl_movie_person import *
from crawl_person import *
from crawl_review import *

if __name__ == "__main__":
    conn, cur = open_db()
    chromedriver_file = './chromedriver'
    driver = webdriver.Chrome(chromedriver_file)
    driver = naver_login(driver)    #naver login for adult movies

    """ make top ranked movie list """
    crawl_naver_top_ranked_movie_list()

    url_list = get_movie_url(cur)
    movie_list = get_movie_list(cur)

    """MOVIE"""
    for movie in movie_list:
        if movie['m_id'] >=10700:
            crawl_movie(conn, cur, movie['url'],movie['m_id'], driver)

    """MOVIE PERSON"""
    for url in url_list:
        crawl_movie_person(conn, cur, url['url'], driver)
    
    """PERSON"""
    # test
    # crawl_person(conn, cur, '5159', driver) #적당한 데이터
    # crawl_person(conn, cur, '104700', driver) #거의 없는 데이터
    # crawl_person(conn, cur, '59818', driver) #많은 데이터
    # crawl_person(conn, cur, '39130', driver) #summary
    # crawl_person(conn, cur, '5967', driver) #height 에러

    pid_list = get_person_pid(cur)

    for pid in pid_list:
        print(pid['p_id'])
        if pid['p_id'] > 0:
            crawl_person(conn, cur, pid['p_id'], driver)

    """REVIEW"""
    mid_list = get_movie_id(cur)
    for mid in mid_list:
        # print(mid['m_id'])
        if mid['m_id'] != 75606:    #리뷰 없는 케이스 제외
            crawl_review(conn, cur, mid['m_id'], driver)
    close_db(conn, cur)
    