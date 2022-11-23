from db_conn54 import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from crawl_naver_movie_ranking_list import *
from crawl_movie_person import *

if __name__ == "__main__":
    conn, cur = open_db()
    chromedriver_file = './chromedriver'
    driver = webdriver.Chrome(chromedriver_file)
    # make top ranked movie list
    # crawl_naver_top_ranked_movie_list()
    url_list = get_movie_url(conn, cur)
    # print(len(url_list))

    #movie person test
    # crawl_movie_person(conn, cur, 'https://movie.naver.com/movie/bi/mi/detail.naver?code=192608', driver)


    for url in url_list:
        crawl_movie_person(conn, cur, url['url'], driver)
    close_db(conn, cur)