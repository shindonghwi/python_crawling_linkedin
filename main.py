import io
import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup as Soup
import re
from datetime import datetime
from typing import IO
import math


class LinkedIn:
    __file: IO[io.FileIO]

    __email = 'nma1256@ruu.kr'
    __pw = 'test01!@'

    # 살아있는 계정
    """ 비번은 test01!@
        
        nma1256@ruu.kr
        sdsdsddd@naver.com
        cqvzx18@ruu.kr
    """

    __company_list = [
        # --- 수집완료
        # ["Tokyo Gas", "tokyo-gas-asia-pte-ltd"],
        # ["Osaka Gas USA", "osaka-gas-energy-america"],
        # ["PlugPower", "plug-power"]
        # ["Green Plains", "green-plains-inc"],
        # ["VerBio", "verbio"],
        # ["Blink Charging", "blinkcharging"],
        # ["Shell", "shell"],
        # ["Total Energies", "totalenergies"],
        # ["Volta", "voltalia"],
        # ["Waste Connections", "waste-connections-inc-"],
        # ["Cleanaway", "cleanawayau"],
        # ["NextEra Energy", "nextera-energy-resources"],
        # ["ChargePoint", "chargepoint"],
        # ["NEL", "nel-hydrogen"],
        # ["ACS", "american-chemical-society"],
        # ["Iberdrola", "iberdrola"],
        # ["STRABAG", "strabag"],
        # ["VINCI", "vinci"],
        # ["Veolia", "veolia-environnement"],
        # ["Henkel", "henkel"],
        # ["CATL", "contemporary-amperex-technology-gmbh"],
        # ["Celanese", "celanese"],
        # ["ITM Power", "itm-power"],
        # ["Ceres Power Holdings PLC", "ceres-power"],
        # ["Valero", "valero-energy"],
        # ["HOCHTIEF", "hochtief"],
        # ["acciona", "acciona"],
        # ["BASF", "basf"],
        # ["Orsted", "orsted"],
        # ["EDP Renewables", "edp-renov-veis"],
        # ["RWE", "rwe-"],
        # ["Stem", "stem-inc"],
        # ["Siemens Gamesa", "siemensgamesa"],
        # ["WSP", "wsp"],
        # ["SKANSKA", "skanska"],
        # ["Republic Services", "republic-services-inc"],
        # ["DSM", "dsm"],
        # ["Waste Management", "waste-management"],
        # ["HF Sinclair(HollyFrontier Sinclair)", "hf-sinclair"],
        # ["Neste", "neste"],

        # --- 진행중
        ["Jacobs", "jacobs"],

    ]

    def __init__(self):
        self.__path = 'https://www.linkedin.com/'
        options = webdriver.ChromeOptions()
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        # options.add_argument("user-agent=Mozilla/5.0 (Linux; Android 9; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.83 Mobile Safari/537.36")
        self.__driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        self.__driver.get(self.__path)

        time.sleep(2)
        self.__process_login()
        self.__search_keyword()

    def __process_login(self):
        xpath_id = '//*[@id="session_key"]'
        xpath_pw = '//*[@id="session_password"]'
        xpath_login_button = '//*[@id="main-content"]/section[1]/div/div/form/button'
        self.__find_xpath_and_input(xpath_id, self.__email, "아이디 입력")
        self.__find_xpath_and_input(xpath_pw, self.__pw, "패스워드 입력")
        self.__find_xpath(xpath_login_button, "로그인 버튼")
        input()  # 감지 봇 때문에 직접 감지 봇 문제 풀고 이어서 진행

    def __search_keyword(self):
        for company_data in self.__company_list:

            print('start company : ', company_data)

            file_path = "save_folder/{}.txt".format("{}".format(company_data[0]))
            try:

                from os import path
                if path.exists(file_path):
                    self.__file = open(file_path, 'r+', encoding='utf-8')
                    success_index = len(self.__file.readlines())
                else:
                    self.__file = open(file_path, 'w', encoding='utf-8')
                    success_index = 0

                # # 회사 - people 정보 리스트 페이지로 이동 후에, html 정보를 가져온다.
                # self.__move_page_company_people(company_data=company_data)
                #
                # # 총 페이지 정보 추출
                # people_list_page_html = self.__get_current_html()
                # total_page = self.__extract_page_info(html=people_list_page_html)

                # 회원의 href 정보 추출

                f = open("save_folder/href/{}_href.txt".format(
                    "{}".format(company_data[0])), 'r', encoding='utf-8')
                h_list = []
                for idx, link in enumerate(f.readlines()):
                    if idx >= success_index:
                        h_list.append(link)
                person_href_list = h_list
                f.close()

                # person_href_list = self.__get_href_from_item_list(
                #     html=people_list_page_html,
                #     total_page=total_page,
                #     filename="save_folder/href/{}_href.txt".format(
                #         "{}".format(company_data[0]))
                # )

                print('{} 회사 총 {}명'.format(company_data[0], len(person_href_list)))

                if len(person_href_list) != 0:
                    for idx, link in enumerate(person_href_list):
                        print('{} 회사 - {}/{} 진행중 -- {}'.format(company_data[0], str(idx + 1),
                                                         len(person_href_list), self.__email))
                        collect_data = {
                            'name': None,
                            'region': None,
                            'company': company_data[0],
                            'profile_url': link,
                            'experience': None,
                            'skills': []
                        }

                        # 사람의 상세페이지로 이동하고, html 정보 가져오기
                        self.__move_page_company_people_detail(link)
                        time.sleep(1.5)
                        person_detail_html = self.__get_current_html().find("main", id="main")

                        # section 프로필 수집
                        section_profile = self.__get_section_profile_from_detail_page(
                            html=person_detail_html)
                        self.__extract_people_name_region_data(
                            data=collect_data,
                            html=section_profile
                        )

                        # section list 스킬, 학력 경험 등
                        section_list = self.__get_section_list_from_detail_page(
                            html=person_detail_html)

                        profile_url = self.__driver.current_url
                        for index, section in enumerate(section_list):
                            # 직무 타이틀, 기간 수집
                            if section.find('div', id='experience') is not None:
                                self.__extract_people_experience_data(
                                    data=collect_data,
                                    url=profile_url + "details/experience"
                                )
                                time.sleep(2)

                            # 스킬 데이터 수집
                            if section.find('div', id='skills') is not None:
                                self.__extract_people_skills_data(
                                    data=collect_data,
                                    url=profile_url + "details/skills"
                                )
                                time.sleep(2)

                        print(json.dumps(collect_data, ensure_ascii=False))
                        self.__file.write(json.dumps(collect_data, ensure_ascii=False))
                        self.__file.write("\n")
                        self.__driver.back()
                        self.__driver.back()
                        time.sleep(1)
            finally:
                self.__file.close()

    def __move_page_company_people(self, company_data):
        """ 회사 회워 리스트 페이지로 이동 """
        company_path = 'https://www.linkedin.com/company/{}/people/'.format(company_data[1])
        self.__driver.get(company_path)
        time.sleep(12)
        people_page_href = self.__get_current_html() \
            .find('main', id='main') \
            .find('div', 'mt1')

        if people_page_href.find('a', 'ember-view org-top-card-secondary-content__see-all-link'):
            people_page_href = people_page_href \
                .find(
                'a',
                'ember-view org-top-card-secondary-content__see-all-link'
            )['href']
        else:
            people_page_href = people_page_href.find('a')['href']

        self.__driver.get('https://www.linkedin.com{}'.format(people_page_href))
        time.sleep(12)

    def __move_page_company_people_detail(self, link):
        """ 회원 상세 페이지로 이동 """
        self.__driver.get(link)

    def __move_page_company_people_skills_detail(self, link):
        """ 회원 스킬 상세 페이지로 이동 """
        self.__driver.get(link)
        time.sleep(14)

    def __move_page_company_people_experience_detail(self, link):
        """ 회원 경력 상세 페이지로 이동 """
        self.__driver.get(link)
        time.sleep(10)

    def __get_current_html(self):
        """ 현재 페이지의 Html 코드를 가져오기 """
        return Soup(self.__driver.page_source, "lxml")

    def __get_section_list_from_detail_page(self, html):
        """ 회원 상세 페이지의 section list 를  가져오기 """
        return html.find_all(
            "section",
            'artdeco-card ember-view relative break-words pb3 mt2'
        )

    def __get_section_profile_from_detail_page(self, html):
        """ 회원 상세 페이지의 section list 를  가져오기 """
        return html.find(
            "section",
            'artdeco-card ember-view pv-top-card'
        )

    def __regex_number(self, msg: str):
        """ 숫자만 추출하는 정규식 """
        return re.sub(r'[^0-9]', '', msg)

    def __extract_page_info(self, html):
        """ 페이지 정보 추출 """
        total_people_count_text = html \
            .find('div', 'search-results-container') \
            .find('div').text
        total_people_count = self.__regex_number(total_people_count_text)
        total_people_page_rest = int(total_people_count) % 10
        total_people_page = int(total_people_count) / 10
        if total_people_page_rest != 0:
            total_people_page += 1
        if total_people_page >= 100:
            total_people_page = 100
        total_people_page = math.ceil(total_people_page)
        return total_people_page

    def __extract_people_name_region_data(self, data: dict, html):
        name = html.find('h1').text
        region = html.find('div', 'pv-text-details__left-panel mt2').find('span').text
        data['name'] = name.strip()
        data['region'] = region.strip()

    def __extract_people_experience_data(self, data: dict, url: str):
        self.__move_page_company_people_experience_detail(url)
        self.__scroll_down(5)
        experience_detail_page_html = self.__get_current_html()
        content_html = experience_detail_page_html.find('main', id='main') \
            .find('section') \
            .find('div', 'pvs-list__container')

        experience_content_list = content_html \
            .find("ul", "pvs-list") \
            .find_all(
            "li", "pvs-list__paged-list-item artdeco-list__item pvs-list__item--line-separated"
        )

        experience_res = {
            'current': [],
            'company_career': []
        }

        for index, item in enumerate(experience_content_list):
            company_career_res = {
                'name': None,
                'period': None,
            }

            # 회사 다녔던 리스트
            company_item_html = item \
                .find('div', 'display-flex flex-column full-width align-self-center') \
                .find('div', 'display-flex align-items-center')

            if company_item_html.find('span', 'mr1 hoverable-link-text t-bold') is not None:
                company = company_item_html \
                    .find('span', 'mr1 hoverable-link-text t-bold').find('span').text
            else:
                company = company_item_html \
                    .find('span', 'mr1 t-bold').find('span').text

            company_period = item \
                .find('div', 'display-flex flex-column full-width align-self-center')

            if company_period.find('span', 't-14 t-normal t-black--light') is not None:
                company_period = company_period \
                    .find('span', 't-14 t-normal t-black--light') \
                    .find('span').text
            else:
                company_period = company_period \
                    .find('span', 'mr1 t-bold') \
                    .find('span').text

            company_career_res['name'] = company

            if 'mos' or 'yr' in company_period:
                company_career_res['period'] = company_period
            else:
                company_career_res['period'] = 'None'

            experience_res['company_career'].append(company_career_res)

            # 최근 회사 찾기 ~ Present
            if item.find('ul', 'pvs-list'):
                career_html = item.find('ul', 'pvs-list')

                if career_html.find('ul', 'pvs-list'):
                    career_html = career_html.find('ul', 'pvs-list')
                career_html = career_html.find_all('li', 'pvs-list__paged-list-item')

            else:
                career_html = experience_content_list

            for career in career_html:
                job_res = {
                    'company': company,
                    'job_title': None,
                    'period': None,
                    'isPresent': None,
                }

                if career.find('span', 'mr1 hoverable-link-text t-bold'):
                    job = career.find('span', 'mr1 hoverable-link-text t-bold').find('span').text
                else:
                    job = career.find('span', 'mr1 t-bold').find('span').text

                try:
                    period = career.find('span', 't-14 t-normal t-black--light')
                    if 'mos' or 'yr' in period.find('span').text:
                        period = period.find('span').text
                    else:
                        period = 'None'
                except:
                    period = 'None'

                job_res['job_title'] = job
                job_res['period'] = period

                if 'Present' in period:
                    job_res['isPresent'] = True
                else:
                    job_res['isPresent'] = False
                experience_res['current'].append(job_res)
            data['experience'] = experience_res

    def __extract_people_skills_data(self, data: dict, url: str):
        self.__move_page_company_people_skills_detail(url)
        self.__scroll_down(5)
        skills_detail_page_html = self.__get_current_html()

        content_html = skills_detail_page_html.find('main', id='main') \
            .find('section') \
            .find('div', 'pvs-list__container')

        skill_content_list = content_html \
            .find("ul", "pvs-list") \
            .find_all(
            "li", "pvs-list__paged-list-item artdeco-list__item pvs-list__item--line-separated"
        )

        for item in skill_content_list:

            skill_res = {
                'name': None,
                'recommended_count': None
            }

            if item.find('div', "pv2") is not None:
                item_detail = item.find('div', "pv2").find('a')['href']
                self.__driver.execute_script('window.open("' + str(item_detail) + '");')
                self.__driver.switch_to.window(self.__driver.window_handles[-1])

                modal_html = self.__get_current_html()
                skill_name = modal_html.find('h1', id='profile-modal').text
                count = modal_html.find('div', id='artdeco-modal-outlet') \
                    .find('div', 'pvs-list__container') \
                    .find('ul') \
                    .find_all('li', 'pvs-list__paged-list-item')[-1] \
                    .find('span').text
                skill_res['name'] = skill_name
                skill_res['recommended_count'] = self.__regex_number(count)
                self.__driver.close()
                self.__driver.switch_to.window(self.__driver.window_handles[-1])
            else:
                skill_name = item \
                    .find('div', 'display-flex flex-column full-width align-self-center') \
                    .find('div', 'display-flex align-items-center') \
                    .find("span", "mr1 hoverable-link-text t-bold") \
                    .find("span").text.strip()

                if item.find(
                        "div",
                        "hoverable-link-text display-flex align-items-center t-14 t-normal t-black"
                ) is not None:
                    count = item \
                        .find(
                        "div",
                        "hoverable-link-text display-flex align-items-center t-14 t-normal t-black"
                    ).find("span").text
                else:
                    count = "0"

                skill_res['name'] = skill_name
                skill_res['recommended_count'] = self.__regex_number(count)
            data['skills'].append(skill_res)

    def __get_href_from_item_list(self, html, total_page, filename):
        access_person_href_list = []
        file = open(filename, 'w', encoding='utf-8')
        for page_index in range(1, total_page + 1):
            if page_index > 1:
                next_page = self.__driver.current_url.split("&page")[0] + "&page=" + str(page_index)
                self.__driver.get(next_page)
                time.sleep(12)
                current_page_html = self.__get_current_html()
            else:
                current_page_html = html

            item_list = current_page_html \
                .find_all("li", "reusable-search__result-container")  # 한 페이지 - 최대 10개

            for index, item in enumerate(item_list):
                a_html = item.find('div', 't-roman t-sans').find('a', 'app-aware-link')

                if a_html.text.strip() != "LinkedIn Member":
                    print(a_html['href'])
                    access_person_href_list.append(a_html['href'])
                    file.write(a_html['href'])
                    file.write("\n")
                    file.flush()
        file.close()
        return access_person_href_list

    def __find_xpath(self, xpath: str, err_msg: str):
        try:
            WebDriverWait(self.__driver, 10).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            ).click()
            time.sleep(0.2)
        except Exception as e:
            print(err_msg, e)
            self.__driver.quit()

    def __find_xpath_and_input(self, xpath: str, value: str, err_msg: str):
        try:
            WebDriverWait(self.__driver, 10).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            ).send_keys(value)
            time.sleep(0.2)
        except Exception as e:
            print(err_msg, " : ", e)
            self.__driver.quit()

    def __create_new_text_file(self, filename: str):
        self.__file = open(filename, 'a', encoding='utf-8')

    def __scroll_down(self, count):
        # 스크롤 높이 가져옴
        last_height = self.__driver.execute_script("return document.body.scrollHeight")

        for i in range(0, count):
            # 끝까지 스크롤 다운
            self.__driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # 1초 대기
            time.sleep(0.5)

            # 스크롤 다운 후 스크롤 높이 다시 가져옴
            new_height = self.__driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height


if __name__ == '__main__':
    LinkedIn()
