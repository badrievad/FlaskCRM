import win32com.client

# Создаем новый экземпляр Excel
excel = win32com.client.Dispatch("Excel.Application")
excel.Visible = False
excel.DisplayAlerts = False  # Отключаем предупреждения
excel.AskToUpdateLinks = False  # Отключаем запросы на обновление ссылок
excel.AlertBeforeOverwriting = False  # Отключаем запросы на перезапись

try:
    # Открываем нужный файл
    workbook = excel.Workbooks.Open(r'C:\Users\ШалапугинД\PycharmProjects\FlaskCRM\Testing calc\Leasing calc vers 1.xlsm')
    sheet_manager = workbook.Sheets('Лист менеджера')

    # Читаем значение
    print('before replace: ' + str(sheet_manager.Range('D2').Value))

    # Изменяем значение
    sheet_manager.Range('D2').Value = 'Легковой автомобиль Hyundai Santa Fe'
    print('after replace: ' + str(sheet_manager.Range('D2').Value))

    # Сохраняем файл под новым именем
    workbook.SaveAs(r'C:\Users\ШалапугинД\PycharmProjects\FlaskCRM\Testing calc\Leasing calc vers 1_1.xlsm', FileFormat=52)

finally:
    # Закрываем книгу без сохранения изменений в оригинальный файл
    workbook.Close(SaveChanges=False)
    # Закрываем Excel, если больше нет открытых книг
    if excel.Workbooks.Count == 0:
        excel.Quit()
    del excel

