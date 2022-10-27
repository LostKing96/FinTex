# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask import Flask, url_for
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from importlib import import_module
from logging import basicConfig, DEBUG, getLogger, StreamHandler
from os import path

from passlib.context import CryptContext
from pymongo import MongoClient
import pymongo
import logging
from datetime import datetime, timedelta

from app.base.util import hash_pass
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Database:
    def __init__(self):
        self.client = MongoClient('mongodb://database:27017/')

        self.db = self.client["FinTEx_Super_Platform"]
        self.users = self.db['users']
        self.bp_constructor = self.db['bp_constructor']
        self.business_plans = self.db['business_plans']
        self.maintenance = self.db['maintenance']
        self.consulting = self.db['consulting']
        self.user_bp = self.db['user_bp']
        self.user_fm = self.db['user_fm']
        self.resetPswd = self.db['resetpswd']
        # added database for statistics
        self.statistics = self.db['statistics']
        # added database for users feedbacks
        self.feedbacks = self.db['feedbacks']

        self.initial_populate()

    def updatePassword(self, password, email):
        result = self.users.update({'email': email},
                                       {"$set": {"password": password, "hashed_password": pwd_context.hash(password)}})
        return result

    def insert(self, table, data):
        if type(data) == list:
            result = table.insert_many(data)
            for d in data:
                d["_id"] = None
        else:
            result = table.insert_one(data)
            data["_id"] = None
        return result

    def get(self, table, key, data):
        try:
            result = table.find({key: data}, {'_id': False})
            result = list(result)
            return result
        except:
            return None

    def get_one(self, table, key, data):
        try:
            result = table.find_one({key: data}, {'_id': False})
            return dict(result)
        except:
            return None

    def get_last(self, table, key, data):
        try:
            result = table.find_one({key: data},
                                    {'_id': False},
                                    sort=[('_id', pymongo.DESCENDING)])
            return dict(result)
        except:
            return None

    def get_all(self, table):
        try:
            result = table.find({}, {'_id': False})
            return list(result)
        except:
            return None

    def delete(self, table, key, data):
        result = table.delete_many({key: data})
        return result

    def initial_populate(self):
        bp_construcotrs = self.get(self.bp_constructor, "bp_type", "dkb2025")
        for constructor in bp_construcotrs:
            self.delete(self.bp_constructor, "bp_type", "dkb2025")
            self.delete(self.bp_constructor, "fm_type", "dkb2025")

        constructor = {
            "bp_type": "dkb2025",
            "project_name_label": "Название проекта",
            "project_name_popover_title": "Как выбрать название проекта",
            "project_name_popover_content": "Лаконичное, запоминающееся и яркое название со смыслом. Всегда имейте в виду, что каждый раз произнося название Вашего проекта, люди неосознанно представляют себе в голове ассоциации, связанные с этим названием. Поэтому выбирайте название с умом, чтобы эти ассоциации были приятными и стимулирующими к покупке Вашего продукта.",
            "project_name_video": "",
            "project_name_placeholder": "",
            "project_name_lines_number": "1",
            "businessman_name_label": "Наименование заявителя",
            "businessman_name_popover_title": "Как правильно написать наименование заявителя",
            "businessman_name_popover_content": "Укажите название своего ИП/ТОО, а также (желательно) имя основателя/основателей проекта",
            "businessman_name_video": "",
            "businessman_name_placeholder": "ИП ...",
            "businessman_name_lines_number": "1",
            "capital_distribution_label": "Распределение уставного капитала",
            "capital_distribution_popover_title": "Как заполнить этот пункт",
            "capital_distribution_popover_content": "Напишите, кому из основателей какая доля проекта принадлежит. Это больше относится к ТОО. ТОО имеет уставной капитал, который вносится в равных/разных пропорциях основателями проекта. В случае ИП - 100% принадлежит владельцу ИП ",
            "capital_distribution_video": "",
            "capital_distribution_placeholder": "",
            "capital_distribution_lines_number": "3",
            "address_label": "Юридический адрес",
            "address_popover_title": "",
            "address_popover_content": "Здесь нужно написать полный адрес помещения, на который вы официально зарегистрировали свое ИП/ТОО",
            "address_video": "",
            "address_placeholder": "город FinTEx, улица Победителей Гранта, д. № 1, кв. № 1, 010000",
            "address_lines_number": "1",
            "website_label": "Сайт (при наличии)",
            "website_popover_title": "Как указать свой сайт",
            "website_popover_content": "Просто напишите адрес вашего вебсайта. Если у вас его нет - лучше его завести, в наше время это must-have. Проще всего это сделать в конструкторе сайтов, например в Tilda. Подробнее по ",
            "website_video": "https://tilda.cc/ru/",
            "website_placeholder": "www.ваш-прекрасный-сайт.kz",
            "website_lines_number": "1",
            "self_investment_label": "Наличие средств",
            "self_investment_popover_title": "Как указать наличие средств",
            "self_investment_popover_content": "Здесь нужно обязательно написать, сколько своих средств вы вложите в проект. Не забудьте, что сумма должна быть как минимум 500 000 тг (10% от суммы гранта). Чем больше вы вкладываете своих денег, тем более ваш проект привлекателен в глазах жюри. Также, надо указать, если вы используете свое помещение или оборудование",
            "self_investment_video": "",
            "self_investment_placeholder": ">= 500 000 тг.",
            "self_investment_lines_number": "1",
            "your_product_label": "Ваш продукт",
            "your_product_popover_title": "Как заполнить инфо о вашем продукте",
            "your_product_popover_content": "Здесь вкратце напишите суть своего продукта. Например - онлайн платформа для предпринимателей с продвинутым финансовым функционалом",
            "your_product_video": "",
            "your_product_placeholder": "",
            "your_product_lines_number": "1",
            "start_deadline_label": "Срок запуска проекта",
            "start_deadline_popover_title": "Как указать срок запуска проекта",
            "start_deadline_popover_content": "Укажите с точностью до месяца и дня, например - 01.07.2022. Если ваша дата запуска проекта зависит от даты получения гранта, имейте в виду, что грантовые деньги вы получите примерно через 3 месяца после подачи документов. Также, не беспокойтесь о том, что вы можете начать чуть позже, чем укажете здесь - никаких последствий за это не будет.",
            "start_deadline_video": "",
            "start_deadline_placeholder": "",
            "start_deadline_lines_number": "1",
            "problem_label": "Проблема",
            "problem_popover_title": "Как описать проблему",
            "problem_popover_content": "Здесь вам нужно описать, с какими проблемами сталкиваются ваши потенциальные клиенты (и которые вы собираетесь решить своим продуктом). Имейте в виду, что проблема считается проблемой, если человек пытается ее решить (то есть проблема не выдуманная), но это стоит ему денег, времени или усилий. Например, какую проблему решаем мы: Начинающим предпринимателям нужен стартовый капитал для открытия бизнеса. Поэтому тратят много времени, денег и усилий на то, чтобы подготовить документы на грант, кредит или для инвестора. При этом, зачастую они проигрывают борьбу за капитал более опытным предпринимателям, либо получают невыгодные условия.",
            "problem_video": "",
            "problem_placeholder": "",
            "problem_lines_number": "3",
            "solution_label": "Решение",
            "solution_popover_title": "Как указать свое решение",
            "solution_popover_content": "А здесь вы рассказываете, как ваш продукт чудесным образом решит проблема вашего клиента из предыдущего пункта. Например: наша платформа позволит начинающим предпринимателям получить передовые знания и опыт по финансам и другим областям бизнеса. При этом, они потратят намного меньше времени благодаря разлчиным конструктора и встроенному искуссвенному интеллекту",
            "solution_video": "",
            "solution_placeholder": "",
            "solution_lines_number": "4",
            "innovation_label": "Инновация",
            "innovation_popover_title": "В чем заключается Ваша инновация/новизна",
            "innovation_popover_content": "Это могут быть каналы продаж, маркетинговая стратегия, материалы или способы производства продукции или какие-то технические составляющие Вашего проекта",
            "innovation_video": "",
            "innovation_placeholder": "",
            "innovation_lines_number": "1",
            "patents_label": "Авторские права",
            "patents_popover_title": "Если есть патент на Вашу продукцию",
            "patents_popover_content": "Здесь надо указать при наличии есть ли у Вас какие-то документы, которые доказывают что только Вы можете это использовать",
            "patents_video": "",
            "patents_placeholder": "",
            "patents_lines_number": "1",
            "business_model_label": "Бизнес модель",
            "business_model_popover_title": "Описание Вашей бизнес модели",
            "business_model_popover_content": "Здесь Вы указываете как работает Ваш бизнес: где покупаете материалы, кому продаете услуги/продукцию, а также информацию через сколько Вы сможете окупить вложения, конкурентоспособен ли Ваш бизнес-проекта, информацию о поставщиках и потребителях, есть ли  договора/контракты на поставку товара/основных средств/сырья и материалов/оказание услуг/работ/приобретение технологий/франшизы/патента и прочее",
            "business_model_video": "",
            "business_model_placeholder": "",
            "business_model_lines_number": "1",
            "resources_label": "Ресурсы",
            "resources_popover_title": "Какие ресурсы для проекта есть",
            "resources_popover_content": "Здесь Вы пишете есть ли помещение и оборудование для реализации бизнес-проекта, есть ли рынок сбыта и есть ли какие-то факторы, которые Вам облегчат продажу Вашейе продукции/услуг",
            "resources_video": "",
            "resources_placeholder": "",
            "resources_lines_number": "1",
            "analysis_label": "Анализ",
            "analysis_popover_title": "Объем Вашего рынка",
            "analysis_popover_content": "Здесь нужно будет посчитать сколько в общем клиентов могут купить у Вас товар/услугу (это и есть объем и емкость рынка продукта), узнать как меняется Ваша сфера - можете включить вырезки из статей и др.источников, желательно показать, что Ваша отрасль растет, то есть все больше людей начинают пользоваться такими продуктами и услугами и есть ли перспектива расширения бизнеса - то есть опять же что количество таких проеков растет",
            "analysis_video": "",
            "analysis_placeholder": "",
            "analysis_lines_number": "1",
            "competitors_label": "Конкуренты",
            "competitors_popover_title": "Ваше преимущество по сравнению с конкурентами",
            "competitors_popover_content": "Здесь надо описать по каким показателям Вы лучше конкурентов или наравне",
            "competitors_video": "",
            "competitors_placeholder": "",
            "competitors_lines_number": "1",
            "strategy_label": "Стратегия",
            "strategy_popover_title": "Как Вы планируете продвигать Ваш продукт/услугу",
            "strategy_popover_content": """Опишите на каких рынках Вы планируете продавать Ваш товар/услугу (экспортный и внутренний), укажите кому или каким основным компаниям Вы планируете продавать Ваш товар/услугу, напишите описание продукций компаний-конкурентов. Подробнее смотрите по """,
            "strategy_video": "https://picayune-ziconium-7e6.notion.site/bd60733df2fe431ca8edd4cd444840f3",
            "strategy_placeholder": "",
            "strategy_lines_number": "1",
            "team_label": "Команда",
            "team_popover_title": "Опишите Вашу команду",
            "team_popover_content": "Здесь надо показать количество сотрудников, кто будет в Вашем проекте, их квалификацию с приложением резюме и документов, подтверждающих квалификацию (диплом, сертификаты).",
            "team_video": "",
            "team_placeholder": "",
            "team_lines_number": "1",
            "experience_label": "Опыт",
            "experience_popover_title": "Полезные опыт команды для развития данного проекта",
            "experience_popover_content": "Опишите опыт команды (можно основной) участия в проектах, полученные результаты и показатели развития предприятия. Другими словами, покажите что Ваша команда может сделать этот проект",
            "experience_video": "",
            "experience_placeholder": "",
            "experience_lines_number": "1",
            "organizational_structure_label": "Организационная структура",
            "organizational_structure_popover_title": "Покажите каких сотрудники будут в Вашем проекте",
            "organizational_structure_popover_content": "Напишите какие сотрудники будут в проекте (преподаватель, инженер, бухгалтер) и сколько планируете им платить. Также напишите как Вы планируете привлекать новых специалистов.",
            "organizational_structure_video": "",
            "organizational_structure_placeholder": "",
            "organizational_structure_lines_number": "1",
            "strength_label": "Сильные стороны",
            "strength_popover_title": "Сильные стороны",
            "strength_popover_content": "Покажите какие сильные стороны есть у Вашего проекта, например у Вас есть патент, квалифицированные специалисты и т.п. Подробнее о 4х пунктах Вы можете прочитать с примерами по ",
            "strength_video": "https://studme.org/1280052810034/ekonomika/silnye_storony",
            "strength_placeholder": "",
            "strength_lines_number": "1",
            "weakness_label": "Слабые стороны",
            "weakness_popover_title": "Слабые стороны",
            "weakness_popover_content": "Например что Вы начинающий предприниматель/бизнес, что о Вас не знают еще и т.п.",
            "weakness_video": "",
            "weakness_placeholder": "",
            "weakness_lines_number": "1",
            "possibility_label": "Возможности",
            "possibility_popover_title": "Возможности для роста проекта",
            "possibility_popover_content": "Например, новые законы - они облегчают Вашу деятельность или из-за этого клиентам надо будет покупать у Вас продукцию, изменение курса валют и другое",
            "possibility_video": "",
            "possibility_placeholder": "",
            "possibility_lines_number": "1",
            "threat_label": "Угрозы",
            "threat_popover_title": "Угрозы вашему бизнесу",
            "threat_popover_content": "Здесь надо описать из-за чего может пострадать Ваш бизнес-проект, например карантин, локдаун, переход на удаленку и т.п.",
            "threat_video": "",
            "threat_placeholder": "",
            "threat_lines_number": "1",
            "realization_plan_label": "Реализация",
            "realization_plan_popover_title": "План реализации Вашего проекта",
            "realization_plan_popover_content": "Здесь надо указать этапы реализации проекта, начиная с/до получения грантовых средств, конкретные получаемые результаты в конце этапа, сколько времени займет и необходимых денег (план составляется как на период финансирования проекта, так и после окончания данного периода)",
            "realization_plan_video": "",
            "realization_plan_placeholder": "",
            "realization_plan_lines_number": "1",
            "investment_before_label": "Предыдущие инвестиции",
            "investment_before_popover_title": "Привлекали ли ранее инвестиции в Ваш бизнес-проект",
            "investment_before_popover_content": "Укажите детали инвестий, привлеченных в бизнес, при наличии. То есть какую сумму, за какую долю в проекте и по каким условиям.",
            "investment_before_video": "",
            "investment_before_placeholder": "",
            "investment_before_lines_number": "1",
            "financial_effectivity_label": "Финансовая эффективность",
            "financial_effectivity_popover_title": "Финансовые показатели Вашего бизнеса с учетом грантовых/инвест. средств",
            "financial_effectivity_popover_content": "Здесь надо будет приложить выжимку основных показателей бизнеса, такие как расходы на производство, прибыль, чистая прибыль, рентабельность выпускаемого продукта) к концу реализации проекта, здесь надо приложить расчет показателей в формате Excel.",
            "financial_effectivity_video": "",
            "financial_effectivity_placeholder": "",
            "financial_effectivity_lines_number": "1",
            "conclusion_label": "Вывод",
            "conclusion_popover_title": "Ваши выводы про проекту",
            "conclusion_popover_content": "Здесь напишите Выводу по Вашему проекту. То есть что за проект у Вас с кратким описанием, сколько требуется инвестиций и к каким результатам планируете прийти, если Вас профинансируют/дадут грант. И Ваши послания жюри.",
            "conclusion_video": "",
            "conclusion_placeholder": "Выводы по проекту",
            "conclusion_lines_number": "10",
            "_label": "",
            "_popover_title": "",
            "_popover_content": "",
            "_video": "",
            "_placeholder": "",
            "_lines_number": "1"
        }
        self.insert(self.bp_constructor, constructor)

        fm_constructor = {
            "fm_type": "dkb2025",
            "investment_name0_label": "Название инвестиции",
            "investment_name0_popover_title": "",
            "investment_name0_popover_content": "",
            "investment_name0_video": "",
            "investment_name0_placeholder": "",
            "investment_name0_lines_number": "1",
            "investment0_label": "Сумма инвестиции",
            "investment0_popover_title": "",
            "investment0_popover_content": "",
            "investment0_video": "",
            "investment0_placeholder": "",
            "investment0_lines_number": "1",
            "employee_position0_label": "Название должности",
            "employee_position0_popover_title": "",
            "employee_position0_popover_content": "",
            "employee_position0_video": "",
            "employee_position0_placeholder": "",
            "employee_position0_lines_number": "1",
            "employee_salary0_label": "Зарплата дожности",
            "employee_salary0_popover_title": "",
            "employee_salary0_popover_content": "",
            "employee_salary0_video": "",
            "employee_salary0_placeholder": "",
            "employee_salary0_lines_number": "1",
            "permanent_expenditure_name0_label": "Название постоянной затраты",
            "permanent_expenditure_name0_popover_title": "",
            "permanent_expenditure_name0_popover_content": "",
            "permanent_expenditure_name0_video": "",
            "permanent_expenditure_name0_placeholder": "",
            "permanent_expenditure_name0_lines_number": "1",
            "permanent_expenditure0_label": "Сумма постоянной затраты",
            "permanent_expenditure0_popover_title": "",
            "permanent_expenditure0_popover_content": "",
            "permanent_expenditure0_video": "",
            "permanent_expenditure0_placeholder": "",
            "permanent_expenditure0_lines_number": "1",
            "variable_expenditure_name0_label": "Название переменное затраты за единицу продукта",
            "variable_expenditure_name0_popover_title": "",
            "variable_expenditure_name0_popover_content": "",
            "variable_expenditure_name0_video": "",
            "variable_expenditure_name0_placeholder": "",
            "variable_expenditure_name0_lines_number": "1",
            "variable_expenditure0_label": "Сумма переменной затраты за единицу продукта",
            "variable_expenditure0_popover_title": "",
            "variable_expenditure0_popover_content": "",
            "variable_expenditure0_video": "",
            "variable_expenditure0_placeholder": "",
            "variable_expenditure0_lines_number": "1",
            "product1_name_label": "Название продукта 1",
            "product1_name_popover_title": "",
            "product1_name_popover_content": "",
            "product1_name_video": "",
            "product1_name_placeholder": "",
            "product1_name_lines_number": "1",
            "product2_name_label": "Название продукта 2",
            "product2_name_popover_title": "",
            "product2_name_popover_content": "",
            "product2_name_video": "",
            "product2_name_placeholder": "",
            "product2_name_lines_number": "1",
            "product1_price_label": "Цена продукта 1",
            "product1_price_popover_title": "",
            "product1_price_popover_content": "",
            "product1_price_video": "",
            "product1_price_placeholder": "",
            "product1_price_lines_number": "1",
            "product1_expenditure_increase_label": "Ежемесячное увеличение переменных затрат на продукт 1",
            "product1_expenditure_increase_popover_title": "",
            "product1_expenditure_increase_popover_content": "",
            "product1_expenditure_increase_video": "",
            "product1_expenditure_increase_placeholder": "",
            "product1_expenditure_increase_lines_number": "1",
            "product1_sales_label": "Продажи продукта 1 в месяц",
            "product1_sales_popover_title": "",
            "product1_sales_popover_content": "",
            "product1_sales_video": "",
            "product1_sales_placeholder": "",
            "product1_sales_lines_number": "1",
            "product1_sales_increase_label": "Ежемесячное увеличение продаж продукта 1",
            "product1_sales_increase_popover_title": "",
            "product1_sales_increase_popover_content": "",
            "product1_sales_increase_video": "",
            "product1_sales_increase_placeholder": "",
            "product1_sales_increase_lines_number": "1",
            "product2_price_label": "Цена продукта 2",
            "product2_price_popover_title": "",
            "product2_price_popover_content": "",
            "product2_price_video": "",
            "product2_price_placeholder": "",
            "product2_price_lines_number": "1",
            "product2_expenditure_increase_label": "Ежемесячное увеличение переменных затрат на продукт 2",
            "product2_expenditure_increase_popover_title": "",
            "product2_expenditure_increase_popover_content": "",
            "product2_expenditure_increase_video": "",
            "product2_expenditure_increase_placeholder": "",
            "product2_expenditure_increase_lines_number": "1",
            "product2_sales_label": "Продажи продукта 2 в месяц",
            "product2_sales_popover_title": "",
            "product2_sales_popover_content": "",
            "product2_sales_video": "",
            "product2_sales_placeholder": "",
            "product2_sales_lines_number": "1",
            "product2_sales_increase_label": "Ежемесячное увеличение продаж продукта 1",
            "product2_sales_increase_popover_title": "",
            "product2_sales_increase_popover_content": "",
            "product2_sales_increase_video": "",
            "product2_sales_increase_placeholder": "",
            "product2_sales_increase_lines_number": "1"
        }
        self.insert(self.bp_constructor, fm_constructor)
        return "ok"


db = Database()


# def register_extensions(app):
#     pass


def register_blueprints(app):
    bp = import_module('app.base.routes')
    au = import_module('app.authorized.routes')
    app.register_blueprint(bp.blueprint)
    app.register_blueprint(au.authorized)
    # for module_name in ('base', 'authorized'):
    #     module = import_module('app.{}.routes'.format(module_name))
    #     app.register_blueprint(module.blueprint)


# def configure_database(app):

#     @app.before_first_request
#     def initialize_database():
#         db.create_all()

#     @app.teardown_request
#     def shutdown_session(exception=None):
#         db.session.remove()

def create_app(config):
    app = Flask(__name__, static_folder='base/static')
    app.config.from_object(config)
    # register_extensions(app)
    register_blueprints(app)
    # configure_database(app)
    return app
