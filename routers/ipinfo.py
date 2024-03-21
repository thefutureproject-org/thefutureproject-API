import requests
from bs4 import BeautifulSoup as bs

from fastapi import APIRouter, HTTPException, status
import schemas
from config import settings


router = APIRouter(
    prefix="/ipinfo",
    tags=["IP Info"]
)


def get_ip_info(ip: str):
    url = f"https://scamalytics.com/ip/{ip}"
    response = requests.get(url=url, proxies=settings.PROXIES)
    soup = bs(response.text, 'lxml')
    ip_score_div = soup.find("div", {"class": "score"})
    if not ip_score_div:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find IP information"
        )

    ip_score = ip_score_div.text.split(":")[1].strip()
    risk = soup.find("div", {"class": "panel_title high_risk"}).text.split(" ")[
        0].strip()

    hostname = soup.find('th', string='Hostname').find_next_sibling(
        'td').text.strip()
    asn = soup.find('th', string='ASN').find_next_sibling('td').text.strip()
    isp_name = soup.find('th', string='ISP Name').find_next_sibling(
        'td').text.strip()
    organisation_name = soup.find(
        'th', string='Organization Name').find_next_sibling('td').text.strip()
    connection_type = soup.find(
        'th', string='Connection type').find_next_sibling('td').text.strip()

    country = soup.find('th', string='Country Name').find_next_sibling(
        'td').text.strip()
    country_code = soup.find(
        'th', string='Country Code').find_next_sibling('td').text.strip()
    state = soup.find('th', string='State / Province').find_next_sibling(
        'td').text.strip()
    district = soup.find(
        'th', string='District / County').find_next_sibling('td').text.strip()
    city = soup.find(
        'th', string='City').find_next_sibling('td').text.strip()
    postal_code = soup.find(
        'th', string='Postal Code').find_next_sibling('td').text.strip()
    latitude = soup.find('th', string='Latitude').find_next_sibling(
        'td').text.strip()
    longitude = soup.find(
        'th', string='Longitude').find_next_sibling('td').text.strip()

    tor_exit_node = soup.find(
        'th', string='Tor Exit Node').find_next_sibling('td').text.strip()
    server = soup.find(
        'th', string='Server').find_next_sibling('td').text.strip()
    public_proxy = soup.find(
        'th', string='Public Proxy').find_next_sibling('td').text.strip()
    web_proxy = soup.find(
        'th', string='Web Proxy').find_next_sibling('td').text.strip()
    search_engine_robot = soup.find(
        'th', string='Search Engine Robot').find_next_sibling('td').text.strip()

    result = {
        "ip": ip,
        "Fraud Risk": {
            "score": ip_score,
            "risk": risk
        },
        "Operator": {
            "Hostname": hostname,
            "ASN": asn,
            "ISP Name": isp_name,
            "Organization Name": organisation_name,
            "Connection type": connection_type
        },
        "Location": {
            "Country Name": country,
            "Country Code": country_code,
            "State / Province": state,
            "District / County": district,
            "City": city,
            "Postal Code": postal_code,
            "Latitude": latitude,
            "Longitude": longitude
        },
        "Proxies": {
            "Tor Exit Node": tor_exit_node,
            "Server": server,
            "Public Proxy": public_proxy,
            "Web Proxy": web_proxy,
            "Search Engine Robot": search_engine_robot
        }
    }
    return result


@router.post("/", status_code=200, summary="Get information about an IP")
async def get_ip_info_route(ip: schemas.Ip_Info_In):
    return get_ip_info(ip.ip)
