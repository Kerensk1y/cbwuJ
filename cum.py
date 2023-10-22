import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QPushButton, QVBoxLayout, QWidget
import sqlite3

# Подключение к базе данных
db_name = 'databases/MyDb.db'
conn = sqlite3.connect(db_name)
cursor = conn.cursor()

# Запрос для получения данных из таблицы Gr_prog
cursor.execute("SELECT * FROM Gr_prog")
data1 = cursor.fetchall()

# Запрос для получения данных из таблицы gr_konk
cursor.execute("SELECT * FROM gr_konk")
data2 = cursor.fetchall()

# Запрос для подсчета количества НИР для каждого уникального значения "Код конк." в таблице Gr_prog
cursor.execute("SELECT 'Код конк.', COUNT(*) FROM Gr_prog GROUP BY 'Код конк.'")
konk_counts = cursor.fetchall()

# Создание словаря для хранения количества НИР по каждому "Код конк."
konk_count_dict = dict(konk_counts)

# Обновление данных в таблице gr_konk
for row, row_data in enumerate(data2):
    code_konk = row_data[1]  # Получаем "Код конк." из второй таблицы
    if code_konk in konk_count_dict:
        count_nir = konk_count_dict[code_konk]  # Получаем количество НИР для этого кода конкурса
        data2[row] = (row_data[0], row_data[1], row_data[2], row_data[3], row_data[4], row_data[5], row_data[6],
                     row_data[7], count_nir)  # Обновляем данные во второй таблице

# Создание окна
app = QApplication(sys.argv)
window = QMainWindow()
window.setGeometry(100, 100, 800, 600)

# Создание виджета для отображения таблицы 1
table1 = QTableWidget()
table1.setColumnCount(15)
table1.setHorizontalHeaderLabels(["Код конк.", "Код НИР", "Руководитель", "Сокр-е наим-е ВУЗа",
                                "План. объём финанс-я", "Факт. объем финанс-я", "1 кв-л", "2 кв-л", "3 кв-л", "4 кв-л",
                                "Код по ГРНТИ", "Должность", "Звание", "Ученая степень", "Код вуза", "Наименование НИР"])
table1.setRowCount(len(data1))

# Заполнение таблицы 1 данными
for row, row_data in enumerate(data1):
    for col, value in enumerate(row_data):
        item = QTableWidgetItem(str(value))
        table1.setItem(row, col, item)

# Создание виджета для отображения таблицы 2
table2 = QTableWidget()
table2.setColumnCount(9)
table2.setHorizontalHeaderLabels(["Название конкурса", "Код конк.", "План. объем финанс-я", "Факт. объем финанс-я",
                                "1 кв-л", "2 кв-л", "3 кв-л", "4 кв-л", "Кол-во НИР"])
table2.setRowCount(len(data2))

# Заполнение таблицы 2 данными и количеством НИР
for row, row_data in enumerate(data2):
    for col, value in enumerate(row_data):
        item = QTableWidgetItem(str(value))
        table2.setItem(row, col, item)

# Создание виджета, содержащего таблицы
table_container = QWidget()
layout = QVBoxLayout()
table_container.setLayout(layout)

# Добавление таблиц в виджет
layout.addWidget(table1)
layout.addWidget(table2)
table2.hide()  # Скрываем вторую таблицу при старте приложения

# Добавление кнопки для переключения между таблицами
toggle_button = QPushButton("Показать/скрыть таблицу 2")
toggle_button.clicked.connect(lambda: table2.setVisible(not table2.isVisible()))
layout.addWidget(toggle_button)

# Отображение окна и виджета с таблицами
window.setCentralWidget(table_container)
window.show()

# Закрытие базы данных при закрытии приложения
def close_database():
    conn.close()

app.aboutToQuit.connect(close_database)
sys.exit(app.exec())
