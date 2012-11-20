# -*- coding: utf-8 -*-
'''
**********************************************************************************************
    Формат вызова
    smart_date_function(formula, year);
    INPUT
        formula - Формула по которой будет выполнен поиск дат (обязательный)
        year    - Год, для которого будет выполнен поиск, по умолчанию - текущий. (необязательный)
    OUTPUT
        array    - Массив, каждый элемент которого также массив из трёх элементов
                   [0] - день, [1] - месяц, [2] - год.
                   Массив отсортирован по возрастанию.

----------------------------------------------------------------------------------------------

    Формула formula состоит из 3-х полей отделённых друг от друга символом "|".
    [поле дат|фильтр дня недели|фильтр данных]

    1. Поле дат.
        1.1 Даты задаются в формате ДД.ММ.ГГГГ. Если поле ГГГГ опущено, то считается, что
            оно равно year.
        1.2 Даты задаются в виде перечисления или интервала.
            1.2.1 Перечисление - несколько дат, с запятой между ними.
                  12.03.2011,14.04.2010,17.05
            1.2.2 Интервал - задаётся в виде "начальная дата"~"конечная дата".
                  12.04.2001~22.04.2001
            1.2.3 Возможна комбинация из перечисления и интервала.
                  21.10,22.11~5.12,15.12
        1.3 В поле дат может стоять формула. В этом случае сначала вычисляется она, затем
            результат её вычисления подставляется в исходную формулу. Уровень вложенности
            формул неограничен.
            [12.03,[14.01~14.02|1110001|-1,-2]|1110001|1,2,3]
        1.4 Вместо даты или интервала можно подставить функцию. Встроенная функция
            оформляется внутри фигурных скобок. В качестве аргумента функции может
            указываться год, для готорого она вызывается. Если год не указан, то
            тогда он считается равным $year. Регистр не важен.
            [{B}~01.02||]=[01.01~01.02]
            [{be(1927)}||]=[01.01.1927~31.12.1927||]
            [{Pascha(2012)}||] - Православная прасха в 2012 году.
        1.5 Смещение дат
            1.5.1 Смещение года. Если в дате год указан со знаком "+" или "-" то он интерпретируется
                  не как год, а как смещение относительно года $year.
                  13.10.-10 = 13.10.2001 ($year=2011)
                  21.12.+7  = 21.12.2018 ($year=2011)
            1.5.2 Смещение дней. Если дата начинается с "число>" или "число<" то такая дата сдвигается
                  вперед по времени (">") или назад по времени ("<") на "число" дней. "Число" может
                  быть отрицательным.
                  12>29.12.2001 = -12<29.12.2001 = 10.01.2002
                  2<1.11.1876 = -2>1.11.1876 = 30.10.1876

    2. Фильтр дня недели
       Фильтр может состоять из 7-ми символов "0" и "1" или быть пустым. Если фильтр не задан,
       то считается, что он равен "1111111". Фильтр указывает какие дни недели нужно оставить
       в выборке дат. Символы идут в порядке - "пн", "вт", - , "вс".
       0110000 - оставить в выборке только вторники и среды.

    3. Фильтр данных
       Фильтр определяет какие данные оставить, в зависимости от того, на каком месте в выборке
       они находятся. "0" - оставить всё. Отрицательные числа определяют какие данные оставить с
       конца выборки.
       1,-1 - оставить первую и последнюю дату.
       0,1,3 - оставить все даты.

    Примеры формул:
        [{BE(2001)},[{BE}||]|1000000|1,-1] - все понедельники за текущий и 2001 год
        [{BE(2001)},{BE()}|1000000|1,-1] - аналогично
'''
import re


class FormulaFactory():

    @staticmethod
    def getClass(formula):
        #если формула выражена полной формулой
        if FullFormula.is_formula(formula):
            return FullFormula(formula)
        #если форумула выражена перечислением
        if EnumFormula.is_formula(formula):
            return EnumFormula(formula)
        #если формула выражена диапазоном
        if DiapasonFormula.is_formula(formula):
            return DiapasonFormula(formula)
        #если формула выражена smart формулой
        if SmartFormula.is_formula(formula):
            return SmartFormula(formula)


class SmartFormula():
    '''
    умная формула выраженная смартформулой
    {be},{b}, {Pascha(1998)}
    '''
    @staticmethod
    def is_formula(formula):
        '''
        если фунция обернута в {}
        '''
        return formula[0] == '{' and formula[-1] == '}'

    def explain(formula):
        formula = formula[1:-1]


class DiapasonFormula():
    '''
    умная формула выраженная диапазоном
    formula1~formula2
    возможны лишь только две субформулы
    '''
    @staticmethod
    def is_formula(formula):
        '''
        проверяем является ли формула диапазоном
        '''
        level = 0
        sub_formules = 1
        for alfa in formula:
            if alfa == '[':
                level += 1
            if alfa == ']':
                level -= 1
            if alfa == '~' and not level:
                sub_formules += 1
        return sub_formules == 2

    @staticmethod
    def explain(formula):
        '''
        разбить на части
        '''
        level = 0
        formula1, formula2 = '', ''
        #записываем в формулу 1
        sub_formules = 1
        for alfa in formula:
            if alfa == '[':
                level += 1
            if alfa == ']':
                level -= 1
            if alfa == '~' and not level:
                sub_formules += 1
            elif sub_formules == 1:
                formula1 += alfa
            elif sub_formules == 2:
                formula2 += alfa
        return [formula1, formula2]

    def check(self):
        '''
        проверить что части - есть одиночные даты
        проверить что первое число меньше второго
        '''
        pass


class EnumFormula():
    '''
    умная формула выраженная в виде перечислений формул:
    formula1,formula2,formula3
    при этом formulaХ может быть формулой с любой формой
    '''
    @staticmethod
    def is_formula(formula):
        '''
        проверяем является ли формула перечислением
        '''
        level = 0
        for alfa in formula:
            if alfa == '[':
                level += 1
            if alfa == ']':
                level -= 1
            # если находится хотябы одна
            if alfa == ',' and not level:
                return True
        return False

    @staticmethod
    def explain(formula):
        '''
        развернем формулу
        например
        12.11,[11.02,[12.02]|1000000|1,2],15.01~14.05, [11.04~15,11.14|1000000|1,4],14.05
        должна разбится на
        12.11
        [11.02,[12.02]|1000000|1,2]
        15.01~14.05
        [11.04~15,11.14|1000000|1,4]
        14.05
        '''
        # избавимся от лишних пробелов
        formula = re.sub('\s', '', formula)
        sub_formules = []
        i, level = 0, 0

        for alfa in formula:
            if alfa == '[':
                level += 1
            if alfa == ']':
                level -= 1
            # если запятая и мы не ушли вглубь другой формулы
            # - то считаем, что началась новая форумал
            if alfa == ',' and not level:
                i += 1
            else:
                try:
                    sub_formules[i] += alfa
                except IndexError:
                    sub_formules.append(alfa)

        return sub_formules


class FullFormula():
    '''
    умная формула выраженная в своей полной форме
    формула,фильтры
    full_formula = [formula|w_filter|d_filter]
    '''
    # фильтр дня недели
    w_filter = '1111111',
    # фильтр данных
    f_filter = '0'
    formula = []

    @staticmethod
    def is_formula(full_formula):
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
        tmp_formula = re.sub('\[.*\]', '*', full_formula)
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
        if FullFormula.is_formula(full_formula):
            # если формула представлена в виде полной формулы
            # то уберем оборачивающие символы
            full_formula = full_formula[1:-1]
        self.formula, w_filter, f_filter = FullFormula.explain(full_formula)
        if w_filter:
            self.w_filter = w_filter
        if f_filter:
            self.f_filter = f_filter

    def get_dates_list(self):
        formula_obj = FormulaFactory.getClass(self.formula)
        self.dates_list = formula_obj.get_dates_list()
