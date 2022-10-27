# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import logging
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, FieldList, FormField
from wtforms.validators import InputRequired, Email, DataRequired
from wtforms.widgets import TextArea
from flask import Markup, session
from app import db

## login and registration

# class AddressEntryForm(FlaskForm):
#     name = StringField()

# class AddressesForm(FlaskForm):
#     """A form for one or more addresses"""
#     addresses = FieldList(FormField(AddressEntryForm), min_entries=1)

def create_field_fm(name):
    label_string = name + "_label"
    title_string = name + "_popover_title"
    content_string = name + "_popover_content"
    video_string = name + "_video"
    lines_number_string = name + "_lines_number"
    placeholder_string = name + "_placeholder"
    label = db.get_one(db.bp_constructor, "fm_type", "dkb2025")[label_string]
    title = db.get_one(db.bp_constructor, "fm_type", "dkb2025")[title_string]
    content = db.get_one(db.bp_constructor, "fm_type", "dkb2025")[content_string]
    video = db.get_one(db.bp_constructor, "fm_type", "dkb2025")[video_string]
    lines_number = int(db.get_one(db.bp_constructor, "fm_type", "dkb2025")[lines_number_string])
    placeholder = db.get_one(db.bp_constructor, "fm_type", "dkb2025")[placeholder_string]
    # value = db.get_one(db.user_bp, "username", username)
    render = {"rows":lines_number, "placeholder": placeholder, "onkeypress":"auto_grow(this);", "onkeyup":"auto_grow(this);", "style":"margin-top:20px;resize:vertical;"}
    first = ' <a href="#" data-toggle="popover" data-trigger="focus" title="" data-content="'
    second = " <a href='"
    third = "'"
    if video == "":
        fourth = " target='_blank' rel='noopener noreferrer'></a>"
    else:
        fourth = " target='_blank' rel='noopener noreferrer'>ссылке</a>"
    fifth = '" data-original-title="'
    sixth = '">(Как заполнять?)</a>'
    markup = label + first + content + second + video + third + fourth + fifth + title + sixth
    field = TextAreaField(label=Markup(f'{markup}'), render_kw=render, id=name, validators=[DataRequired()])
    return field


def create_field(name):
    label_string = name + "_label"
    title_string = name + "_popover_title"
    content_string = name + "_popover_content"
    video_string = name + "_video"
    lines_number_string = name + "_lines_number"
    placeholder_string = name + "_placeholder"
    label = db.get_one(db.bp_constructor, "bp_type", "dkb2025")[label_string]
    title = db.get_one(db.bp_constructor, "bp_type", "dkb2025")[title_string]
    content = db.get_one(db.bp_constructor, "bp_type", "dkb2025")[content_string]
    video = db.get_one(db.bp_constructor, "bp_type", "dkb2025")[video_string]
    lines_number = int(db.get_one(db.bp_constructor, "bp_type", "dkb2025")[lines_number_string])
    placeholder = db.get_one(db.bp_constructor, "bp_type", "dkb2025")[placeholder_string]
    # value = db.get_one(db.user_bp, "username", username)
    render = {"rows":lines_number, "placeholder": placeholder, "onkeypress":"auto_grow(this);", "onkeyup":"auto_grow(this);", "style":"margin-top:20px;resize:vertical;"}
    first = ' <a href="#" data-toggle="popover" data-trigger="focus" title="" data-content="'
    second = " <a href='"
    third = "'"
    if video == "":
        fourth = " target='_blank' rel='noopener noreferrer'></a>"
    else:
        fourth = " target='_blank' rel='noopener noreferrer'>ссылке</a>"
    fifth = '" data-original-title="'
    sixth = '">(Как заполнять?)</a>'
    markup = label + first + content + second + video + third + fourth + fifth + title + sixth
    field = TextAreaField(label=Markup(f'{markup}'), render_kw=render, id=name, validators=[DataRequired()])
    return field

class fmForm(FlaskForm):
    investment0 = create_field_fm("investment0")
    investment_name0 = create_field_fm("investment_name0")

    investment_name1 = TextAreaField('investment_name1', render_kw={"rows": 1, "placeholder":"test"}, id='investment_name1')
    investment1 = TextAreaField('investment1', render_kw={"rows": 1, "placeholder": "test"}, id='investment1')

    investment_name1 = TextAreaField('investment_name1', id='investment_name1')
    investment1 = TextAreaField('investment1', id='investment1')

    investment_name2 = TextAreaField('investment_name2', id='investment_name2')
    investment2 = TextAreaField('investment2', id='investment2')

    investment_name3 = TextAreaField('investment_name3', id='investment_name3')
    investment3 = TextAreaField('investment3', id='investment3')

    investment_name4 = TextAreaField('investment_name4', id='investment_name4')
    investment4 = TextAreaField('investment4', id='investment4')

    investment_name5 = TextAreaField('investment_name5', id='investment_name5')
    investment5 = TextAreaField('investment5', id='investment5')

    investment_name6 = TextAreaField('investment_name6', id='investment_name6')
    investment6 = TextAreaField('investment6', id='investment6')

    investment_name7 = TextAreaField('investment_name7', id='investment_name7')
    investment7 = TextAreaField('investment7', id='investment7')

    investment_name8 = TextAreaField('investment_name8', id='investment_name8')
    investment8 = TextAreaField('competitor1', id='investment1')

    investment_name9 = TextAreaField('investment_name9', id='investment_name9')
    investment9 = TextAreaField('competitor1', id='investment1')

    investment_name10 = TextAreaField('investment_name10', id='investment_name10')
    investment10 = TextAreaField('competitor1', id='investment1')

    investment_name11 = TextAreaField('investment_name11', id='investment_name11')
    investment11 = TextAreaField('investment11', id='investment11')

    investment_name12 = TextAreaField('investment_name12', id='investment_name12')
    investment12 = TextAreaField('investment12', id='investment12')

    investment_name13 = TextAreaField('investment_name13', id='investment_name13')
    investment13 = TextAreaField('investment13', id='investment13')

    investment_name14 = TextAreaField('investment_name14', id='investment_name14')
    investment14 = TextAreaField('investment14', id='investment14')








    employee_position0 = create_field_fm("employee_position0")
    employee_salary0 = create_field_fm("employee_salary0")

    employee_position1 = TextAreaField('employee_position1', id='employee_position1')
    employee_salary1 = TextAreaField('employee_salary1', id='employee_salary1')

    employee_position2 = TextAreaField('employee_position2', id='employee_position2')
    employee_salary2 = TextAreaField('employee_salary2', id='employee_salary2')

    employee_position3 = TextAreaField('employee_position3', id='employee_position3')
    employee_salary3 = TextAreaField('employee_salary3', id='employee_salary3')

    employee_position4 = TextAreaField('employee_position4', id='employee_position4')
    employee_salary4 = TextAreaField('employee_salary4', id='employee_salary4')

    employee_position5 = TextAreaField('employee_position5', id='employee_position5')
    employee_salary5 = TextAreaField('employee_salary5', id='employee_salary5')

    employee_position6 = TextAreaField('employee_position6', id='employee_position6')
    employee_salary6 = TextAreaField('employee_salary6', id='employee_salary6')

    employee_position7 = TextAreaField('employee_position7', id='employee_position7')
    employee_salary7 = TextAreaField('employee_salary7', id='employee_salary7')

    employee_position8 = TextAreaField('employee_position8', id='employee_position8')
    employee_salary8 = TextAreaField('employee_salary8', id='employee_salary8')

    employee_position9 = TextAreaField('employee_position9', id='employee_position9')
    employee_salary9 = TextAreaField('employee_salary9', id='employee_salary9')

    employee_position10 = TextAreaField('employee_position10', id='employee_position10')
    employee_salary10 = TextAreaField('employee_salary10', id='employee_salary10')

    employee_position11 = TextAreaField('employee_position11', id='employee_position11')
    employee_salary11 = TextAreaField('employee_salary11', id='employee_salary11')

    employee_position12 = TextAreaField('employee_position12', id='employee_position12')
    employee_salary12 = TextAreaField('employee_salary12', id='employee_salary12')

    employee_position13 = TextAreaField('employee_position13', id='employee_position13')
    employee_salary13 = TextAreaField('employee_salary13', id='employee_salary13')

    employee_position14 = TextAreaField('employee_position14', id='employee_position14')
    employee_salary14 = TextAreaField('employee_salary14', id='employee_salary14')








    permanent_expenditure_name0 = create_field_fm("permanent_expenditure_name0")
    permanent_expenditure0 = create_field_fm("permanent_expenditure0")

    permanent_expenditure_name1 = TextAreaField('permanent_expenditure_name1', id='permanent_expenditure_name1')
    permanent_expenditure1 = TextAreaField('permanent_expenditure1', id='permanent_expenditure1')

    permanent_expenditure_name2 = TextAreaField('permanent_expenditure_name2', id='permanent_expenditure_name2')
    permanent_expenditure2 = TextAreaField('permanent_expenditure2', id='permanent_expenditure2')

    permanent_expenditure_name3 = TextAreaField('permanent_expenditure_name3', id='permanent_expenditure_name3')
    permanent_expenditure3 = TextAreaField('permanent_expenditure3', id='permanent_expenditure3')

    permanent_expenditure_name4 = TextAreaField('permanent_expenditure_name4', id='permanent_expenditure_name4')
    permanent_expenditure4 = TextAreaField('permanent_expenditure4', id='permanent_expenditure4')

    permanent_expenditure_name5 = TextAreaField('permanent_expenditure_name5', id='permanent_expenditure_name5')
    permanent_expenditure5 = TextAreaField('permanent_expenditure5', id='permanent_expenditure5')

    permanent_expenditure_name6 = TextAreaField('permanent_expenditure_name6', id='permanent_expenditure_name6')
    permanent_expenditure6 = TextAreaField('permanent_expenditure6', id='permanent_expenditure6')

    permanent_expenditure_name7 = TextAreaField('permanent_expenditure_name7', id='permanent_expenditure_name7')
    permanent_expenditure7 = TextAreaField('permanent_expenditure7', id='permanent_expenditure7')

    permanent_expenditure_name8 = TextAreaField('permanent_expenditure_name8', id='permanent_expenditure_name8')
    permanent_expenditure8 = TextAreaField('permanent_expenditure8', id='permanent_expenditure8')

    permanent_expenditure_name9 = TextAreaField('permanent_expenditure_name9', id='permanent_expenditure_name9')
    permanent_expenditure9 = TextAreaField('permanent_expenditure9', id='permanent_expenditure9')

    permanent_expenditure_name10 = TextAreaField('permanent_expenditure_name10', id='permanent_expenditure_name10')
    permanent_expenditure10 = TextAreaField('permanent_expenditure10', id='permanent_expenditure10')

    permanent_expenditure_name11 = TextAreaField('permanent_expenditure_name11', id='permanent_expenditure_name11')
    permanent_expenditure11 = TextAreaField('permanent_expenditure11', id='permanent_expenditure11')

    permanent_expenditure_name12 = TextAreaField('permanent_expenditure_name12', id='permanent_expenditure_name12')
    permanent_expenditure12 = TextAreaField('permanent_expenditure12', id='permanent_expenditure12')

    permanent_expenditure_name13 = TextAreaField('permanent_expenditure_name13', id='permanent_expenditure_name13')
    permanent_expenditure13 = TextAreaField('permanent_expenditure13', id='permanent_expenditure13')

    permanent_expenditure_name14 = TextAreaField('permanent_expenditure_name14', id='permanent_expenditure_name14')
    permanent_expenditure14 = TextAreaField('permanent_expenditure14', id='permanent_expenditure14')








    variable_expenditure_name0 = create_field_fm("variable_expenditure_name0")
    variable_expenditure0 = create_field_fm("variable_expenditure0")

    variable_expenditure_name1 = TextAreaField('variable_expenditure_name1', id='variable_expenditure_name1')
    variable_expenditure1 = TextAreaField('variable_expenditure1', id='variable_expenditure1')

    variable_expenditure_name2 = TextAreaField('variable_expenditure_name2', id='variable_expenditure_name2')
    variable_expenditure2 = TextAreaField('variable_expenditure2', id='variable_expenditure2')

    variable_expenditure_name3 = TextAreaField('variable_expenditure_name3', id='variable_expenditure_name3')
    variable_expenditure3 = TextAreaField('variable_expenditure3', id='variable_expenditure3')

    variable_expenditure_name4 = TextAreaField('variable_expenditure_name4', id='variable_expenditure_name4')
    variable_expenditure4 = TextAreaField('variable_expenditure4', id='variable_expenditure4')

    variable_expenditure_name5 = TextAreaField('variable_expenditure_name5', id='variable_expenditure_name5')
    variable_expenditure5 = TextAreaField('variable_expenditure5', id='variable_expenditure5')

    variable_expenditure_name6 = TextAreaField('variable_expenditure_name6', id='variable_expenditure_name6')
    variable_expenditure6 = TextAreaField('variable_expenditure6', id='variable_expenditure6')

    variable_expenditure_name7 = TextAreaField('variable_expenditure_name7', id='variable_expenditure_name7')
    variable_expenditure7 = TextAreaField('variable_expenditure7', id='variable_expenditure7')

    variable_expenditure_name8 = TextAreaField('variable_expenditure_name8', id='variable_expenditure_name8')
    variable_expenditure8 = TextAreaField('variable_expenditure8', id='variable_expenditure8')

    variable_expenditure_name9 = TextAreaField('variable_expenditure_name9', id='variable_expenditure_name9')
    variable_expenditure9 = TextAreaField('variable_expenditure9', id='variable_expenditure9')

    variable_expenditure_name10 = TextAreaField('variable_expenditure_name10', id='variable_expenditure_name10')
    variable_expenditure10 = TextAreaField('variable_expenditure10', id='variable_expenditure10')

    variable_expenditure_name11 = TextAreaField('variable_expenditure_name11', id='variable_expenditure_name11')
    variable_expenditure11 = TextAreaField('variable_expenditure11', id='variable_expenditure11')

    variable_expenditure_name12 = TextAreaField('variable_expenditure_name12', id='variable_expenditure_name12')
    variable_expenditure12 = TextAreaField('variable_expenditure12', id='variable_expenditure12')

    variable_expenditure_name13 = TextAreaField('variable_expenditure_name13', id='variable_expenditure_name13')
    variable_expenditure13 = TextAreaField('variable_expenditure13', id='variable_expenditure13')

    variable_expenditure_name14 = TextAreaField('variable_expenditure_name14', id='variable_expenditure_name14')
    variable_expenditure14 = TextAreaField('variable_expenditure14', id='variable_expenditure14')

    variable_expenditure_name15 = TextAreaField('variable_expenditure_name15', id='variable_expenditure_name15')
    variable_expenditure15 = TextAreaField('variable_expenditure15', id='variable_expenditure15')

    variable_expenditure_name16 = TextAreaField('variable_expenditure_name16', id='variable_expenditure_name16')
    variable_expenditure16 = TextAreaField('variable_expenditure16', id='variable_expenditure16')

    variable_expenditure_name17 = TextAreaField('variable_expenditure_name17', id='variable_expenditure_name17')
    variable_expenditure17 = TextAreaField('variable_expenditure17', id='variable_expenditure17')

    variable_expenditure_name18 = TextAreaField('variable_expenditure_name18', id='variable_expenditure_name18')
    variable_expenditure18 = TextAreaField('variable_expenditure18', id='variable_expenditure18')

    variable_expenditure_name19 = TextAreaField('variable_expenditure_name19', id='variable_expenditure_name19')
    variable_expenditure19 = TextAreaField('variable_expenditure19', id='variable_expenditure19')

    variable_expenditure_name20 = TextAreaField('variable_expenditure_name20', id='variable_expenditure_name20')
    variable_expenditure20 = TextAreaField('variable_expenditure20', id='variable_expenditure20')

    variable_expenditure_name21 = TextAreaField('variable_expenditure_name21', id='variable_expenditure_name21')
    variable_expenditure21 = TextAreaField('variable_expenditure21', id='variable_expenditure21')

    variable_expenditure_name22 = TextAreaField('variable_expenditure_name22', id='variable_expenditure_name22')
    variable_expenditure22 = TextAreaField('variable_expenditure22', id='variable_expenditure22')

    variable_expenditure_name23 = TextAreaField('variable_expenditure_name23', id='variable_expenditure_name23')
    variable_expenditure23 = TextAreaField('variable_expenditure23', id='variable_expenditure23')

    variable_expenditure_name24 = TextAreaField('variable_expenditure_name24', id='variable_expenditure_name24')
    variable_expenditure24 = TextAreaField('variable_expenditure24', id='variable_expenditure24')

    variable_expenditure_name25 = TextAreaField('variable_expenditure_name25', id='variable_expenditure_name25')
    variable_expenditure25 = TextAreaField('variable_expenditure25', id='variable_expenditure25')

    variable_expenditure_name26 = TextAreaField('variable_expenditure_name26', id='variable_expenditure_name26')
    variable_expenditure26 = TextAreaField('variable_expenditure26', id='variable_expenditure26')

    variable_expenditure_name27 = TextAreaField('variable_expenditure_name27', id='variable_expenditure_name27')
    variable_expenditure27 = TextAreaField('variable_expenditure27', id='variable_expenditure27')

    variable_expenditure_name28 = TextAreaField('variable_expenditure_name28', id='variable_expenditure_name28')
    variable_expenditure28 = TextAreaField('variable_expenditure28', id='variable_expenditure28')

    variable_expenditure_name29 = TextAreaField('variable_expenditure_name29', id='variable_expenditure_name29')
    variable_expenditure29 = TextAreaField('variable_expenditure29', id='variable_expenditure29')



    product1_name = create_field_fm("product1_name")
    product1_price = create_field_fm("product1_price")
    product1_expenditure_increase = create_field_fm("product1_expenditure_increase")
    product1_sales = create_field_fm("product1_sales")
    product1_sales_increase = create_field_fm("product1_sales_increase")


    product2_name = create_field_fm("product2_name")
    product2_price = create_field_fm("product2_price")
    product2_expenditure_increase = create_field_fm("product2_expenditure_increase")
    product2_sales = create_field_fm("product2_sales")
    product2_sales_increase = create_field_fm("product2_sales_increase")







class bpForm(FlaskForm):
    project_name = create_field("project_name")
    businessman_name = create_field("businessman_name")
    capital_distribution = create_field("capital_distribution")
    address = create_field("address")
    website = create_field("website")
    self_investment = create_field("self_investment")
    your_product = create_field("your_product")
    start_deadline = create_field("start_deadline")
    problem = create_field("problem")
    solution = create_field("solution")
    innovation = create_field("innovation")
    patents = create_field("patents")
    business_model = create_field("business_model")
    resources = create_field("resources")
    analysis = create_field("analysis")
    competitors = create_field("competitors")
    competitor1 = TextAreaField('competitor1', id='competitor1'   , validators=[DataRequired()])
    competitor2 = TextAreaField('competitor2', id='competitor2'   , validators=[DataRequired()])
    competitor3 = TextAreaField('competitor3', id='competitor3'   , validators=[DataRequired()])
    competitor1value1 = TextAreaField('competitor1value1', id='competitor1value1'   , validators=[DataRequired()])
    competitor2value1 = TextAreaField('competitor2value1', id='competitor2value1'   , validators=[DataRequired()])
    competitor3value1 = TextAreaField('competitor3value1', id='competitor3value1'   , validators=[DataRequired()])
    competitor1value2 = TextAreaField('competitor1value1', id='competitor1value2'   , validators=[DataRequired()])
    competitor2value2 = TextAreaField('competitor2value1', id='competitor2value2'   , validators=[DataRequired()])
    competitor3value2 = TextAreaField('competitor3value1', id='competitor3value2'   , validators=[DataRequired()])
    competitor1value3 = TextAreaField('competitor1value1', id='competitor1value3'   , validators=[DataRequired()])
    competitor2value3 = TextAreaField('competitor2value1', id='competitor2value3'   , validators=[DataRequired()])
    competitor3value3 = TextAreaField('competitor3value1', id='competitor3value3'   , validators=[DataRequired()])
    competitor1value4 = TextAreaField('competitor1value1', id='competitor1value4'   , validators=[DataRequired()])
    competitor2value4 = TextAreaField('competitor2value1', id='competitor2value4'   , validators=[DataRequired()])
    competitor3value4 = TextAreaField('competitor3value1', id='competitor3value4'   , validators=[DataRequired()])
    advantage1 = TextAreaField('advantage1', id='advantage1'   , validators=[DataRequired()])
    advantage2 = TextAreaField('advantage1', id='advantage1'   , validators=[DataRequired()])
    advantage3 = TextAreaField('advantage1', id='advantage1'   , validators=[DataRequired()])
    advantage4 = TextAreaField('advantage1', id='advantage1'   , validators=[DataRequired()]) 
    strategy = create_field("strategy")
    team = create_field("team")
    experience = create_field("experience")
    organizational_structure = create_field("organizational_structure")
    strength = create_field("strength")
    weakness = create_field("weakness")
    possibility = create_field("possibility")
    threat = create_field("threat")
    realization_plan = create_field("realization_plan")
    investment_before = create_field("investment_before")
    financial_effectivity = create_field("financial_effectivity")
    conclusion = create_field("conclusion")
    
#     start_deadline = create_field("project_name")


    
#    address = TextAreaField('Юридический адрес', render_kw={"rows":1, "onkeypress":"auto_grow(this);", "onkeyup":"auto_grow(this);", "style":"margin-top:20px;resize:vertical;"}, id='address', validators=[DataRequired()])
#     website = TextField('Сайт (при наличии)', render_kw={"rows":1, "onkeypress":"auto_grow(this);", "onkeyup":"auto_grow(this);", "style":"margin-top:20px;resize:vertical;"}, id='website', validators=[DataRequired()])
#     self_investment = TextField('Наличие основных средств и необходимых площадей', render_kw={"rows":1, "onkeypress":"auto_grow(this);", "onkeyup":"auto_grow(this);", "style":"margin-top:20px;resize:vertical;"}, id='self_investment', validators=[DataRequired()])
#     your_product = TextAreaField('Предполагаемая к выпуску продукция (товар, услуга) или бизнес-процесс', render_kw={"rows":1, "onkeypress":"auto_grow(this);", "onkeyup":"auto_grow(this);", "style":"margin-top:20px;resize:vertical;"}, id='your_product', validators=[DataRequired()])
    # start_deadline = TextAreaField('Предполагаемый срок запуска проекта с момента получения гранта', render_kw={"rows":1, "placeholder":"test", "onkeypress":"auto_grow(this);", "onkeyup":"auto_grow(this);", "style":"margin-top:20px;resize:vertical;"}, id='start_deadline', validators=[DataRequired()])
    bp_submit = SubmitField("Сгенерировать БП")

class MaintenanceForm(FlaskForm):
    name = StringField('name', id='name'   , validators=[DataRequired()])
    phone_number = StringField('phone_number', id='phone_number'        , validators=[DataRequired()])
    phone_number_again = StringField('phone_number_again', id='phone_number_again'        , validators=[DataRequired()])
    have_idea = StringField('have_idea', id='have_idea'        , validators=[DataRequired()])
    your_sphere = StringField('your_sphere', id='your_sphere')




class ConsultingForm(FlaskForm):
    name = StringField('name', id='name'   , validators=[DataRequired()])
    phone_number = StringField('phone_number', id='phone_number'        , validators=[DataRequired()])
    phone_number_again = StringField('phone_number_again', id='phone_number_again'        , validators=[DataRequired()])
    question = StringField('question', id='question'        , validators=[DataRequired()])