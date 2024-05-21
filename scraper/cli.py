import click
from scraperMAIShedule import SheduleScraperMAI


@click.command()
@click.argument('inst')
@click.argument('course')
@click.argument('group')
@click.argument('week')
@click.argument('subject')
@click.option(
    '--path', '-p',
    help='Путь до директории, в которую нужно сохранить информацию',
)
def main(inst, course, group, week, subject, path):
    """
    Загружает расписание на определенного института, определенной группы на определенную неделю.\n
    Формат вызова из cmd: cli.py <inst> <course> <group> <week>\n
    :param inst: требуемый институт (номер)\n
    :param course: требуемый курс\n
    :param group: требуемая группа (полностью)\n
    :param week: требуемая неделя (либо номер недели, либо неделя в формате ДД.ММ.ГГ-ДД.ММ.ГГ)\n
    :param path: путь для директории, куда сохранять файл\n
    """
    s = SheduleScraperMAI('https://mai.ru/education/studies/schedule/', cache_dir=path)
    ans = s.scrap_by_group_and_week(inst, course, group, week, try_cache=False, subject=subject)
    print(f'Scrapped in file {ans['file_path']}')


if __name__ == '__main__':
    main()
