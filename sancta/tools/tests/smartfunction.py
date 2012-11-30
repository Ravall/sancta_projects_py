# -*- coding: utf-8 -*-
from django.test import TestCase
from tools.testutil import data_provider
import tools.date as date
from tools.smartfunction import FullFormula, EnumFormula, DiapasonFormula,\
    SmartFormula, BlasFormula, BlasYearFormula, SimpleDateFormula,\
    FormulaException, Formula

class FormulaTest(TestCase):
    def test_sort_dates_list(self):
        # просто фейк-формула
        formula_obj = Formula('xxx')
        formula_obj.dates_list = [
            (1, 1, 1984), (1, 12, 1983), (3, 11, 1983),
            (5, 11, 1983), (10, 1, 1983), (1, 2, 1983),
            (11, 9, 1982)
        ]
        formula_obj.sort_dates_list()
        self.assertEquals(
            formula_obj.dates_list,
            [
                (11, 9, 1982), (10, 1, 1983), (1, 2, 1983),
                (3, 11, 1983), (5, 11, 1983), (1, 12, 1983),
                (1, 1, 1984),
            ],
            'получилось: {0}'.format(formula_obj.dates_list)
        )


class FullFormulaTest(TestCase):
    def provider_explain():
        return (
            ("12.01,12.15.01~[12<{Pascha}~18<{Pascha}||1]"
             ",[{be}|1000000]|1100111|1,2,3",
             '1100111', '1,2,3', '12.01,12.15.01~[12<{Pascha}~18<{Pascha}||1],[{be}|1000000]'),
            ('12.01~[12.02~13.04|100000]|1100001',
             '1100001', '0', '12.01~[12.02~13.04|100000]'),
            ('19.01|1111111', '1111111', '0', '19.01'),
            ('19.01||0', '1111111', '0', '19.01'),
            ('12.01~[12.02~13.04|100000]', '1111111', '0', '12.01~[12.02~13.04|100000]'),
            ('19.01', '1111111', '0', '19.01'),
        )

    @data_provider(provider_explain)
    def test_explain(self, full_formula, w_filter, d_filter, formula):
        frm, w_f, d_f = FullFormula.explain(full_formula)
        self.assertEquals(
            frm, formula,
            'в полной формуле {0} формула '
            'должна выйти {1}, но не {2}'.format(full_formula, formula, frm)
        )
        self.assertEquals(
            w_f, w_filter, 'в полной формуле {0} фильтр дней '
                           'должен выйти {1}, но не {2}'
                           .format(full_formula, w_filter, w_f)
        )
        self.assertEquals(
            d_f, d_filter, 'в полной формуле {0} фильтр данных '
                           'должен выйти {1}, но не {2}'
                           .format(full_formula, d_filter, d_f)
        )

    def provider_check():
        return (
            ('11.01|1|1|1', False),
            ('11.01|1|1', False),
            ('11.01||1,,2', False),
            ('11.01||1,--2', False),
            ('11.01|1111112|1', False),
            ('11.01|1111111|1', True),
            ('11.01|1111111|-1,1', True),
            ('11.01|1111111|', True),
            ('11.01|1111111|11,12', True),
            ('11.01||0', True),

        )

    @data_provider(provider_check)
    def test_check(self, formula, correct):
        try:
            formula_obj = FullFormula(formula)
            formula_obj.check(*FullFormula.explain(formula))
            is_correct = True
        except FormulaException:
            is_correct = False
        self.assertEquals(is_correct, correct)

    def provider_week_filter():
        return (
            (
                '1111111',
                [(1, 11, 1983), (2, 11, 1983), (3, 11, 1983)],
                [(1, 11, 1983), (2, 11, 1983), (3, 11, 1983)]
            ),
            (
                '0000000',
                [(1, 11, 1983), (2, 11, 1983), (3, 11, 1983)],
                []
            ),
            (
                '1010100',
                [
                    (19, 11, 2012), (20, 11, 2012), (21, 11, 2012),
                    (22, 11, 2012), (23, 11, 2012), (24, 11, 2012),
                    (25, 11, 2012)
                ],
                [
                    (19, 11, 2012), (21, 11, 2012), (23, 11, 2012)
                ],
            ),
            (
                '0000011',
                [
                    (19, 11, 2012), (20, 11, 2012), (21, 11, 2012),
                    (22, 11, 2012), (23, 11, 2012), (24, 11, 2012),
                    (25, 11, 2012), (26, 11, 2012), (27, 11, 2012),
                    (28, 11, 2012), (29, 11, 2012), (30, 11, 2012),
                    (1, 12, 2012), (2, 12, 2012)
                ],
                [
                    (24, 11, 2012), (25, 11, 2012), (1, 12, 2012),
                    (2, 12, 2012)
                ],
            )
        )

    @data_provider(provider_week_filter)
    def test_week_filter(self, w_filter, dates_list, result_dates_list):
        # инициируем объект FullFormula с фильтром.
        # сама формула не важна, потому как список дат мы ниже внедрим
        formula_obj = FullFormula('xxx')
        # внедрим список дат
        formula_obj.dates_list = dates_list
        formula_obj.week_filter(w_filter)
        self.assertEquals(
            result_dates_list, formula_obj.dates_list,
            'для фильтра {0} результат не верный. Получился {1}'.format(
                w_filter, formula_obj.dates_list
            )
        )

    def provider_data_filter():
        def week_dates():
            return [
                (19, 11, 2012), (20, 11, 2012), (21, 11, 2012),
                (22, 11, 2012), (23, 11, 2012), (24, 11, 2012),
                (25, 11, 2012)
            ]
        return (
            ('0,1,2,3', week_dates(), week_dates()),
            ('1', week_dates(), [(19, 11, 2012)]),
            ('1,2', week_dates(), [(19, 11, 2012), (20, 11, 2012)]),
            ('-1,2', week_dates(), [(20, 11, 2012), (25, 11, 2012)]),
        )

    @data_provider(provider_data_filter)
    def test_data_filter(self, d_filter, dates_list, result_dates_list):
        #аналогично test_week_filter
        formula_obj = FullFormula('xxx')
        formula_obj.dates_list = dates_list
        formula_obj.data_filter(d_filter)
        self.assertEquals(result_dates_list, formula_obj.dates_list)

    def provider_generatelist():
        return (
            (
                '[29.10~4.11|0000011]', 2012,
                [(3, 11, 2012), (4, 11, 2012)]
            ),
            (
                '29.10~4.11|0100011|1,2', 2012,
                [
                    (30, 10, 2012), (3, 11, 2012)
                ]
            ),
        )

    @data_provider(provider_generatelist)
    def test_generatelist(self, formula, year, dates_list):
        formula_obj = FullFormula(formula, year)
        try:
            formula_obj.generatelist()
            d_list = formula_obj.dates_list
        except FormulaException:
            d_list = False
        self.assertEquals(d_list, dates_list)


class EnumFormulaTest(TestCase):
    def provider_explain():
        return (
            ('12.11,[11.02,[12.02]|1000000|1,2],15.01~14.05,'
             ' [11.04~15,11.14|1000000|1,4],14.05',
             ['12.11', '[11.02,[12.02]|1000000|1,2]',
              '15.01~14.05', '[11.04~15,11.14|1000000|1,4]', '14.05']),
            ('11.11', ['11.11']),
            ('11.11~[11.11||1,2]', ['11.11~[11.11||1,2]']),
        )

    @data_provider(provider_explain)
    def test_explain(self, formula, f_list):
        self.assertEquals(EnumFormula.explain(formula), f_list)

    def provider_is_formula():
        return (
            ('11.11,12.11', True),
            ('11.11~[12.11,12.11]', False),
            ('[12.11,12.11]~[12,12||1,2]', False),
            ('[12.11,12.11]~[12,12||1,2],11.12', True),
            ('11.11~12.11~13.11', False),
        )

    @data_provider(provider_is_formula)
    def test_is_formula(self, formula, result):
        self.assertEquals(EnumFormula.is_formula(formula), result)

    def provider_generatelist():
        c_year = date.get_current_year()
        return (
            (
                '12.01,14.01', 2010,
                [(12, 1, 2010), (14, 1, 2010)]
            ),
            (
                '[30.01~3.02],5.02', 2010,
                [
                    (30, 1, 2010), (31, 1, 2010), (1, 2, 2010),
                    (2, 2, 2010), (3, 2, 2010), (5, 2, 2010)
                ]
            ),
            (
                '{b},3.01', None,
                [
                    (1, 1, c_year), (3, 1, c_year)
                ]
            ),
        )

    @data_provider(provider_generatelist)
    def test_generatelist(self, formula, year, dates_list):
        formula_obj = EnumFormula(formula, year)
        try:
            formula_obj.generatelist()
            d_list = formula_obj.dates_list
        except FormulaException:
            d_list = False
        self.assertEquals(d_list, dates_list)


class DiapasonFormulaTest(TestCase):
    def provider_is_formula():
        return (
            ('11.11,12.11', False),
            ('11.11~[12.11,12.11]', True),
            ('[12.11,12.11]~[12,12||1,2]', True),
            ('11.11~12.11~13.11', False),
            ('11.11~12.11', True),
        )

    @data_provider(provider_is_formula)
    def test_is_formula(self, formula, result):
        self.assertEquals(DiapasonFormula.is_formula(formula), result)

    def provider_explain():
        return (
            ('12>12.01~11.02', ['12>12.01', '11.02']),
            ('[11.12~15.12]~[20.12~21.12]', ['[11.12~15.12]', '[20.12~21.12]']),
        )

    @data_provider(provider_explain)
    def test_explain(self, formula, f_list):
        self.assertEquals(DiapasonFormula.explain(formula), f_list)

    def provider_check():
        return (
            (
                [(1, 11, 1983), (2, 11, 1983)],
                [(3, 11, 1983), (4, 11, 1983)],
                False
            ),
            (
                [(1, 11, 1983)],
                [(3, 11, 1983), (4, 11, 1983)],
                False
            ),
            (
                [(1, 11, 1983), (2, 11, 1983)],
                [(4, 11,1983)],
                False
            ),
            (
                [(4, 11, 1983)],
                [(3, 11, 1983)],
                False
            ),
            (
                [(3, 11, 1983)],
                [(3, 11, 1983)],
                False
            ),
            (
                [(1, 11, 1983)],
                [(3, 11, 1983)],
                True
            ),
        )

    @data_provider(provider_check)
    def test_check(self, date_list1, date_list2, correct):
        try:
            #просто левая формула
            formula_obj = DiapasonFormula('12.01~13.01')
            formula_obj.check(date_list1, date_list2)
            is_correct = True
        except FormulaException:
            is_correct = False
        self.assertEquals(is_correct, correct)


    def provider_generate_list():
        return (
            (
                (3, 11, 1983), (5, 11, 1983),
                [(3, 11, 1983), (4, 11, 1983), (5, 11, 1983)]
            ),
            (
                (3, 11, 1983), (4, 11, 1983),
                [(3, 11, 1983), (4, 11, 1983)]
            ),
            (
                (29, 11, 1983), (4, 12, 1983),
                [
                    (29, 11, 1983), (30, 11, 1983), (1, 12, 1983),
                    (2, 12, 1983), (3, 12, 1983), (4, 12, 1983)
                ]
            ),
            (
                (26, 2, 2011), (2, 3, 2011),
                [
                    (26, 2, 2011), (27, 2, 2011), (28, 2, 2011),
                    (1, 3, 2011), (2, 3, 2011),
                ]
            ),
            (
                (26, 2, 2000), (2, 3, 2000),
                [
                    (26, 2, 2000), (27, 2, 2000), (28, 2, 2000),
                    (29, 2, 2000), (1, 3, 2000), (2, 3, 2000),
                ]
            ),
        )

    @data_provider(provider_generate_list)
    def test_diapason(self, date1, date2, dates_list):
        #просто левая формула
        formula_obj = DiapasonFormula('12.01~13.01')
        formula_obj.diapason([date1], [date2])
        self.assertEquals(formula_obj.dates_list, dates_list)

    def provider_generatelist():
        c_year = date.get_current_year()
        return (
            (
                '12.01~14.01', 2010,
                [(12, 1, 2010), (13, 1, 2010), (14, 1, 2010)]
            ),
            (
                '30.01~3.02', 2010,
                [
                    (30, 1, 2010), (31, 1, 2010), (1, 2, 2010),
                    (2, 2, 2010), (3, 2, 2010)
                ]
            ),
            (
                '{b}~3.01', None,
                [
                    (1, 1, c_year), (2, 1, c_year), (3, 1, c_year)
                ]
            ),
            (
                '10<11.12~3.12', 2010,
                [(1, 12, 2010), (2, 12, 2010), (3, 12, 2010)]
            ),

        )

    @data_provider(provider_generatelist)
    def test_generatelist(self, formula, year, dates_list):
        formula_obj = DiapasonFormula(formula, year)
        try:
            formula_obj.generatelist()
            d_list = formula_obj.dates_list
        except FormulaException:
            d_list = False
        self.assertEquals(d_list, dates_list)



class SmartFormulaTest(TestCase):
    def provider_is_formula():
        return (
            ('{xxx}', True),
            ('{xx(1)}', True),
            ('xx}', False),
            ('{xx)', False),
        )

    @data_provider(provider_is_formula)
    def test_is_formula(self, formula, result):
        self.assertEquals(SmartFormula.is_formula(formula), result)

    def provider_explain():
        return (
            ('{be}', ['be', None]),
            ('{e(1900)}', ['e', '1900']),
        )

    @data_provider(provider_explain)
    def test_explain(self, formula, f_list):
        self.assertEquals(SmartFormula.explain(formula), f_list)

    def provider_generatelist():
        return (
            ('{b}', 2010, [(1, 1, 2010)]),
            ('{b(2011)}', 2010, [(1, 1, 2011)]),
            ('{e}', None, [(31, 12, date.get_current_year())]),
            ('{e(2000)}', None, [(31, 12, 2000)]),
            ('{Pascha}', 2000, [date.Pascha(2000)]),
            ('{Pascha}', None, [date.Pascha(date.get_current_year())]),
        )

    @data_provider(provider_generatelist)
    def test_generatelist(self, formula, year, dates_list):
        formula_obj = SmartFormula(formula, year)
        try:
            formula_obj.generatelist()
            d_list = formula_obj.dates_list
        except FormulaException:
            d_list = False
        self.assertEquals(d_list, dates_list)


class BlasFormulaTest(TestCase):
    def provider_is_formula():
        return (
            ('12>{Pascha}', True),
            ('-12>[12>11.02]', True),
            ('12>{Pascha}>11', False),
            ('11.12>11', False),
        )

    @data_provider(provider_is_formula)
    def test_is_formula(self, formula, result):
        message = 'формула {0} должна быть {1}'.format(
            formula,
            'корректной' if result else 'не корректной',
        )
        self.assertEquals(BlasFormula.is_formula(formula), result, message)

    def provider_explain():
        return (
            ('12>{Pascha}', 12, '{Pascha}'),
            ('12<{Pascha}', -12, '{Pascha}'),
            ('-12<[12>11.02]', 12, '[12>11.02]'),
            ('-12>[12>11.02]', -12, '[12>11.02]'),
        )

    @data_provider(provider_explain)
    def test_explain(self, formula, days, subformula):
        _days, _subformula = BlasFormula.explain(formula)
        self.assertEquals(days, _days)
        self.assertEquals(subformula, _subformula)

    def provider_generatelist():
        return (
            ('12>11.02', 2010, [(23, 2, 2010)]),
            ('20<11.02.+10', None, [(22, 1, date.get_current_year()+10)]),
            ('1>28.02', 2000, [(29, 2, 2000)]),
            ('2>28.02', 2000, [(1, 3, 2000)]),
        )

    @data_provider(provider_generatelist)
    def test_generatelist(self, formula, year, dates_list):
        formula_obj = BlasFormula(formula, year)
        try:
            formula_obj.generatelist()
            d_list = formula_obj.dates_list
        except FormulaException:
            d_list = False
        self.assertEquals(d_list, dates_list)

class BlasYearFormulaTest(TestCase):
    def provider_is_formula():
        return (
            ('01.12.+7', True),
            ('15.06.-1', True),
            ('15.06-1', False),
            ('15.06.11', False),
        )

    @data_provider(provider_is_formula)
    def test_is_formula(self, formula, result):
        message = 'формула {0} должна быть {1}'.format(
            formula,
            'корректной' if result else 'не корректной',
        )
        self.assertEquals(BlasYearFormula.is_formula(formula), result, message)

    def provider_explain():
        return (
            ('01.12.+7', '01.12', '+7'),
            ('15.06.-1', '15.06', '-1'),
        )

    @data_provider(provider_explain)
    def test_explain(self, formula, subformula, year):
        _subformula, _year = BlasYearFormula.explain(formula)
        self.assertEquals(year, _year)
        self.assertEquals(subformula, _subformula)

    def provider_generatelist():
        return (
            ('11.02.+1', 2010, [(11, 2, 2011)]),
            ('11.02.-2', '2010', [(11, 2, 2008)]),
            ('11.02.+10', None, [(11, 2, date.get_current_year()+10)]),
            ('29.02.+1', 1999, [(29, 2, 2000)]),
            ('29.02.-1', 2000, False),
        )

    @data_provider(provider_generatelist)
    def test_generatelist(self, formula, year, dates_list):
        formula_obj = BlasYearFormula(formula, year)
        try:
            formula_obj.generatelist()
            d_list = formula_obj.dates_list
        except FormulaException:
            d_list = False
        self.assertEquals(d_list, dates_list)


class SimpleDateFormulaTest(TestCase):
    def provider_is_formula():
        return (
            ('11.01.2011', True),
            ('3.11', True),
            ('3.11.12', False),
            ('3.11.', False),
        )

    @data_provider(provider_is_formula)
    def test_is_formula(self, formula, result):
        message = 'формула {0} должна быть {1}'.format(
            formula,
            'корректной' if result else 'не корректной',
        )
        self.assertEquals(SimpleDateFormula.is_formula(formula), result, message)

    def provider_explain():
        return (
            ('11.01.2011', '11', '01', '2011'),
            ('15.06', '15', '06', '0'),
        )

    @data_provider(provider_explain)
    def test_explain(self, formula, day, month, year):
        self.assertEquals(
            SimpleDateFormula.explain(formula),
            [day, month, year]
        )

    def provider_generatelist():
        return (
            ('11.02', 2010, [(11, 2, 2010)]),
            ('11.02', '2010', [(11, 2, 2010)]),
            ('11.02', None, [(11, 2, date.get_current_year())]),
            ('29.02', 2000, [(29, 2, 2000)]),
            ('29.02', 2001, False),
        )

    @data_provider(provider_generatelist)
    def test_generatelist(self, formula, year, dates_list):
        formula_obj = SimpleDateFormula(formula, year)
        try:
            formula_obj.generatelist()
            d_list = formula_obj.dates_list
        except FormulaException:
            d_list = False
        self.assertEquals(d_list, dates_list)

class SmartFunctionTest(TestCase):
    def provider_function():
        c_year = date.get_current_year()
        return (
            #simple
            ('12.01', None, [(12, 1, c_year)]),
            ('[12.01]', None, [(12, 1, c_year)]),
            ('[28.03]', None, [(28, 3, c_year)]),
            ('[28.03.2010||]', None, [(28, 3, 2010)]),
            ('[28.03]', 2010, [(28, 3, 2010)]),
            ('[28.12.2010]', None, [(28, 3, 2010)]),
            ('[28.12,29.12]', None, [(28, 12, c_year), (29, 12, c_year)]),
            #посты
            (
                '28.11~06.01.+1', 2010,  
                get_period(28, 11, 2010, 6, 1, 2011)
            ), #рождественский пост
            (
                '28.11~06.01.+1', 2013, 
                $this->getPeriond('2013-11-28','2014-01-06')), //Рождественский пост
                array('14.08~27.08','2010',  $this->getPeriond('2010-08-14','2010-08-27')), //  Успенский пост
                array('14.08~27.08','2011',  $this->getPeriond('2011-08-14','2011-08-27')), //  Успенский пост
                array('57>{Pascha}~11.07', '2010', $this->getPeriond('2010-05-31','2010-07-11')), //Петров пост
                array('57>{Pascha}~11.07', '2011', $this->getPeriond('2011-06-20','2011-07-11')), //Петров пост
                array('48<{Pascha}~1<{Pascha}', '2011', $this->getPeriond('2011-03-07','2011-04-23')), // Великий пост
                array('48<{Pascha}~1<{Pascha}', '2012', $this->getPeriond('2012-02-27','2012-04-14')), // Великий пост
                // мясоеды
                array('28.08~27.11','2010', $this->getPeriond('2010-08-28','2010-11-27')), //Осенний мясоед
                array('28.08~27.11','2011', $this->getPeriond('2011-08-28','2011-11-27')), //Осенний мясоед
                array('28.08~27.11','2013', $this->getPeriond('2013-08-28','2013-11-27')), //Осенний мясоед
                array('07.01~49<{Pascha}', '2010', $this->getPeriond('2010-01-07','2010-02-14')), // зимний мясоед
                array('07.01~49<{Pascha}', '2011', $this->getPeriond('2011-01-07','2011-03-06')), // зимний мясоед
                array('07.01~49<{Pascha}', '2012', $this->getPeriond('2012-01-07','2012-02-26')), // зимний мясоед
                array('{Pascha}~56>{Pascha}', '2010', $this->getPeriond('2010-04-04','2010-05-30')), // Весенний мясоед
                array('{Pascha}~56>{Pascha}', '2011', $this->getPeriond('2011-04-24','2011-06-19')), // Весенний мясоед
                array('{Pascha}~56>{Pascha}', '2012', $this->getPeriond('2012-04-15','2012-06-10')), // Весенний мясоед
                array('12.07~13.08', '2010', $this->getPeriond('2010-07-12','2010-08-13')), // Летний мясоед
                array('12.07~13.08', '2011', $this->getPeriond('2011-07-12','2011-08-13')), // Летний мясоед
                array('12.07~13.08', '2012', $this->getPeriond('2012-07-12','2012-08-13')), // Летний мясоед
                // сплошные седмицы
                array('07.01~18.01', '2011', $this->getPeriond('2011-01-07', '2011-01-18')), // Святки
                array('07.01~18.01', '2012', $this->getPeriond('2012-01-07', '2012-01-18')), // Святки
                array('07.01~18.01', '2013', $this->getPeriond('2013-01-07', '2013-01-18')), // Святки
                array('69<{Pascha}~63<{Pascha}', '2011', $this->getPeriond('2011-02-14', '2011-02-20')), // седмица Мытаря и фарисея
                array('69<{Pascha}~63<{Pascha}', '2012', $this->getPeriond('2012-02-06', '2012-02-12')), // седмица Мытаря и фарисея
                array('69<{Pascha}~63<{Pascha}', '2013', $this->getPeriond('2013-02-25', '2013-03-03')), // седмица Мытаря и фарисея
                array('55<{Pascha}~49<{Pascha}', '2011', $this->getPeriond('2011-02-28', '2011-03-06')), // масленица
                array('55<{Pascha}~49<{Pascha}', '2012', $this->getPeriond('2012-02-20', '2012-02-26')), // масленица
                array('55<{Pascha}~49<{Pascha}', '2013', $this->getPeriond('2013-03-11', '2013-03-17')), // масленица
                array('{Pascha}~6>{Pascha}', '2011', $this->getPeriond('2011-04-24', '2011-04-30')), // Пасхальная седмица
                array('{Pascha}~6>{Pascha}', '2012', $this->getPeriond('2012-04-15', '2012-04-21')), // Пасхальная седмица
                array('{Pascha}~6>{Pascha}', '2013', $this->getPeriond('2013-05-05', '2013-05-11')), // Пасхальная седмица
                array('50>{Pascha}~56>{Pascha}', '2011', $this->getPeriond('2011-06-13', '2011-06-19')), // Троицкая седмица
                array('50>{Pascha}~56>{Pascha}', '2012', $this->getPeriond('2012-06-04', '2012-06-10')), // Троицкая седмица
                array('50>{Pascha}~56>{Pascha}', '2013', $this->getPeriond('2013-06-24', '2013-06-30')), // Троицкая седмица
                array('62<{Pascha}~56<{Pascha}', '2011', $this->getPeriond('2011-02-21', '2011-02-27')), // мясопустная седмица
                array('62<{Pascha}~56<{Pascha}', '2012', $this->getPeriond('2012-02-13', '2012-02-19')), // мясопустная седмица
                array('62<{Pascha}~56<{Pascha}', '2013', $this->getPeriond('2013-03-04', '2013-03-10')), // мясопустная седмица
                array('6<{Pascha}~1<{Pascha}', '2011', $this->getPeriond('2011-04-18', '2011-04-23')), // Страстная седмица
                array('6<{Pascha}~1<{Pascha}', '2012', $this->getPeriond('2012-04-09', '2012-04-14')), // Страстная седмица
                array('6<{Pascha}~1<{Pascha}', '2013', $this->getPeriond('2013-04-29', '2013-05-04')), // Страстная седмица
                // Страстная седмица
                array('6<{Pascha}', '2011', array('2011-04-18')), // Страстной понедельик
                array('5<{Pascha}', '2011', array('2011-04-19')), // Страстной вторник
                array('4<{Pascha}', '2011', array('2011-04-20')), // Страстной среда
                array('3<{Pascha}', '2011', array('2011-04-21')), // Страстной четверг
                array('2<{Pascha}', '2011', array('2011-04-22')), // Страстная пятница
                array('1<{Pascha}', '2011', array('2011-04-23')), // Страстная суббота
                // Великие праздники
                array('{Pascha}', '2010', array('2010-04-04')), // пасха
                array('{Pascha}', '2011', array('2011-04-24')), // пасха
                array('{Pascha}', '2012', array('2012-04-15')), // пасха
                array('{Pascha}', '2013', array('2013-05-05')), // пасха
                array('{Pascha}', '2014', array('2014-04-20')), // пасха
                array('{Pascha}', '2015', array('2015-04-12')), // пасха
                array('{Pascha}', '2016', array('2016-05-01')), // пасха
                array('{Pascha}', '2017', array('2017-04-16')), // пасха
                array('{Pascha}', '2018', array('2018-04-08')), // пасха
                array('{Pascha}', '2019', array('2019-04-28')), // пасха
                array('{Pascha}', '2020', array('2020-04-19')), // пасха
                array('21.09', '2010', array('2010-09-21')), //  Рождество Богородицы
                array('21.09', '2011', array('2011-09-21')), //  Рождество Богородицы
                array('21.09', '2012', array('2012-09-21')), //  Рождество Богородицы
                array('27.09', '2010', array('2010-09-27')), //  Водвижение креста господня
                array('27.09', '2011', array('2011-09-27')), //  Водвижение креста господня
                array('27.09', '2012', array('2012-09-27')), //  Водвижение креста господня
                array('04.12', '2010', array('2010-12-04')), //  Введение во храм Пресвятой Богородицы
                array('04.12', '2011', array('2011-12-04')), //  Введение во храм Пресвятой Богородицы
                array('04.12', '2012', array('2012-12-04')), //  Введение во храм Пресвятой Богородицы
                array('07.01', '2010', array('2010-01-07')), //  Рождество христово
                array('07.01', '2011', array('2011-01-07')), //  Рождество христово
                array('07.01', '2012', array('2012-01-07')), //  Рождество христово
                array('19.01', '2010', array('2010-01-19')), //  Крещение Господне
                array('19.01', '2011', array('2011-01-19')), //  Крещение Господне
                array('19.01', '2012', array('2012-01-19')), //  Крещение Господне
                array('15.02', '2010', array('2010-02-15')), //  Сретение Господне
                array('15.02', '2011', array('2011-02-15')), //  Сретение Господне
                array('15.02', '2012', array('2012-02-15')), //  Сретение Господне
                array('07.04', '2010', array('2010-04-07')), //  Благовещение Пресвятой Богородицы
                array('07.04', '2011', array('2011-04-07')), //  Благовещение Пресвятой Богородицы
                array('07.04', '2012', array('2012-04-07')), //  Благовещение Пресвятой Богородицы
                array('7<{Pascha}', '2010', array('2010-03-28')), //  Вход Господень в Иерусалим
                array('7<{Pascha}', '2011', array('2011-04-17')), //  Вход Господень в Иерусалим
                array('7<{Pascha}', '2012', array('2012-04-08')), //  Вход Господень в Иерусалим
                array('7<{Pascha}', '2013', array('2013-04-28')), //  Вход Господень в Иерусалим
                array('7<{Pascha}', '2014', array('2014-04-13')), //  Вход Господень в Иерусалим
                array('7<{Pascha}', '2015', array('2015-04-05')), //  Вход Господень в Иерусалим
                array('39>{Pascha}', '2010', array('2010-05-13')), //  Вознесение Господне
                array('39>{Pascha}', '2011', array('2011-06-02')), //  Вознесение Господне
                array('39>{Pascha}', '2012', array('2012-05-24')), //  Вознесение Господне
                array('39>{Pascha}', '2013', array('2013-06-13')), //  Вознесение Господне
                array('39>{Pascha}', '2014', array('2014-05-29')), //  Вознесение Господне
                array('39>{Pascha}', '2015', array('2015-05-21')), //  Вознесение Господне
                array('49>{Pascha}', '2010', array('2010-05-23')), //  День святой троицы
                array('49>{Pascha}', '2011', array('2011-06-12')), //  День святой троицы
                array('49>{Pascha}', '2012', array('2012-06-03')), //  День святой троицы
                array('49>{Pascha}', '2013', array('2013-06-23')), //  День святой троицы
                array('49>{Pascha}', '2014', array('2014-06-08')), //  День святой троицы
                array('49>{Pascha}', '2015', array('2015-05-31')), //  День святой троицы
                array('19.08', '2010', array('2010-08-19')), //  Преображение Господне
                array('19.08', '2011', array('2011-08-19')), //  Преображение Господне
                array('19.08', '2012', array('2012-08-19')), //  Преображение Господне
                array('28.08', '2010', array('2010-08-28')), //  Успение Пресвятой Богородицы
                array('28.08', '2011', array('2011-08-28')), //  Успение Пресвятой Богородицы
                array('28.08', '2012', array('2012-08-28')), //  Успение Пресвятой Богородицы
                array('14.10', '2010', array('2010-10-14')), //  Покров Пресвятой Богородицы
                array('14.10', '2011', array('2011-10-14')), //  Покров Пресвятой Богородицы
                array('14.10', '2012', array('2012-10-14')), //  Покров Пресвятой Богородицы
                array('14.01', '2010', array('2010-01-14')), //  Обрезание Господне
                array('14.01', '2011', array('2011-01-14')), //  Обрезание Господне
                array('14.01', '2012', array('2012-01-14')), //  Обрезание Господне
                array('07.07', '2010', array('2010-07-07')), //  Рождество Иоанна Предтечи
                array('07.07', '2011', array('2011-07-07')), //  Рождество Иоанна Предтечи
                array('07.07', '2012', array('2012-07-07')), //  Рождество Иоанна Предтечи
                array('12.07', '2010', array('2010-07-12')), //  День апостолов петра и павла
                array('12.07', '2011', array('2011-07-12')), //  День апостолов петра и павла
                array('12.07', '2012', array('2012-07-12')), //  День апостолов петра и павла
                array('11.09', '2010', array('2010-09-11')), //  Усекновение главы иона Предтечи
                array('11.09', '2011', array('2011-09-11')), //  Усекновение главы иона Предтечи
                array('11.09', '2012', array('2012-09-11')), //  Усекновение главы иона Предтечи
                
                array('06.01', '2011', array('2011-01-06')), //  Рождественский сочельник
                array('06.01', '2012', array('2012-01-06')), //  Рождественский сочельник

                array('18.01', '2011', array('2011-01-18')), //  Богоявленский сочельник
                array('18.01', '2012', array('2012-01-18')), //  Богоявленский сочельник

                // дни особого поминовения усопших
                array('57<{Pascha}', '2010', array('2010-02-06')), //  Мясопустная вселенская родительская суббота
                array('57<{Pascha}', '2011', array('2011-02-26')), //  Мясопустная вселенская родительская суббота
                array('57<{Pascha}', '2012', array('2012-02-18')), //  Мясопустная вселенская родительская суббота
                array('36<{Pascha},29<{Pascha},22<{Pascha}', '2010', array('2010-02-27', '2010-03-06', '2010-03-13')), //  Родительская вселенская суббота
                array('36<{Pascha},29<{Pascha},22<{Pascha}', '2011', array('2011-03-19', '2011-03-26', '2011-04-02')), //  Родительская вселенская суббота
                array('36<{Pascha},29<{Pascha},22<{Pascha}', '2012', array('2012-03-10', '2012-03-17', '2012-03-24')), //  Родительская вселенская суббота
                array('9>{Pascha}', '2010', array('2010-04-13')), //  Радоница
                array('9>{Pascha}', '2011', array('2011-05-03')), //  Радоница
                array('9>{Pascha}', '2012', array('2012-04-24')), //  Радоница
                array('09.05', '2010', array('2010-05-09')), //  9-го мая
                array('09.05', '2011', array('2011-05-09')), //  9-го мая
                array('09.05', '2012', array('2012-05-09')), //  9-го мая
                array('48>{Pascha}', '2010', array('2010-05-22')), //  Троицкая вселенская родительская суббота
                array('48>{Pascha}', '2011', array('2011-06-11')), //  Троицкая вселенская родительская суббота
                array('48>{Pascha}', '2012', array('2012-06-02')), //  Троицкая вселенская родительская суббота
                array('02.11~08.11|0000010', '2010', array('2010-11-06')), //  Димитриевская суббота
                array('02.11~08.11|0000010', '2011', array('2011-11-05')), //  Димитриевская суббота
                array('02.11~08.11|0000010', '2012', array('2012-11-03')), //  Димитриевская суббота
                // дни четырдесятницы
                array('70<{Pascha}', '2011', array('2011-02-13')), // Неделя мытаря и фарисея.
                array('70<{Pascha}', '2012', array('2012-02-05')), // Неделя мытаря и фарисея.
                array('70<{Pascha}', '2013', array('2013-02-24')), // Неделя мытаря и фарисея.

                array('63<{Pascha}', '2011', array('2011-02-20')), // Неделя о блудном сыне
                array('63<{Pascha}', '2012', array('2012-02-12')), // Неделя о блудном сыне
                array('63<{Pascha}', '2013', array('2013-03-03')), // Неделя о блудном сыне

                array('56<{Pascha}', '2011', array('2011-02-27')), // Неделя о Страшном суде. Заговенье на мясо
                array('56<{Pascha}', '2012', array('2012-02-19')), // Неделя о Страшном суде. Заговенье на мясо
                array('56<{Pascha}', '2013', array('2013-03-10')), // Неделя о Страшном суде. Заговенье на мясо

                array('49<{Pascha}', '2011', array('2011-03-06')), // Прощеное воскресенье - Неделя сыропустная
                array('49<{Pascha}', '2012', array('2012-02-26')), // Прощеное воскресенье - Неделя сыропустная
                array('49<{Pascha}', '2013', array('2013-03-17')), // Прощеное воскресенье - Неделя сыропустная
                
                array('42<{Pascha}', '2011', array('2011-03-13')), // тожество православия
                array('42<{Pascha}', '2012', array('2012-03-04')), // тожество православия
                array('42<{Pascha}', '2013', array('2013-03-24')), // тожество православия

                array('35<{Pascha}', '2011', array('2011-03-20')), // Неделя 2-я Великого поста - Святителя Григория Паламы
                array('35<{Pascha}', '2012', array('2012-03-11')), // Неделя 2-я Великого поста - Святителя Григория Паламы
                array('35<{Pascha}', '2013', array('2013-03-31')), // Неделя 2-я Великого поста - Святителя Григория Паламы

                array('28<{Pascha}', '2011', array('2011-03-27')), // Неделя 3-я Великого поста - Крестопоклонная
                array('28<{Pascha}', '2012', array('2012-03-18')), // Неделя 3-я Великого поста - Крестопоклонная
                array('28<{Pascha}', '2013', array('2013-04-07')), // Неделя 3-я Великого поста - Крестопоклонная

                array('21<{Pascha}', '2011', array('2011-04-03')), // Преподобного Иоанна Лествичника
                array('21<{Pascha}', '2012', array('2012-03-25')), // Преподобного Иоанна Лествичника
                array('21<{Pascha}', '2013', array('2013-04-14')), // Преподобного Иоанна Лествичника

                array('14<{Pascha}', '2011', array('2011-04-10')), // Преподобной Марии Египетской
                array('14<{Pascha}', '2012', array('2012-04-01')), // Преподобной Марии Египетской
                array('14<{Pascha}', '2013', array('2013-04-21')), // Преподобной Марии Египетской

                array('15<{Pascha}', '2011', array('2011-04-09')), // Суббота акафиста
                array('15<{Pascha}', '2012', array('2012-03-31')), // Суббота акафиста
                array('15<{Pascha}', '2013', array('2013-04-20')), // Суббота акафиста

                array('17<{Pascha}', '2011', array('2011-04-07')), // Марьино стояние
                array('17<{Pascha}', '2012', array('2012-03-29')), // Марьино стояние
                array('17<{Pascha}', '2013', array('2013-04-18')), // Марьино стояние

                array('8<{Pascha}', '2011', array('2011-04-16')), // Лазарева суббота
                array('8<{Pascha}', '2012', array('2012-04-07')), // Лазарева суббота
                array('8<{Pascha}', '2013', array('2013-04-27')), // Лазарева суббота
                array('01.05~31.05|0000001|-1', '2011', array('2011-05-29')), // последнее воскресенье мая
                array('01.05~31.05|0000001|-1', '2012', array('2012-05-27')), // последнее воскресенье мая
                array('01.10~31.10|0000001|-1', '2011', array('2011-10-30')), // последнее воскресенье октября
                array('01.10~31.10|0000001|-1', '2012', array('2012-10-28')), // последнее воскресенье октября
                array('[01.05~31.05|0000001|-1]~[01.10~31.10|0000001|-1]','2011', $this->getPeriond('2011-05-29','2011-10-30')),
            );
