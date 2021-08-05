from selenium import webdriver;
import sys;
import time
import chromedriver_binary

# ChromeOptionsを設定

args = sys.argv
USER = "tai.tai.kinntyann.so@gmail.com"
PASS = args[1]
print(PASS)

# ドライバーを得る
# ChromeOptionsを設定
options = webdriver.ChromeOptions();
options.add_argument('--disable-gpu');
options.add_argument('--disable-extensions')
#options.add_argument('--proxy-server="direct://"')
#options.add_argument('--proxy-bypass-list=*')
#options.add_argument('--start-maximized')
#options.add_argument('--kiosk')
#options.add_argument('--headless');
driver = webdriver.Chrome(options=options)

# ログインページにアクセス
url_login = "https://1point02.jp/op/login.aspx"
driver.get(url_login)
print("ログインページにアクセスしました")

# テキストボックスに文字を入力
id = driver.find_element_by_id("edtID")
id.send_keys(USER)
password = driver.find_element_by_id("edtPass")
password.send_keys(PASS)
# フォームを送信
frm = driver.find_element_by_css_selector("#form1")

login_button = driver.find_element_by_id("lbnLogin")
login_button.click()

print("情報を入力してログインボタンを押しました")

# マイページのURLを得る
url_mypage = "https://1point02.jp/op/index.aspx"
print("マイページのURL=", url_mypage)

# マイページを表示
driver.get(url_mypage)

