from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import amazon as am

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--log-level=3')

# windows
driver = webdriver.Chrome(options=chrome_options, executable_path='chromedriver.exe')

driver.get('https://www.amazon.com/gp/browse.html?node=11851273011&ref_=ods_gw_tpr_sd21_d_h1_xpl_ddp&pf_rd_r=9MKAX6SAY9R2ZW47ZZCK&pf_rd_p=de877882-d27e-4efc-8560-da3c0f2a82bf')

deal_title_elems = driver.find_elements_by_css_selector('#dealTitle > span')
deal_titles = []

for deal_title_elem in deal_title_elems:
    deal_titles.append(deal_title_elem.text)

price_elems = driver.find_elements_by_css_selector('.priceBlock > span')
prices = []

for price_elem in price_elems:
    prices.append(price_elem.text)

titles_with_prices = dict(zip(deal_titles, prices))

print(titles_with_prices)

amazon = am.Amazon()
# amazon.reset_database()

for key, value in titles_with_prices.items():
    amazon.add(key,value)

