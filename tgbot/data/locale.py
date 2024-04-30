import logging

import openpyxl
from openpyxl.worksheet.worksheet import Worksheet


class Lang:
    RUS = "rus"
    KAZ = "kz"


class LocaleManager:
    data = {

    }

    default_locale = 'rus'

    @classmethod
    def add_locale(
            cls,
            file_name: str,
            col_locale: int,
            locale_name: str
    ):
        wb = openpyxl.load_workbook(file_name)
        ws: Worksheet = wb.active

        locale_data = {
            locale_name: {}
        }
        
        for row in ws.iter_rows(min_row=1, min_col=1, max_col=col_locale, values_only=True):

            text_ru = row[0]

            if text_ru is None:
                continue

            text_en = row[col_locale - 1]

            if text_en is None:
                text_en = text_ru

            text_en = text_en.strip()
            text_ru = text_ru.strip()

            locale_data[locale_name][text_ru] = text_en
        cls.data.update(
            locale_data
        )

    @classmethod
    def get(cls, text_ru: str, locale: str):
        if text_ru is None:
            return 'f'
        text_ru = text_ru.strip()

        if locale is None:
            locale = cls.default_locale

        locale_data = cls.data.get(locale)

        if (text_en := locale_data.get(text_ru)) is None:
            return text_ru

        return text_en
