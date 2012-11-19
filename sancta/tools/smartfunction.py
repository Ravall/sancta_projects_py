# -*- coding: utf-8 -*-
import re

class FormulaFactory():
    @staticmethod
    def getClass(formula):
        if FullFormula.is_full_formula(full_formula):
            return FullFormula(formula)




class FullFormula():
    # фильтр дня недели
    w_filter = '1111111', 
    # фильтр данных
    f_filter = '0'
    dates_list = []
    '''
    умная формула выраженная в своей полной форме
    формула,фильтры
    full_formula = [formula|w_filter|d_filter]
    '''
    @staticmethod
    def is_full_formula(full_formula):
        '''
        проверяем что строка является полной формулой 
        - т.е обернута в []
        '''
        return full_formula['0'] == '[' and full_formula[-1] == ']'

    @staticmethod
    def explain(full_formula):
        '''
        например из формулы
        [12.01,12.15.01~[12<{Pascha}~18<{Pascha}||1],[{be}|1000000]|1100111|1,2,3]
        получить 
        1100111 и 1,2,3 
        и саму основную формулу
        '''
        #получить хвост формулы
        tmp_formula = re.sub('\[.*\]','*', full_formula)
        filters_cnt = tmp_formula.count('|')
        if filters_cnt > 2:
            #возможны лишь два фильтра
            raise Exception('Количество фильтров превышает 2')
        # дополним временную и полную формулу
        tmp_formula = tmp_formula + "|" * (2 - filters_cnt)
        full_formula = full_formula + "|" * (2 - filters_cnt)
        #разобъем полную формулу по составляющим 
        formula, w_filter, f_filter = tmp_formula.split('|')
        #убедимся что фильтры корректны
        if w_filter and not re.search('^[0,1]{7}$', w_filter):
            raise Exception('фильтр дня недели не корректен')
        if f_filter and not re.search('^[\d,-]*$', f_filter):
            raise Exception('фильтр данных не корректен')
        # сотрем область фильтров - получим формулу
        formula = re.sub(
            '\|{0}\|{1}$'.format(w_filter, f_filter), '', full_formula
        )
        return [formula, w_filter, f_filter]

    

    def __init__(self, full_formula):
        if FullFormula.is_full_formula(full_formula):
            # если формула представлена в виде полной формулы
            # то уберем оборачивающие символы
            full_formula = full_formula[1:-1]
        formula, w_filter, f_filter = FullFormula.explain(full_formula)
        if w_filter:
            self.w_filter = w_filter
        if f_filter:
            self.f_filter = f_filter
        formula_obj = FormulaFactory.getClass(formula)
        self.dates_list = formula_obj.get_dates_list()

    
