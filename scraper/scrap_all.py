from scraperMAIShedule import SheduleScraperMAI
from DBApi import DataBase


def main():
    scraper = SheduleScraperMAI('https://mai.ru/education/studies/schedule/', cache_dir='parsed_data')
    db = DataBase('LessonsDB.db')

    for course in range(1, 4 + 1):
        print(course)
        for group in scraper.scrap_available_groups('8', str(course)):
            print(f"group: {group} from {scraper.scrap_available_groups('8', str(course))}")
            for week in scraper.scrap_available_weeks():
                print(f'week: {week} from {scraper.scrap_available_weeks()}')
                ans = scraper.scrap_by_group_and_week('8', str(course), group, week, try_cache=False)
                db.add_from_json(ans['file_path'])
                print(f"succesfully written: {ans['file_name']}")


if __name__ == '__main__':
    main()
