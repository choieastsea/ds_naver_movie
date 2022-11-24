from selenium.webdriver.common.by import By
import datetime as dt


def crawl_movie(conn, cur, url, mid, driver):
    print(mid)
    driver.get(url)
    article = driver.find_element(By.CLASS_NAME, 'article')
    try:
        mv_info = article.find_element(By.CLASS_NAME, 'mv_info_area')
    except:
        pass
    """
    영화 제목
    """
    title = ""
    try:
        title = mv_info.find_element(By.CLASS_NAME, 'h_movie').find_element(By.XPATH,'a').text
    except:
        pass
    """
    영화 부제목
    """
    second_title = ""
    m_year = 0
    try:
        second_title = "".join(mv_info.find_element(By.CLASS_NAME, 'h_movie2').text.split(",")[:-1])
        m_year = int(mv_info.find_element(By.CLASS_NAME, 'h_movie2').text.split(",")[-1])
    except:
        pass
    """
    photo_url
    """
    photo_url = ""
    try:
        photo_url = mv_info.find_element(By.CLASS_NAME,'poster').find_element(By.XPATH,'a/img').get_attribute('src')
    except:
        pass
    
    """
    평점
    """
    user_point=0.0
    reporter_point = 0.0
    netizen_point = 0.0
    try:
        main_score = mv_info.find_element(By.CLASS_NAME, 'main_score')
        try:
            user_point = float(main_score.find_element(By.ID, 'actualPointPersentBasic').find_element(By.CLASS_NAME,'st_on').get_attribute('style').split(":")[1].split("%")[0])/10
        except:
            pass
        try:
            reporter_point = float(main_score.find_element(By.CLASS_NAME, 'spc_score_area').find_element(By.CLASS_NAME,'st_on').get_attribute('style').split(":")[1].split("%")[0])/10
        except:
            pass
        try:
            netizen_point = float(main_score.find_element(By.ID, 'pointNetizenPersentBasic').find_element(By.CLASS_NAME,'st_on').get_attribute('style').split(":")[1].split("%")[0])/10
        except:
            pass
    except:
        pass
    """
    opening-date
    genre
    nationality
    running_time
    domestic_rate
    foreign_rate
    """
    info_spec = mv_info.find_element(By.CLASS_NAME, 'info_spec')

    opening_date = ""
    genre = ""
    nationality = ""
    running_time = 0

    domestic_rate = ""
    foreign_rate = ""

    try:
        info_spec_as = info_spec.find_elements(By.TAG_NAME,'a')
        for a in info_spec_as:
            if(a.get_attribute('href').__contains__('genre')):
                genre = a.text
            if(a.get_attribute('href').__contains__('nation')):
                nationality = a.text
            if(a.get_attribute('href').__contains__('open')):
                opening_date += a.text
        info_spec_spans = info_spec.find_elements(By.TAG_NAME,'span')
        for span in info_spec_spans:
            if(span.text.__contains__('분')):
                running_time = int(span.text.split('분')[0])
        info_spec_ps = info_spec.find_elements(By.TAG_NAME,'p')
        for p in info_spec_ps:
            if(p.text.__contains__("국내")):
                domestic_rate = p.find_element(By.TAG_NAME,'a').text
            if(p.text.__contains__("해외")):
                foreign_rate = p.find_element(By.TAG_NAME,'a').text
    except:
        pass
    if(opening_date.__contains__(".") == True):
        if(len(opening_date.split("."))==2):
            opening_date += ".01"
    else:
        opening_date += ".01.01"
    datetime_format = "%Y.%m.%d"
    try:
        opening_date = dt.strptime(opening_date, datetime_format)
    except:
        opening_date = dt.datetime(1970, 1, 1, 1, 1, 1, 0)
    """
    summary
    """
    summary = ''
    try:
        summary = driver.find_element(By.CLASS_NAME,'con_tx').text
        if(len(summary)>=2000):
            summary = summary[0:1999]
    except:
        pass
    
    # print("title : ", title)
    # print("second_title : ", second_title)
    # print("photo_url : ", photo_url)
    # print("m_year : ", m_year)
    # print("user_point : ", user_point)
    # print("reporter_point : ", reporter_point)
    # print("netizen_point : ", netizen_point)
    # print("genre : ", genre)
    # print("nationality : ", nationality)
    # print("opening_date : ", opening_date)
    # print("running_time : ", running_time)
    # print("domestic_rate : ", domestic_rate)
    # print("foreign_rate : ", foreign_rate)
    # print("summary : ", summary)
    
    data = (mid, title, second_title, photo_url, m_year, user_point, reporter_point, netizen_point, nationality, running_time, opening_date, domestic_rate, foreign_rate, summary)
    
    insert_sql_movie ="""
    insert ignore into movie(m_id, title, second_title, photo_url, m_year, user_point, reporter_point, netizen_point, nationality, running_time, opening_date , domestic_rate, foreign_rate, summary)
        values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
    """
    insert_sql_genre="""
    insert ignore into movie_genre(m_id,genre)
        values(%s,%s);
    """
    update_sql ="""
    UPDATE naver_top_ranked_movie_list SET crawl_flag = %s WHERE m_id=%s;
    """

    cur.execute(insert_sql_movie, data)
    cur.execute(insert_sql_genre, (mid, genre))
    cur.execute(update_sql, (1, mid))
    conn.commit()
        