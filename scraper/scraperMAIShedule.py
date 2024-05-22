import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.common.by import By
import json
from os import path
from selenium.common.exceptions import NoSuchElementException
import datetime


class SheduleScraperMAI:
    """Класс для скраппинга сайта маи с расписанием"""

    def __init__(self, url: str, cache_dir=''):
        """
        Параметры:
        :param str url: адрес сайта маи с расписанием
        :param str cache_dir: директория для кэширования
        """
        self.url = url
        if cache_dir is None:
            self.cache_dir = ''
        else:
            self.cache_dir = cache_dir
        self._driver = webdriver.Chrome()

    def __go_to_groups_page__(self, course: str, inst: str):
        """
        Переходит на страницу с всеми группами указанного курса и института
        :param inst: институт
        :param course: курс
        :return:
        """

        driver = self._driver
        driver.get(self.url)
        btn_institute = driver.find_element(By.ID, 'department')
        btn_institute.send_keys(f'Институт №{inst}')
        btn_course = driver.find_element(By.ID, 'course')
        btn_course.send_keys(course)
        btn_submit = driver.find_element(By.ID, 'student')
        btn_submit = btn_submit.find_element(By.TAG_NAME, 'button')
        btn_submit.submit()

    def __go_to_week_page(self, required_inst: str, required_course: str, required_group: str, required_week=''):
        """
        Переход на страницу с расписанием соответствующей недели.
        Если неделя не указана, перейдет на самую первую неделю в семестре.
        :param required_inst: номер института
        :param required_group: номер группы
        :param required_week: неделя в формате ДД.ММ.ГГ-ДД.ММ.ГГ
        """
        self.__go_to_groups_page__(required_course, required_inst)
        driver = self._driver
        groups_elements = driver.find_element(By.ID, 'nav-1-eg1')
        groups = groups_elements.find_elements(By.TAG_NAME, 'a')
        for element in groups:
            if element.text == required_group:
                element.send_keys('\n')
                break
        driver.get(driver.current_url + '&week=1')
        choose_week_btn = driver.find_element(By.CSS_SELECTOR,
                                              '.btn.btn-sm.btn-outline-primary.me-2.mb-2.w-100'
                                              '.w-sm-auto.text-center[href="#collapseWeeks"]')
        choose_week_btn.send_keys('\n')
        weeks_elements_container = driver.find_element(By.CSS_SELECTOR, '.list-group.list-group-striped.list-group-sm')
        weeks_els = weeks_elements_container.find_elements(By.CSS_SELECTOR, 'li')

        weeks_identificators = dict()
        for i in range(len(weeks_els)):
            week_id = weeks_els[i].find_element(By.CSS_SELECTOR, ':last-child').text.replace(' ', '')
            weeks_identificators[week_id] = weeks_els[i]
            weeks_identificators[str(i + 1)] = weeks_els[i]

        if required_week:
            req_week_btn = weeks_identificators[required_week].find_elements(By.TAG_NAME, 'a')
        else:
            req_week_btn = None

        if req_week_btn:
            req_week_btn[0].send_keys('\n')

    def scrap_by_group_and_week(self, inst: str, course: str, group: str, week: str, try_cache=True, subject=None):
        """
        Скрапит информацию с сайта
        :param subject: предмет
        :param int inst: номер института
        :param str group: название группы полностью
        :param str week: неделя в формате ДД.ММ.ГГ-ДД.ММ.ГГ или номер недели
        :param try_cache: если True, то будет предпринята попытка загрузить данные из кэша, иначе будет скрапить с нуля
        :param course: номер курса
        :return: словарь, состоящий из расписания на конкретную неделю
        """

        data_path = path.join(self.cache_dir, f'{inst}i{course}c{group}g{week}w.json')
        answer = {'file_name': f'{inst}i{course}c{group}g{week}w.json', 'file_path': data_path, 'data': {}}

        if week.isdigit():
            week = self.scrap_available_weeks()[int(week) - 1]

        if try_cache and path.exists(data_path):
            with open(data_path, 'r', encoding='utf-8') as fp:
                res = json.load(fp)
            answer['data'] = res
            return answer
        else:
            self._driver = webdriver.Chrome()
            driver = self._driver
            driver.get(self.url)
            self.__go_to_week_page(required_group=group, required_week=week, required_inst=inst,
                                   required_course=course)
            res = dict()
            days_elements = driver.find_elements(By.CLASS_NAME, 'step-content')
            week_start = week.split('-')[0]
            date_start = datetime.date(int(week_start.split('.')[2]), int(week_start.split('.')[1]),
                                       int(week_start.split('.')[0]))
            cur_date = date_start
            for day_ind in range(len(days_elements)):

                lessons_elements = days_elements[day_ind].find_elements(By.CSS_SELECTOR, '.mb-4')
                date_info = days_elements[day_ind].find_element(By.TAG_NAME, 'span').text.replace(',', '').split(
                    ' ')
                day_number = int(date_info[1])
                week_day = date_info[0]
                while day_number != cur_date.day:
                    cur_date += datetime.timedelta(days=1)
                lessons = []
                for i in range(len(lessons_elements)):
                    try:
                        subject_name_element = lessons_elements[i].find_element(By.TAG_NAME, 'div')
                        lesson_info_element = lessons_elements[i].find_element(By.TAG_NAME, 'ul')
                    except selenium.common.exceptions.NoSuchElementException:
                        continue

                    if subject_name_element and lesson_info_element:
                        cur = dict()
                        sub_info = subject_name_element.text.split()
                        cur['subject'] = ' '.join(sub_info[:len(sub_info) - 1])
                        cur['subject_type'] = sub_info[-1]

                        lesson_info = lesson_info_element.find_elements(By.TAG_NAME, 'li')
                        time = lesson_info[0].text.replace(' ', '').split('–')
                        cur['time_start'] = time[0]
                        cur['time_end'] = time[1]
                        cur['teachers'] = []
                        for ind in range(1, len(lesson_info) - 1):
                            cur['teachers'].append(lesson_info[ind].text)
                        cur['cabinet'] = lesson_info[-1].text
                        if subject is None or cur['subject'] == subject:
                            lessons.append(cur)
                if len(lessons) != 0:
                    res[week_day] = dict({'lessons': lessons, 'date': str(cur_date).replace('-', '.')})

            with open(data_path, 'w', encoding='utf-8') as fp:
                json.dump(res, fp, ensure_ascii=False, indent=2)
        driver.quit()
        answer['data'] = res
        return answer

    def scrap_available_institutes(self, try_cache=True):
        """
        Получает все возможные институты МАИ
        :param try_cache: если True, то будет предпринята попытка загрузить данные из кэша, иначе будет скрапить с нуля
        :return: массив всех возможных институтов
        """

        self._driver = webdriver.Chrome()
        file_path = path.join(self.cache_dir, 'institutes.json')
        if try_cache and path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as fp:
                return json.load(fp)
        driver = self._driver
        driver.get(self.url)
        inst_list = driver.find_element(By.NAME, 'department')
        institutes = [i.text for i in inst_list.find_elements(By.TAG_NAME, 'option')][1:]
        with open(file_path, 'w', encoding='utf-8') as fp:
            json.dump(institutes, fp, ensure_ascii=False, indent=2)
        driver.quit()
        return institutes

    def scrap_available_courses(self, try_cache=True):
        """
        Получает все возможные курсы МАИ
        :param try_cache: если True, то будет предпринята попытка загрузить данные из кэша, иначе будет скрапить с нуля
        :return: массив всех возможных курсов
        """

        self._driver = webdriver.Chrome()
        file_path = path.join(self.cache_dir, 'courses.json')
        if try_cache and path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as fp:
                return json.load(fp)
        driver = self._driver
        driver.get(self.url)
        courses_list = driver.find_element(By.NAME, 'course')
        courses = [i.text for i in courses_list.find_elements(By.TAG_NAME, 'option')][2:]
        with open(file_path, 'w', encoding='utf-8') as fp:
            json.dump(courses, fp, ensure_ascii=False, indent=2)
        driver.quit()
        return courses

    def scrap_available_weeks(self, try_cache=True):
        """
        Получает все недели, на которые можно получить расписание
        :param try_cache: если True, то сначала данные будут искаться в кэше
        :return: массив, содержащий строки в формате ДД.ММ.ГГ-ДД.ММ.ГГ
        """

        # в данном случае все равно, на страницу какой группы и какой недели переходить,
        # так как недели для всех групп одинаковые
        self._driver = webdriver.Chrome()
        driver = self._driver
        data_path = path.join(self.cache_dir, 'weeks.json')
        if try_cache and path.exists(data_path):
            with open(data_path, 'r', encoding='utf-8') as fp:
                return json.load(fp)

        self.__go_to_week_page('8', '1', 'М8О-110Б-23', '')
        weeks_elements_container = driver.find_element(By.CSS_SELECTOR, '.list-group.list-group-striped.list-group-sm')
        weeks = weeks_elements_container.find_elements(By.CSS_SELECTOR, 'li')
        weeks = list(map(lambda x: x.text.split('\n')[1].replace(' ', ''), weeks))

        with open(data_path, 'w', encoding='utf-8') as fp:
            json.dump(weeks, fp, ensure_ascii=False, indent=2)
        driver.quit()
        return weeks

    def scrap_available_groups(self, institute, course):
        """
        Получает все группы для определенного института и курса
        :param institute: номер требуемого института
        :param course: номер требуемого курса
        :return: список строк с названиями доступных групп. Если групп нет, то список будет пустой
        """

        self._driver = webdriver.Chrome()
        driver = self._driver
        self.__go_to_groups_page__(course, institute)
        try:
            groups_elements_container = driver.find_element(By.ID, 'nav-1-eg1')
            groups = groups_elements_container.find_elements(By.TAG_NAME, 'a')
            res = [i.text for i in groups]
        except NoSuchElementException:
            #     если нет групп, то и контейнера для них нет
            res = []
        driver.quit()
        return res

    # пока непонянто, надо это или нет. Функция для скраппинга ВСЕХ институтов, ВСЕХ групп, ВСЕХ недель
    # def update_all(self):
    #     print(self._driver)
    #     available_inst = self.scrap_available_institutes(try_cache=True)
    #     available_courses = self.scrap_available_courses(try_cache=True)
    #     available_weeks = self.scrap_available_weeks(try_cache=True)
    #     print(available_weeks)
    #     # input()
    #     print("start")
    #     for inst in available_inst:
    #         for course in available_courses:
    #             groups = self.scrap_available_groups(inst, course)
    #             print(groups)
    #             for g in groups:
    #                 for week in available_weeks:
    #                     print(inst, course, g, week)
    #                     self.scrap_by_group_and_week(inst, g, week, course, try_cache=True)
