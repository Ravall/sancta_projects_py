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
