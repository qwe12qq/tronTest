import time
from selenium import webdriver
from selenium.webdriver import Chrome

def main():
    print ("hello")
    option = webdriver.ChromeOptions()

    option.add_argument("–-disk-cache-dir=/Users/lanyu/Library/Application Support/Google/Chrome/Default/Service Worker/CacheStorage/")
    option.add_argument("--user-data-dir="+r"/Users/lanyu/Library/Application Support/Google/Chrome/")
    driver = webdriver.Chrome(chrome_options=option)   # 打开chrome浏览器
    print (driver.get("about:plugins"))
    driver.get('https://sun.io/#/sun')
    time.sleep(50000)
    # driver.quit()

if __name__=="__main__":
    main()
