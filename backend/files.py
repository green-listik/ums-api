import os
from zipfile import ZipFile

import xlsxwriter
import glob


def writeXLSX(data):
    headers = ['Тема', 'Суть сообщения, информационный повод',
               'Дата', 'Место, время',
               'Ответственное лицо по вопросам', 'Официальный спикер']
    file_name = os.getcwd() + "/files/" + 'Events.xlsx'
    workbook = xlsxwriter.Workbook(file_name)
    worksheet = workbook.add_worksheet()
    format = workbook.add_format({'bold': True, 'align': 'center', 'shrink': 'True'})
    for i in range(len(headers)):
        worksheet.write(0, i, headers[i], format)
    for i in range(1, len(data)):
        j = 0
        if data[i]['isGubernator']:
            format = workbook.add_format({'bold': True, 'bg_color': 'red'})
        elif data[i]['isImportant']:
            format = workbook.add_format({'bg_color': 'red'})
        else:
            format = workbook.add_format()
        for key in data[i]:
            if key != 'isGubernator' and key != 'isImportant':
                worksheet.write(i, j, data[i][key], format)
                j += 1
    workbook.close()
    return file_name


def packZIP(xlsx_file):
    list_of_files = glob.glob(os.getcwd() + "/files/*")
    file_name = os.getcwd() + "/temp/" + 'Events.zip'
    file_name2 = os.getcwd() + "/temp/" + 'Fact_lists.zip'
    zip2 = ZipFile(file_name2, 'w')
    for file in list_of_files:
        zip2.write(file)
    zip2.close()
    zip = ZipFile(file_name, 'w')
    zip.write(file_name2)
    zip.write(xlsx_file)
    zip.close()
    return file_name
