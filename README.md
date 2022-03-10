# test-selectel-api

1) Для запуска базы postgre необходимо выполнить docker-compose -f postgre.yml up --build 
2) dump базы также лежит в postgre
3) Для создания таблицы и записи данных за 30 дней необходимо выполнить python3 etl.py 
4) Для запуска файла DAG.py в airflow необходимо установить зависимости из requirements.txt и папку dag_etl помесить в директорию с dag'ами airflow
