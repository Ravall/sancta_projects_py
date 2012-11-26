# -*- coding: utf-8 -*-
from django.test import TestCase
from tools.testutil import data_provider

from tools.smartfunction import FullFormula, EnumFormula, DiapasonFormula,\
    SmartFormula, BlasFormula, BlasYearFormula, SimpleDateFormula,\
    FormulaException





class FullFormulaTest(TestCase):
    def provider_explain():
        return (
            ("12.01,12.15.01~[12<{Pascha}~18<{Pascha}||1]"
             ",[{be}|1000000]|1100111|1,2,3",
             '1100111', '1,2,3', '12.01,12.15.01~[12<{Pascha}~18<{Pascha}||1],[{be}|1000000]'),
            ('12.01~[12.02~13.04|100000]|1100001',
             '1100001', '', '12.01~[12.02~13.04|100000]'),
            ('19.01|1111111', '1111111', '', '19.01'),
            ('19.01||0', '', '0', '19.01'),
            ('12.01~[12.02~13.04|100000]', '', '', '12.01~[12.02~13.04|100000]'),
            ('19.01', '', '', '19.01'),
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
           # ('11.01|1|1|1', False, None),
           # ('11.01|1|1', False, None),
           # ('11.01|1111112|1', False, None),
           # ('11.01|1111111|1', True, None),
           # ('11.01|1111111|-1,1', True, None),
           # ('11.01|1111111|', True, None),
            ('11.01||0', True, None),

        )

    @data_provider(provider_check)
    def test_check(self, formula, correct, year):
        try:
            formula_obj = FullFormula(formula)
            formula_obj.year = year
            formula_obj.check()
            is_correct = True
        except FormulaException:
            is_correct = False
        self.assertEquals(is_correct, correct)



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
            ('{be}', ['be', '']),
            ('{e(1900)}', ['e', '1900']),
        )

    @data_provider(provider_explain)
    def test_explain(self, formula, f_list):
        self.assertEquals(SmartFormula.explain(formula), f_list)

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
            ('12>{Pascha}', '12', '>', '{Pascha}'),
            ('-12<[12>11.02]', '-12', '<', '[12>11.02]'),
        )

    @data_provider(provider_explain)
    def test_explain(self, formula, days, operator, subformula):
        _days, _operator, _subformula = BlasFormula.explain(formula)
        self.assertEquals(days, _days)
        self.assertEquals(operator, _operator)
        self.assertEquals(subformula, _subformula)


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
            ('15.06', '15', '06', None),
        )

    @data_provider(provider_explain)
    def test_explain(self, formula, day, month, year):
        self.assertEquals(
            SimpleDateFormula.explain(formula), 
            [day, month, year]
        )
        



