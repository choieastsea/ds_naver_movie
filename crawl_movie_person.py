from selenium import webdriver
from selenium.webdriver.common.by import By

def crawl_movie_person(conn, cur, url, driver):
    # 한 영화에 대하여 '상세정보'에 들어가서 인물정보를 저장한다
    m_id = int(url.split('=')[-1])
    print(f'mid : {m_id}')
    driver.get(f'https://movie.naver.com/movie/bi/mi/detail.naver?code={m_id}')
    
    #더보기 버튼 활성화
    try:
        driver.find_element(By.ID, 'actorMore').click() 
    except:
        pass

    """
    배우
    """
    person_list = driver.find_elements(By.CLASS_NAME, 'p_info')
    sql_list = []
    for person in person_list:
        try:
            p_id = person.find_element(By.XPATH, 'a').get_attribute('href').split('code=')[1] 
        except:
            p_id = -1   #pid 없는 경우
        try:
            # 주연 / 조연 등
            role = person.find_element(By.CLASS_NAME, 'p_part').text
        except:
            role = ''
        try:
            # ~~ 역
            character = person.find_element(By.CLASS_NAME, 'pe_cmt').find_element(By.XPATH,'span').text.replace('역','').strip()
        except:
            character =''
        sql_list.append((m_id, p_id, role, character))
        print(f'mid:{m_id}\npid:{p_id}\nrole:{role}\ncharacter:{character}\n===========================')

    """
    단역 및 특별출연
    """
    try:
        person_span_list_row = driver.find_element(By.ID, 'subActorList').find_elements(By.XPATH,'tbody/tr')
    except:
        person_span_list_row = []
    
    for row in person_span_list_row:
        try: 
            role = row.find_element(By.XPATH,'th/img').get_attribute('alt') #단역, 특별출연 등
        except:
            role = ''
        person_list = row.find_elements(By.XPATH,'td/span')
        for person in person_list:
            try:
                p_id = person.find_element(By.XPATH,'a').get_attribute('href').split('code=')[1]
            except:
                p_id = -1
            try:
                character = person.find_element(By.XPATH,'em').text
            except:
                character = ''
            sql_list.append((m_id, p_id, role, character))
            print(f'mid:{m_id}\npid:{p_id}\nrole:{role}\ncharacter:{character}\n===========================')
    """
    감독 
    """
    try:
        director_list = driver.find_elements(By.CLASS_NAME,'dir_product')
    except:
        director_list = []
    for director in director_list:
        try:
            p_id = director.find_element(By.XPATH, 'a').get_attribute('href').split('code=')[1]
        except:
            p_id =-1
        role = '감독'
        character = ''
        sql_list.append((m_id, p_id, role, character))
        print(f'mid:{m_id}\npid:{p_id}\nrole:{role}\ncharacter:{character}\n===========================')

    insert_sql = """
        insert into movie_person(m_id, p_id, role, character_)
        values(%s,%s,%s,%s); """
    cur.executemany(insert_sql, sql_list)
    conn.commit()


    