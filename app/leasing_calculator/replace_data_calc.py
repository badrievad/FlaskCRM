import win32com.client


data = {
    'item_type': 'Легковые',
    'item_year': 2024,
    'item_condition': 'Новое',
    'item_price': 1000000.0,
    'item_name': 'Отсутствует наименование ПЛ',
    'currency': 'rub',
    'foreign_price': 10000.0,
    'initial_payment': 100000.0,
    'credit_sum': 800000.0,
    'credit_term': 36,
    'bank_commission': 0.0,
    'insurance_casko': 0.0,
    'insurance_osago': 0.0,
    'health_insurance': 0.0,
    'other_insurance': 0.0,
    'agent_commission': 0.0,
    'manager_bonus': 1.2,
    'tracker': 0.0,
    'mayak': 0.0,
    'fedresurs': 0.0,
    'gsm': 0.0,
    'mail': 0.0,
    'input_period': '2024-08-09',
    'tranches': {
        'tranche1': {
            'size': 20.0,
            'rate': 20.0,
            'fee': 4.85,
            'own_fee': 0.0,
            'credit_date': '2024-08-09',
            'payment_date': '2024-08-09'
        },
        'tranche2': {
            'size': 80.0,
            'rate': 20.0,
            'fee': 4.85,
            'own_fee': 0.0,
            'credit_date': '2024-08-09',
            'payment_date': '2024-08-09'
        },
        'tranche3': {
            'size': 0.0,
            'rate': 0.0,
            'fee': 0.0,
            'own_fee': 0.0,
            'credit_date': '2024-08-09',
            'payment_date': '2024-08-09'
        },
        'tranche4': {
            'size': 0.0,
            'rate': 0.0,
            'fee': 0.0,
            'own_fee': 0.0,
            'credit_date': '2024-08-09',
            'payment_date': '2024-08-09'
        },
        'tranche5': {
            'size': 0.0,
            'rate': 0.0,
            'fee': 0.0,
            'own_fee': 0.0,
            'credit_date': '2024-08-09',
            'payment_date': '2024-08-09'
        }
    }
}

# Пример использования данных
print(data)

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

    sheet_manager.Range('D2').Value = data['item_name']
    sheet_manager.Range('D3').Value = data['item_price']
    sheet_manager.Range('D4').Value = data['initial_payment']
    sheet_manager.Range('D6').Value = data['credit_sum']
    sheet_manager.Range('D11').Value = '1.80'

    # Сохраняем файл под новым именем
    workbook.SaveAs(r'C:\Users\ШалапугинД\PycharmProjects\FlaskCRM\Testing calc\Leasing calc vers 1_1.xlsm', FileFormat=52)

finally:
    # Закрываем книгу без сохранения изменений в оригинальный файл
    workbook.Close(SaveChanges=False)
    # Закрываем Excel, если больше нет открытых книг
    if excel.Workbooks.Count == 0:
        excel.Quit()
    del excel





