import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import datetime

DB_PATH = "sqlite:///sochi_athletes.sqlite3"
Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id = sa.Column(sa.Integer, primary_key=True)
    first_name = sa.Column(sa.TEXT)
    last_name = sa.Column(sa.TEXT)
    gender = sa.Column(sa.TEXT)
    email = sa.Column(sa.TEXT)
    birthdate = sa.Column(sa.TEXT)
    height = sa.Column(sa.Float)

class Athelete(Base):
    __tablename__ = "athelete"
    id = sa.Column(sa.Integer, primary_key=True)
    birthdate = sa.Column(sa.TEXT)
    height = sa.Column(sa.Float)
    name = sa.Column(sa.TEXT)

def connect_db():
    engine = sa.create_engine(DB_PATH)
    session = sessionmaker(engine)
    return session()

def request_data():
    print("Привет!Необходимо ввести следующие данные:")
    first_name = input("Имя: ")
    last_name = input("Фамилию: ")
    email = input("Электронная почта: ")
    gender = input("Пол: ")
    birthdate = input("Дату рождения (пример 1988-12-04): ")
    height = input("Рост (пример 1.76): ")
    user = User(

        first_name=first_name,
        last_name=last_name,
        email=email,
        gender=gender,
        birthdate=birthdate,
        height=height,
    )
    return user

def find_user(id_find, session):
    """
    Производит поиск пользователя в таблице User по заданному идентификатору id_find
    """
    # нахдим все записи в таблице User, у которых поле User.id совпадает с парарметром id_find
    query = session.query(User).filter(User.id == id_find)
    # составляем список идентификаторов всех найденных пользователей
    user_ids = [user.id for user in query.all()]
    user_birthdate = [user.birthdate for user in query.all()]
    user_birthdate = ''.join(user_birthdate)
    user_height = [user.height for user in query.all()]
    user_height = user_height[0]
    return (user_ids, user_birthdate,user_height )

def convert_date(date):
    # Конвертирует дату в формат  datetime.date
    conv_date = date.split("-")
    date_parts = map(int, conv_date)
    date = datetime.date(*date_parts)
    return date

def nearest_by_bd(user, session) :
    """
    Ищет ближайшего по дате рождения атлета к пользователю user
    """
    # отбираем всех атлетов из таблицы Атлеты
    athletes_list = session.query(Athelete).all()
    #создаем словарь
    athlete_id_bd = {}
    #пробегаемся по всем выбранным атлетам
    for athlete in athletes_list :
        #передаем в функцию дату рождения атлета
        #сохраняем в bd  результат конвертации даты рождения атлета
        bd = convert_date(athlete.birthdate)
        #заполняем словарь значениями из bd
        athlete_id_bd[athlete.id] = bd
    #сохраняем в переменную user_bd результат конвертации даты рождения
    user_bd = convert_date(user)
    #задаем значение переменной для миним разницы
    min_dist = None
    athlete_id = None
    athlete_bd = None
    # пробегаемся по словарю, по ключу и значению
    for id_, bd in athlete_id_bd.items():
        #сохраняем в dist разницу между датами рождения юзера и атлета
        dist = abs(user_bd - bd)
        # ищем наименьшее значение dist
        if not min_dist or dist < min_dist:
            min_dist = dist
            athlete_id = id_
            bd = str(bd)
            athlete_bd = bd

    return athlete_id, athlete_bd

def nearest_by_height(user, session) :
    """
    Ищет ближайшего по росту атлета к пользователю user
    """
    # Поиск ближайшего по росту атлета с условием что рост не пустой
    athletes_list = session.query(Athelete).filter(Athelete.height != None).all()
    #создаем словарь и заполняем его значениями id и роста
    atlhete_id_height = {athlete.id : athlete.height for athlete in athletes_list}
    #сохраняем в переменную значение роста юзера
    user_height = user
    #задаем нулевые значения для переменных
    min_dist = None
    athlete_id = None
    athlete_height = None
    # пробегаемся по словарю с атлетами
    for id_, height in atlhete_id_height.items() :
        if height is None :
            continue
        # находим разницу между ростом юзера и атлета
        dist = abs(user_height - height)
        #ищем наименьшее значение dist
        if not min_dist or dist < min_dist :
            min_dist = dist
            athlete_id = id_
            athlete_height = height

    return athlete_id, athlete_height

def print_users_list(user_ids, user_birthdate,user_height ,athelete_height,athelete_birthdate):
    """
    Выводит на экран найденного пользователя, его имя и фамилию и данные найденного атлета.
    Если передан пустой идентификатор, выводит сообщение о том, что пользователя не найдено.
    """
    # проверяем на пустоту список идентификаторов
    if user_ids:
        # если список не пуст, распечатываем найденного пользователя и атлета
        print("Найден пользователь, идентификатор-{} д.р.{} рост {}".format(user_ids, user_birthdate, user_height ))
        if athelete_height:
            print("Найден атлет с соответствующим id и ростом{}".format(athelete_height))
        else:
            print("Не найден атлет с соответствующим ростом")
        if athelete_birthdate:
            print("Найден атлет c соответствующим id и датой рождения {}".format(athelete_birthdate))
        else:
            print("Не найден атлет с соответствующей датой рождения")

def main():
    session = connect_db()
    mode = input("Выберите модуль.\n1 - Модуль для ввода нового пользователя\n2 - Модуль для поиска атлета по идентификатору пользователя\n")

    if mode == "2":
        id_find = input("Введите идентификатор пользователя")
        user_ids, user_birthdate, user_height = find_user(id_find, session)
        if user_height and user_birthdate:
            athelete_birthdate = nearest_by_bd(user_birthdate, session)
            athelete_height = nearest_by_height(user_height, session)
            print_users_list(user_ids, user_birthdate, user_height, athelete_height,athelete_birthdate)
            print("Желаешь повторить выбор модуля? yes  /  no")
            reboot = input()
            if reboot == "yes" :
                main()
        else:
            # если список оказался пустым, выводим сообщение об этом
            print("Пользователя с таким идентификатором нет.")
    elif mode == "1":
        user = request_data()
        session.add(user)
        session.commit()
        print("Отлично, новый пользователь создан!")
        print("Желаешь повторить выбор модуля? yes  /  no")
        reboot=input()
        if reboot == "yes":
            main()
if __name__ == "__main__":
    main()
