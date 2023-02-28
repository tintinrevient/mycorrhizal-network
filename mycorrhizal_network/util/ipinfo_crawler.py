from dataclasses import dataclass

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@dataclass
class IPInfo(object):
    ip: str
    country: str
    region: str
    city: str
    isp: str
    org: str
    lat: str
    lon: str


def search_for_ipinfo(driver: WebDriver, ip: str) -> IPInfo:
    # Submit the wanted IP address
    search_form = driver.find_element(By.NAME, "lookup")
    ip_input = search_form.find_element(By.CSS_SELECTOR, "input")
    ip_input.send_keys(ip)
    ip_input.submit()

    # Find the geo-data results
    node_list = WebDriverWait(driver, 30).until(
        EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".geo-data"))
    )

    # Get the geo-data result ONLY via "ipinfo.io" which ranges from 8 till 15
    ip = node_list[8].find_element(By.CSS_SELECTOR, "span.ipinfo--ip").text
    country = node_list[9].find_element(By.CSS_SELECTOR, "span.ipinfo--country").text
    region = node_list[10].find_element(By.CSS_SELECTOR, "span.ipinfo--region").text
    city = node_list[11].find_element(By.CSS_SELECTOR, "span.ipinfo--city").text

    isp = node_list[12].find_element(By.CSS_SELECTOR, "span.ipinfo--isp").text
    org = node_list[13].find_element(By.CSS_SELECTOR, "span.ipinfo--org").text
    lat = node_list[14].find_element(By.CSS_SELECTOR, "span.ipinfo--lat").text
    lon = node_list[15].find_element(By.CSS_SELECTOR, "span.ipinfo--long").text

    return IPInfo(ip=ip, country=country, region=region, city=city, isp=isp, org=org, lat=lat, lon=lon)
