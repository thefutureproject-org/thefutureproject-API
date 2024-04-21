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
            # -------------------Extracting Rank-------------------#
            rank = soup.find(
                'span', class_='profilePicSection_head_userRankContainer_rank__abngM')
            if rank:
                rank = rank.get_text()
                data['rank'] = rank

            # -------------------Extracting Streak-------------------#

            streak = soup.find(
                'div', class_='circularProgressBar_head_mid_streakCnt__MFOF1 tooltipped').text.strip().split('/')[0]
            data['streak'] = streak

            # -------------------Extracting Institution-------------------#

            Institution = soup.find(
                'div', class_='educationDetails_head_left--text__tgi9I')
            if Institution:
                Institution = Institution.text.strip()
                data['Institution'] = Institution

            # -------------------Extracting Languages-------------------#

            Languages = soup.find(
                'div', class_='educationDetails_head_right--text__lLOHI')
            if Languages:
                Languages = Languages.text.strip()
                data['Languages'] = Languages

            # -------------------Extracting Score Cards-------------------#

            score_card_divs = soup.find_all(
                'div', class_='scoreCard_head__nxXR8')
            if score_card_divs:
                for div in score_card_divs:
                    text_div = div.find(
                        'div', class_='scoreCard_head_card_left--text__hs9G4')
                    score_div = div.find(
                        'div', class_='scoreCard_head_card_left--score__pC6ZA')

                    if text_div and score_div:
                        text = text_div.text.strip()
                        score = score_div.text.strip()
                        data[text] = score

            # -------------------Extracting Solved Problems-------------------#

            difficulty_divs = soup.find_all(
                'div', class_='problemNavbar_head_nav__a4K6P')

            if difficulty_divs:
                for div in difficulty_divs:
                    text = div.find(
                        'div', class_='problemNavbar_head_nav--text__UaGCx').get_text()
                    difficulty, _, tags = text.partition('(')
                    difficulty = difficulty.strip()
                    tags = tags.split(')')[0].strip()
                    data[difficulty] = tags

            # ---------------------------------------------------------------#
            return data

        except AttributeError as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    else:
        get_user_data(username)
