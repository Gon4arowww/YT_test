#!/usr/bin/env python
# coding: utf-8

# In[7]:


# !pip install yandex_tracker_client


# In[25]:


from yandex_tracker_client import TrackerClient
import sqlite3


# In[26]:


# Создаем или открываем базу данных
conn = sqlite3.connect('example.db')
cursor = conn.cursor()
# Создаем таблицу, если она еще не существует
cursor.execute('''
    CREATE TABLE IF NOT EXISTS dates_table (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        key TEXT UNIQUE,
        date1 TEXT,
        date2 TEXT
    )
''')


# In[27]:


# функция для сохранения записей в БД
def save_to_db(key, date1, date2):
    # Пытаемся вставить данные в базу
    try:
        cursor.execute('''
            INSERT INTO dates_table (key, date1, date2) 
            VALUES (?, ?, ?)
        ''', (key, date1, date2))
        conn.commit()
    except sqlite3.IntegrityError:
        # Ключ уже существует в базе данных
        print(f"Key '{key}' already exists in the database.")

def fetch_all_records(table_name):
    try:
        # Формирование SQL-запроса для извлечения всех записей из таблицы
        query = f"SELECT * FROM {table_name}"
        cursor.execute(query)
        # Получение всех записей
        records = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Ошибка при работе с SQLite: {e}")
        records = []
    return records


# In[28]:


# создаем подключение к yandex tracker
lv_token = "y0_AgAAAAAG8hr_AAzbPQAAAAEaNz6FAAD_CQ14-6pPerTIwFWw0KPjkG9ZSQ"
lv_orgId = "7175997"
go_client = TrackerClient(token=lv_token, org_id=lv_orgId)


# In[29]:


lv_key = "TESTAVG-4"
lv_deadline = None
lv_update = None

# получаем значение задачи 
go_issue = go_client.issues[lv_key]
lv_deadline = go_issue.deadline
lv_update = go_issue.updatedAt
print(lv_key, lv_deadline, lv_update)

# сохраняем в БД
save_to_db(lv_key, lv_deadline, lv_update)


# In[30]:


fetch_all_records("dates_table")


# In[32]:


# Закрытие курсора и соединения
cursor.close()
conn.close()

