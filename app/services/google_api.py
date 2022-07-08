from copy import deepcopy
from typing import Optional
from datetime import datetime

from aiogoogle import Aiogoogle

from app.core.config import settings


FORMAT = "%Y/%m/%d %H:%M:%S"
SPREADSHEET_TITLE = 'Отчет на {now}'
SPREADSHEET_BODY = dict(
    properties={
        'title': 'spreadsheet title',
        'locale': 'ru_RU',
    },
    sheets=[{
        'properties': {
            'sheetType': 'GRID',
            'sheetId': 0,
            'title': 'Лист1',
            'gridProperties': {
                'rowCount': settings.table_rows_count,
                'columnCount': settings.table_columns_count
            }
        }
    }]
)
TABLE_HEADER = dict(
    creation_time=['Отчет от'],
    report_name=['Топ проектов по скорости закрытия'],
    report_columns=['Название проекта', 'Время сбора', 'Описание']
)
TABLE_EXCEEDING_SIZE = (
    'Полученные данные превышают размер таблицы. '
    'Полученное кол-во столбцов: {columns_count}, '
    'максимально допустимое: {max_columns_count}. '
    'Полученное кол-во строк: {rows_count}, '
    'максимально допустимое {max_rows_count}'
)


class dict_as_obj(dict):

    def __getattr__(self, name):
        return self.get(name)

    def __setattr__(self, name, value):
        me = self
        me[name] = value


async def spreadsheets_create(
        wrapper_services: Aiogoogle,
        spreadsheet_body: Optional[dict] = None
) -> str:
    service = await wrapper_services.discover(*settings.spreadsheets_api)
    spreadsheet_body = (
        deepcopy(dict_as_obj(SPREADSHEET_BODY))
        if spreadsheet_body is None
        else dict_as_obj(spreadsheet_body)
    )
    spreadsheet_body.properties['title'] = (
        SPREADSHEET_TITLE.format(
            now=datetime.now().strftime(FORMAT))
    )
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    return response['spreadsheetId']


async def set_user_permissions(
        spreadsheet_id: str,
        wrapper_services: Aiogoogle
) -> None:
    permissions_body = {
        'type': 'user',
        'role': 'writer',
        'emailAddress': settings.email
    }
    service = await wrapper_services.discover(*settings.drive_api)
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheet_id,
            json=permissions_body,
            fields='id'
        )
    )


async def spreadsheets_update_value(
        spreadsheet_id: str,
        projects: list,
        wrapper_services: Aiogoogle,
        table_header: Optional[dict] = None
) -> None:
    service = await wrapper_services.discover(*settings.spreadsheets_api)
    rows = sorted(
        (
            (
                project.name,
                project.close_date - project.create_date,
                project.description
            )
            for project in projects
        ),
        key=lambda row: row[1]
    )
    table_header = (
        deepcopy(dict_as_obj(TABLE_HEADER))
        if table_header is None
        else dict_as_obj(table_header)
    )
    now_date_time = datetime.now().strftime(FORMAT)
    try:
        table_header.creation_time.append(now_date_time)
    except AttributeError:
        table_header = dict(creation_time=[now_date_time], **table_header)
    table_values = [
        *table_header.values(),
        *[list(map(str, row)) for row in rows]
    ]
    rows_count = len(table_values)
    columns_count = max([len(columns) for columns in table_values])
    if (
        rows_count > settings.table_rows_count or
        columns_count > settings.table_columns_count
    ):
        raise IndexError(
            TABLE_EXCEEDING_SIZE.format(
                rows_count=rows_count,
                columns_count=columns_count,
                max_rows_count=settings.table_rows_count,
                max_columns_count=settings.table_columns_count,
            )
        )
    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range=f'R1C1:R{rows_count}C{columns_count}',
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )
