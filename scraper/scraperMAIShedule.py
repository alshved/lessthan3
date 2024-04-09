import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.common.by import By
import json
from os import path


class SheduleScraperMAI:
    """Класс для скраппинга сайта маи с расписанием"""

    def __init__(self, url: str, cache_dir=''):
        """
        Параметры:
        :param str url: адрес сайта маи с расписанием
        :param str cache_dir: директория для кэширования
        """

        self.url = url
        self.cache_dir = cache_dir
        self._driver = webdriver.Chrome()

    def __go_to_week_page(self, inst: int, group: str, week: str):
        driver = self._driver
        required_inst = inst
        required_group = group
        required_week = week
        driver.get(self.url)
        btn_institute = driver.find_element(By.ID, "department")
        btn_institute.send_keys(f"Институт №{str(required_inst)}")
        btn_course = driver.find_element(By.ID, "course")
        btn_course.send_keys("1")
        btn_submit = driver.find_element(By.ID, "student")
        btn_submit = btn_submit.find_element(By.TAG_NAME, "button")
        btn_submit.submit()
        groups = driver.find_element(By.ID, "nav-1-eg1")
        g = groups.find_elements(By.TAG_NAME, "a")
        for i in g:
            if i.text == required_group:
                i.send_keys("\n")
                break
        driver.get(driver.current_url + "&week=1")
        choose_week_btn = driver.find_element(By.CSS_SELECTOR,
                                              '.btn.btn-sm.btn-outline-primary.me-2.mb-2.w-100.w-sm-auto.text-center + '
                                              '.btn.btn-sm.btn-outline-primary.me-2.mb-2.w-100.w-sm-auto.text-center')

        choose_week_btn.send_keys('\n')
        weeks_elements_container = driver.find_element(By.CSS_SELECTOR, ".list-group.list-group-striped.list-group-sm")
        weeks_elements = weeks_elements_container.find_elements(By.CSS_SELECTOR, "li")
        weeks_identificators = dict()
        for i in weeks_elements:
            week_id = i.find_element(By.CSS_SELECTOR, ":last-child").text.replace(' ', '')
            weeks_identificators[week_id] = i

        req_week_btn = weeks_identificators[required_week].find_elements(By.TAG_NAME, "a")

        if req_week_btn:
            req_week_btn[0].send_keys('\n')

    def scrap_by_group_and_week(self, inst: int, group: str, week: str, try_cache=True):
        """
        Скрапит информацию с сайта
        :param int inst: Номер института
        :param str group: Название группы полностью
        :param str week: Неделя в формате ДД.ММ.ГГ-ДД.ММ.ГГ
        :param try_cache: Если True, то будет предпринята попытка загрузить данные из кэша, иначе будет скрапить с нуля.
        По умолчанию True
        """

        data_path = path.join(self.cache_dir, f'{inst}i{group}g{week}w.json')
        if try_cache and path.exists(data_path):
            with open(data_path, 'r', encoding='utf-8') as fp:
                res = json.load(fp)
            return res
        else:
            driver = self._driver
            driver.get(self.url)
            self.__go_to_week_page(group=group, week=week, inst=inst)
            res = dict()
            days_elements = driver.find_elements(By.CLASS_NAME, "step-content")
            for day_ind in range(len(days_elements)):
                lessons_elements = days_elements[day_ind].find_elements(By.CSS_SELECTOR, ".mb-4")
                lessons = []
                for i in range(len(lessons_elements)):
                    subject_name_element = None
                    lesson_info_element = None
                    try:
                        subject_name_element = lessons_elements[i].find_element(By.TAG_NAME, "div")
                        lesson_info_element = lessons_elements[i].find_element(By.TAG_NAME, "ul")
                    except selenium.common.exceptions.NoSuchElementException:
                        pass
                    if subject_name_element and lesson_info_element:
                        cur = dict()
                        sub_info = subject_name_element.text.split()
                        cur['subject'] = " ".join(sub_info[:len(sub_info) - 1])
                        cur['subject_type'] = sub_info[-1]

                        lesson_info = lesson_info_element.find_elements(By.TAG_NAME, "li")
                        time = lesson_info[0].text.replace(' ', '').split('–')
                        cur['time_start'] = time[0]
                        cur['time_end'] = time[1]
                        cur['teachers'] = []
                        for ind in range(1, len(lesson_info) - 1):
                            cur['teachers'].append(lesson_info[ind].text)

                        cur["cabinet"] = lesson_info[-1].text
                        lessons.append(cur)
                date_info = days_elements[day_ind].find_element(By.TAG_NAME, "span").text.replace(',', '').split(' ')
                week_day = date_info[0]
                date = date_info[1] + date_info[2]
                res[week_day] = dict({'lessons': lessons, 'date': date})

            with open(data_path, 'w', encoding='utf-8') as fp:
                json.dump(res, fp, ensure_ascii=False, indent=2)
            return res


s = SheduleScraperMAI("https://mai.ru/education/studies/schedule/")
s.scrap_by_group_and_week(8, 'М8О-110Б-23', '08.04.2024-14.04.2024', try_cache=False)
