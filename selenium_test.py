from selenium import webdriver
import sys

args = sys.argv
USER = "tai.tai.kinntyann.so@gmail.com"
PASS = args[1]
print(PASS)
# PhantomJSのドライバーを得る
browser = webdriver.PhantomJS()
browser.implicitly_wait(3)

# ログインページにアクセス
url_login = "https://1point02.jp/op/login.aspx"
browser.get(url_login)
print("ログインページにアクセスしました")

# テキストボックスに文字を入力
e = browser.find_element_by_id("edtID")
e.clear()
e.send_keys(USER)
e = browser.find_element_by_id("edtPass")
e.clear()
e.send_keys(PASS)
# フォームを送信
frm = browser.find_element_by_css_selector("#form1")
frm.submit()
print("情報を入力してログインボタンを押しました")

# マイページのURLを得る
#a = browser.find_element_by_css_selector(".islogin a")
url_mypage = "https://1point02.jp/op/index.aspx"
print("マイページのURL=", url_mypage)

# マイページを表示
browser.get(url_mypage)

# お気に入りのタイトルを列挙
links = browser.find_elements_by_css_selector(
    "#gv_WAR_BAT li > a")
for a in links:
    href = a.get_attribute('href')
    title = a.text
    print("-", title, ">", href)
