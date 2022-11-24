from selenium.webdriver.common.by import By
from datetime import datetime
import datetime as dt
from db_conn54 import *


def crawl_review(conn, cur, m_id, driver):
    page = 1
    rows = []
    print(m_id)
    for _ in range(10):
        review_url = f"https://movie.naver.com/movie/bi/mi/pointWriteFormList.naver?code={m_id}&type=after&isActualPointWriteExecute=false&isMileageSubscriptionAlready=false&isMileageSubscriptionReject=false&page={page}"
        driver.get(review_url)

        input_netizen  = driver.find_element(By.CLASS_NAME,'score_result')
        netizen_list = input_netizen.find_elements(By.TAG_NAME,'li')
        
        for netizen in netizen_list:
            point = 0
            short_review = ''
            user_id = ''
            review_date = dt.datetime(1970, 1, 1, 1, 1, 1, 0)

            """
            point
            """
            point = int(netizen.find_element(By.CLASS_NAME, 'star_score').find_element(By.TAG_NAME,'em').text.replace(' ',''))

            score_reple = netizen.find_element(By.CLASS_NAME, 'score_reple')

            """
            short_review
            """
            try:
                short_review = score_reple.find_element(By.CLASS_NAME,'_unfold_ment').find_element(By.TAG_NAME,'a').get_attribute('data-src')
                if len(short_review)>300:
                    short_review = short_review[0:299]
            except:
                short_reviews = score_reple.find_elements(By.XPATH,'p/span')
                if len(short_reviews) > 1:
                    short_review = short_reviews[1].text
                else:
                    short_review = short_reviews[0].text

            user_id = score_reple.find_element(By.XPATH,'dl/dt/em/a').text

            if len(user_id) > 20:
                user_id = user_id[:20]
            review_date_str = score_reple.find_elements(By.TAG_NAME,'em')[1].text

            datetime_format = "%Y.%m.%d %H:%M"
            try:
                review_date = datetime.strptime(review_date_str, datetime_format)
            except:
                review_date = dt.datetime(1970, 1, 1, 1, 1, 1, 0)

            rows.append((int(m_id),point,str(short_review),str(user_id),review_date))

        insert_movie_short_review_sql = """insert ignore into movie_short_review(m_id,point,short_review,user_id,review_date) values(%s,%s,%s,%s,%s); """
        cur.executemany(insert_movie_short_review_sql, rows)
        conn.commit()
        rows.clear()
        page += 1
        
    