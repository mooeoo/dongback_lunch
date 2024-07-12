import streamlit as st
import requests
import re
import xml.etree.ElementTree as ET
from datetime import date


def parse_xml_from_url():
    """
    XML 데이터를 URL에서 가져와 파싱하고 결과를 출력합니다.
    """

    # 오늘 날짜를 'YYYYMMDD' 형식의 문자열로 변환
    today_str = date.today().strftime('%Y%m%d')

    url = f"https://open.neis.go.kr/hub/mealServiceDietInfo?ATPT_OFCDC_SC_CODE=J10&SD_SCHUL_CODE=7530823&MLSV_YMD={today_str}"

    try:
        response = requests.get(url)

        if response.status_code == 200:
            tree = ET.ElementTree(ET.fromstring(response.content))

            root = tree.getroot()
            row = root.find("row")

            if row is not None:
                DDISH_NM_STR = row.find('DDISH_NM').text
                CAL_INFO = row.find('CAL_INFO').text
                NTR_INFO_STR = row.find('NTR_INFO').text

                DDISH_NM_LIST = DDISH_NM_STR.split("<br/>")
                NTR_INFO_LIST = NTR_INFO_STR.split("<br/>")

                st.title('오늘의 점심:')

                index = 0
                for TMP_DDISH_NM in DDISH_NM_LIST:
                    index += 1
                    st.success(f'{index}. {remove_numbers(TMP_DDISH_NM)}')

                st.info(f'총 칼로리: {CAL_INFO}')

                st.write('구성요소:')
                index = 0
                for TMP_NTR_INFO in NTR_INFO_LIST:
                    index += 1
                    st.text(f'{index}. {remove_numbers(TMP_NTR_INFO)}')
            else:
                st.write('오늘의 식단 정보를 찾을 수 없습니다.')
        else:
            st.write(f'Failed to retrieve data. Status code: {response.status_code}')
    except requests.exceptions.RequestException as e:
        st.write(f'Error fetching data: {e}')


def remove_numbers(text):
    pattern = r'\s*\(([\d.]+)\)'
    cleaned_str = re.sub(pattern, '', text)
    return cleaned_str


if __name__ == '__main__':
    st.title('급식 정보 조회')
    st.write('오늘의 급식 정보를 불러오려면 아래 버튼을 클릭하세요.')
    if st.button('급식 정보 불러오기'):
        parse_xml_from_url()
