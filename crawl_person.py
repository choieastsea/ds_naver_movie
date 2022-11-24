import datetime
from selenium.webdriver.common.by import By

def crawl_person(conn, cur, pid, driver):
    """한 인물 페이지에 대하여 인물정보를 저장한다"""
    driver.get(f'https://movie.naver.com/movie/bi/pi/basic.naver?code={pid}')
    person_info = driver.find_element(By.CLASS_NAME,'mv_info_area')
    
    """
    이름(name)
    """
    try:
        name = person_info.find_element(By.XPATH,'div/h3/a').text
    except:
        name =''
    if len(name) > 50:
        name = name[:50]
    """
    영어이름(eng_name)
    """
    try:
        eng_name = person_info.find_element(By.XPATH,'div/strong').text
        if len(eng_name) > 100:
            eng_name = eng_name[:100]
        # for char in eng_name: #영어는 에라 모르겠다~
        #     if char.isalpha():
    except:
        eng_name = ''

    """
    photo_url
    """
    try:
        photo_url = person_info.find_element(By.CLASS_NAME, 'poster').find_element(By.XPATH, 'img').get_attribute('src')
    except:
        photo_url = 'https://ssl.pstatic.net/static/movie/2012/06/dft_img120x150.png'

    """
    birth_date & birth_location
    """
    try:
        birth_str = person_info.find_element(By.CLASS_NAME, 'info_spec').find_element(By.CLASS_NAME, 'step5').find_element(By.XPATH,'following-sibling::dd').text
        birth_date_str = birth_str.split('/')[0].replace('년','.').replace('월','.').replace('일','.').replace(' ','').strip()
        birth_location_str = birth_str.split('/')[1].strip()
    except:
        birth_date_str = "1900.1.1."
        birth_location_str = None
    birth_date_str = birth_date_str.split('.')
    try:
        year = int(birth_date_str[0])
        month = int(birth_date_str[1])
        date = int(birth_date_str[2])
        birth_date = datetime.date(year, month, date)
    except:
        year = 1900
        month = 1
        date = 1
        birth_date = None
    """
    award
    """
    try:
        award = person_info.find_element(By.CLASS_NAME, 'info_spec').find_element(By.CLASS_NAME, 'step8').find_element(By.XPATH,'following-sibling::dd').text
    except:
        award = None
    """
    nickname, height, weight, family, education, summary
    """
    try:
        driver.find_element(By.ID, 'peopleInfoButton').click()
    except:
        pass

    try:
        profile = driver.find_element(By.CLASS_NAME, 'profile')
    except:
        pass
    
    try:
        profile_title_list = profile.find_element(By.CLASS_NAME, 'tbl_profile').find_elements(By.XPATH, 'tbody/tr/th')
    except:
        profile_title_list = []
    profile_dict = {"별명" : "nickname", "신체" : "body", "가족" : "family", "학력" : "education"}

    nickname = None
    height = None
    weight = None
    family = None
    education = None

    for profile_title in profile_title_list:
        try:
            title = profile_title.find_element(By.XPATH,'img').get_attribute('alt')
            if title in profile_dict:
                content = profile_title.find_element(By.XPATH,'following-sibling::td').text
                # print(f'{profile_dict[title]} : {content}')
                if profile_dict[title] == "nickname":
                    nickname = content
                    if len(nickname) > 50:
                        nickname = nickname[:50]
                if profile_dict[title] == "body":
                    # print(f"body : {content}")
                    body_split = content.split(',')
                    if len(body_split)==2:
                        height = body_split[0].replace('cm','')
                        weight = body_split[1].replace('kg','')
                    height = body_split[0].replace('cm','')
                if profile_dict[title] == "family":
                    family = content
                    if len(family) > 100:
                        family = family[:100]
                if profile_dict[title] == "education":
                    education = content
                    if len(education) > 100:
                        education = education[:100]
        except:
            pass

    summary = None
    try:
        summary = profile.find_element(By.CLASS_NAME, 'con_tx').find_element(By.XPATH,'p').text
        if len(summary)>2000:
            summary = summary[:2000]
    except:
        pass

    print(f"pid: {pid}\nname: {name}\neng_name : {eng_name}")
    print(f"photo_url : {photo_url}\nbirth_date_str : {birth_date_str}")
    print(f"birth_location_str : {birth_location_str}\nbirth_date : {birth_date}")
    print(f"award : {award}")
    print(f"nickname : {nickname}, height : {height}, weight: {weight}, family:{family}, edu:{education}")
    print(f"summary: {summary}")
    print('==================================')
    sql = (pid, name, eng_name, photo_url, birth_date, birth_location_str, award, nickname, height, weight, family, education, summary)
    insert_sql = """
        insert ignore into person(p_id, name, eng_name, photo_url, birth_date, birth_location, award, nickname, height, weight, family, education, summary)
        values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s); """
    cur.execute(insert_sql, sql)
    conn.commit()

"""
    p_id int primary key,
    name varchar(50),
    eng_name varchar(100),
    photo_url varchar(500),
    birth_date date,
    birth_location varchar(50),
    award varchar(300),
    nickname varchar(50),
    height int,
    weight int,
    family varchar(100),
    education varchar(100),
    summary varchar(2000),
    enter_date datetime default now()    
"""
