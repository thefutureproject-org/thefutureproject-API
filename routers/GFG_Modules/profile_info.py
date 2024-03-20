import requests
from bs4 import BeautifulSoup
from fastapi import HTTPException, status
from config import settings


def get_user_data(username: str):
    response = requests.get(
        url=f"https://auth.geeksforgeeks.org/user/{username}/", proxies=settings.PROXIES)

    if response.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if response.status_code == 200:
        try:
            data = {"username": username}
            soup = BeautifulSoup(response.text, 'lxml')
            rank = soup.find('span', class_='rankNum')
            if rank:
                rank = rank.get_text()
                data['rank'] = rank
            details = soup.find('div', class_='row basic_details')
            for detail in details:
                if detail == "\n":
                    continue
                detail_name = detail.find(
                    'div', class_='basic_details_name').text.strip()

                detail_data = detail.find(
                    'div', class_='basic_details_data').text.strip()
                data[detail_name] = detail_data

            score_cards = soup.find_all('div', class_='score_card_left')
            for card in score_cards:
                score_name = card.find(
                    'span', class_='score_card_name').get_text(strip=True)
                score_value = card.find(
                    'span', class_='score_card_value').get_text(strip=True)
                data[score_name] = score_value

            solved_problems = soup.find(
                'ul', class_='tabs tabs-fixed-width linksTypeProblem').find_all('li', class_='tab')
            for tab_element in solved_problems:
                category_text = tab_element.text.strip()
                category, count = category_text.split(' (')
                count = int(count[:-1])
                data[category] = count
            streak = soup.find(
                'div', class_='streakCnt tooltipped').text.strip().split()[0]
            data['streak'] = streak

            return data

        except AttributeError as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    else:
        get_user_data(username)
