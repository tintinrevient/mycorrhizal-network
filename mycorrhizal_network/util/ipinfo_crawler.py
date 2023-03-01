from dataclasses import dataclass

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@dataclass
class IPInfo(object):
    ip: str
    country: str = None
    region: str = None
    city: str = None
    isp: str = None
    org: str = None
    lat: str = None
    lon: str = None
    hostname: str = None
    asn: str = None
    services: str = None
    assignment: str = None


def search_for_iplocation(driver: WebDriver, ip: str) -> IPInfo:
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
    info = IPInfo(ip=ip)

    info.country = node_list[9].find_element(By.CSS_SELECTOR, "span.ipinfo--country").text
    info.region = node_list[10].find_element(By.CSS_SELECTOR, "span.ipinfo--region").text
    info.city = node_list[11].find_element(By.CSS_SELECTOR, "span.ipinfo--city").text

    info.isp = node_list[12].find_element(By.CSS_SELECTOR, "span.ipinfo--isp").text
    info.org = node_list[13].find_element(By.CSS_SELECTOR, "span.ipinfo--org").text
    info.lat = node_list[14].find_element(By.CSS_SELECTOR, "span.ipinfo--lat").text
    info.lon = node_list[15].find_element(By.CSS_SELECTOR, "span.ipinfo--long").text

    return info


def search_for_myipaddress(driver: WebDriver, ip: str) -> IPInfo:
    print(f"search for {ip}...")
    # Submit the wanted IP address
    search_form = driver.find_element(By.CSS_SELECTOR, ".search-form.inline-form")
    ip_input = search_form.find_element(By.CSS_SELECTOR, "input")
    ip_input.send_keys(ip)
    ip_input.submit()

    # Find the geo-data results
    node_list = WebDriverWait(driver, 30).until(
        EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".information"))
    )

    # Get the geo-data result
    info = IPInfo(ip=ip)

    for node in node_list:
        key = node.find_element(By.CSS_SELECTOR, "span").text

        if key == "Hostname:":
            info.hostname = node.find_element(By.CSS_SELECTOR, "span:nth-child(2)").text
        elif key == "ISP:":
            info.isp = node.find_element(By.CSS_SELECTOR, "span:nth-child(2)").text
        elif key == "ASN:":
            info.asn = node.find_element(By.CSS_SELECTOR, "span:nth-child(2)").text
        elif key == "Services:":
            info.services = node.find_element(By.CSS_SELECTOR, "span:nth-child(2)").text
        elif key == "Assignment:":
            info.assignment = node.find_element(By.CSS_SELECTOR, "span:nth-child(2)").text
        elif key == "Country:":
            info.country = node.find_element(By.CSS_SELECTOR, "span:nth-child(2)").text
        elif key == "State/Region:":
            info.region = node.find_element(By.CSS_SELECTOR, "span:nth-child(2)").text
        elif key == "City:":
            info.city = node.find_element(By.CSS_SELECTOR, "span:nth-child(2)").text
        elif key == "Latitude:":
            info.lat = node.find_element(By.CSS_SELECTOR, "span:nth-child(2)").text
        elif key == "Longitude:":
            info.lon = node.find_element(By.CSS_SELECTOR, "span:nth-child(2)").text

    return info
