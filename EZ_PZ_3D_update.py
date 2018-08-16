from Web_scrapper import login_xpath as login
from Web_scrapper import headless_mode
from datetime import date,timedelta
import time
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select
from pymongo import MongoClient
import pymongo

'''a function iterate through the page and put the revenue info in the data base
'''
def info_getter(Collection,driver):
    i = 2
    for something in range(100):
        try:
            game_date = driver.find_element_by_xpath('//*[@id="__t_grid_0"]/tbody/tr['+str(i)+']/td[1]')
            dau = driver.find_element_by_xpath('//*[@id="__t_grid_0"]/tbody/tr['+str(i)+']/td[4]')
            dou = driver.find_element_by_xpath('//*[@id="__t_grid_0"]/tbody/tr['+str(i)+']/td[5]')
            dnu = driver.find_element_by_xpath('//*[@id="__t_grid_0"]/tbody/tr['+str(i)+']/td[6]')
            revenue = driver.find_element_by_xpath('//*[@id="__t_grid_0"]/tbody/tr['+str(i)+']/td[7]')
            paid_players = driver.find_element_by_xpath('//*[@id="__t_grid_0"]/tbody/tr['+str(i)+']/td[8]')
            new_paid_players = driver.find_element_by_xpath('//*[@id="__t_grid_0"]/tbody/tr['+str(i)+']/td[9]')
            post = { 'dau' : int(dau.text),
                     'dou' : int(dou.text),
                     'dnu' : int(dnu.text),
                     'revenue' : float(revenue.text),
                     'paid_players' : int(paid_players.text),
                     'new_paid_players' : int(new_paid_players.text),
                     'date' : game_date.text
                     }
            Collection.insert_one(post)
            print(game_date.text + ' data insert completed')
            i +=1
        except NoSuchElementException:
            break

def page_navi(Collection,driver,sleep_time,start_date,end_date):
    time.sleep(sleep_time)
    url = 'http://data.r2games.com/mobile/?r=complex%2Findex&m=M354&p=mobile&g=bzdxc&server=ALL&time_start='+start_date.isoformat()+'&time_end='+end_date.isoformat()+'&show=ByDate'
    driver.get(url)
    show_content = driver.find_element_by_xpath('//*[@id="grid_0"]/div[2]/p/select')
    show = Select(show_content)
    show.select_by_value('100')
    info_getter(Collection,driver)


def update():
    client = MongoClient()
    DB = client.Mobile_revenue
    Collection = DB.EZ_PZ_RPG_3D
    Collection.create_index([('date',pymongo.ASCENDING)],unique = True)
    sleep_time = 0.5
    last_date = Collection.find().distinct('date')[-1]
    last_date = last_date.split('-')
    last_date = date(int(last_date[0]),int(last_date[1]),int(last_date[2]))
    start_date = last_date+timedelta(days=1)
    end_date = date.today()-timedelta(days=1)
    days_intervel = 31

    url = 'http://acc.r2games.com/main/?r=site/login'
    account_xpath = '//*[@id="login-form"]/dl/dd[1]/input'
    password_xpath = '//*[@id="login-form"]/dl/dd[2]/input'
    login_xpath = '//*[@id="submit-btn"]'
    account_content = '10024'
    password_content = 'yyy666'
    driver = headless_mode()
    login(driver,url,account_xpath,password_xpath,login_xpath,account_content,password_content)
    start_date_real = start_date
    page_navi(Collection,driver,sleep_time,start_date_real,end_date)
    driver.quit()

if __name__ == '__main__':
    update()
