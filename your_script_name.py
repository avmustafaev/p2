from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

class AvitoParser:
    def __init__(self):
        self.driver = self._setup_driver()
        self.price_value = None
        self.full_address = None
        self.rooms = None
        self.total_area = None
        self.floor = None

    def _setup_driver(self):
        firefox_options = Options()
        firefox_options.add_argument("--headless")
        firefox_options.add_argument("--disable-gpu")
        firefox_options.add_argument("--blink-settings=imagesEnabled=false")
        firefox_options.add_argument("--disable-extensions")
        firefox_options.add_argument("--disable-dev-shm-usage")
        firefox_options.add_argument("--no-sandbox")
        firefox_options.add_argument("--disable-setuid-sandbox")
        firefox_options.add_argument("--disable-background-networking")
        firefox_options.add_argument("--disable-background-timer-throttling")
        firefox_options.add_argument("--disable-backgrounding-occluded-windows")
        firefox_options.add_argument("--disable-breakpad")
        firefox_options.add_argument("--disable-client-side-phishing-detection")
        firefox_options.add_argument("--disable-component-update")
        firefox_options.add_argument("--disable-default-apps")
        firefox_options.add_argument("--disable-domain-reliability")
        firefox_options.add_argument("--disable-features=AudioServiceOutOfProcess")
        firefox_options.add_argument("--disable-hang-monitor")
        firefox_options.add_argument("--disable-ipc-flooding-protection")
        firefox_options.add_argument("--disable-popup-blocking")
        firefox_options.add_argument("--disable-prompt-on-repost")
        firefox_options.add_argument("--disable-renderer-backgrounding")
        firefox_options.add_argument("--disable-sync")
        firefox_options.add_argument("--force-color-profile=srgb")
        firefox_options.add_argument("--metrics-recording-only")
        firefox_options.add_argument("--no-first-run")
        firefox_options.add_argument("--safebrowsing-disable-auto-update")
        firefox_options.add_argument("--enable-automation")
        firefox_options.add_argument("--password-store=basic")
        firefox_options.add_argument("--use-mock-keychain")

        prefs = {
            "profile.managed_default_content_settings.images": 2,
            "profile.managed_default_content_settings.javascript": 2,
        }
        firefox_options.set_preference("profile.managed_default_content_settings.images", 2)
        firefox_options.set_preference("profile.managed_default_content_settings.javascript", 2)

        return webdriver.Firefox(options=firefox_options)

    def _extract_param(self, params_soup, param_name):
        for li in params_soup.find_all('li', class_='params-paramsList__item-_2Y2O'):
            span = li.find('span', class_='styles-module-noAccent-l9CMS')
            if span and param_name in span.text:
                return span.next_sibling.strip()
        return "Не указано"

    def parse(self, url):
        self.driver.get(url)

        wait = WebDriverWait(self.driver, 10)
        price_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "span[itemprop='price']")))

        page_source = self.driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

        price_span = soup.find('span', {'itemprop': 'price'})
        self.price_value = price_span.get('content', 'Не указано') if price_span else 'Не указано'

        params_block = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-marker='item-view/item-params']")))
        params_html = params_block.get_attribute('innerHTML')
        params_soup = BeautifulSoup(params_html, 'html.parser')

        self.rooms = self._extract_param(params_soup, "Количество комнат")
        self.total_area = self._extract_param(params_soup, "Общая площадь")
        self.floor = self._extract_param(params_soup, "Этаж")

        self.total_area = self.total_area.replace("\u00A0м\u00B2", "").replace(" м\u00B2", "")
        self.floor = self.floor.replace(" из ", "/")

        address_element = self.driver.find_element(By.CSS_SELECTOR, "span.style-item-address__string-wt61A")
        self.full_address = address_element.text.strip()

    def close(self):
        self.driver.quit()

if __name__ == "__main__":
    url = 'https://www.avito.ru/ekaterinburg/kvartiry/1-k._kvartira_406_m_69_et._4574477371?context=H4sIAAAAAAAA_wEmANn_YToxOntzOjE6IngiO3M6MTY6Ik9Ra1c5RzE3TUY5c0R2NW8iO32sRl6AJgAAAA'
    parser = AvitoParser()
    parser.parse(url)
    print(f"📍 {parser.full_address}")
    print(f"💵 {parser.price_value}₽")
    print('')
    print(f"🚪 {parser.rooms}комн.")
    print(f"📐 {parser.total_area}м²")
    print(f"🪜 {parser.floor}")
    parser.close()