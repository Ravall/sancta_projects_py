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
import tools.date as date


def smart_function(formula, year):
    '''
    основная функция
    '''
    try:
        formula_obj = FormulaFactory.getClass(formula, year)
        #получим
        formula_obj.process()
        formula_obj.generatelist()
        formula_obj.sort_dates_list()
        dates_list = formula_obj.dates_list
    except:
        dates_list = []
    return dates_list


class FormulaException(Exception):
    pass


class FormulaFactory():
    @staticmethod
    def getClass(formula, year):
        #если формула выражена полной формулой
        if FullFormula.is_formula(formula):
            return FullFormula(formula, year)
        #если форумула выражена перечислением
        if EnumFormula.is_formula(formula):
            return EnumFormula(formula, year)
        #если формула выражена диапазоном
        if DiapasonFormula.is_formula(formula):
            return DiapasonFormula(formula, year)
        #если формула выражена смещением
        if BlasFormula.is_formula(formula):
            return BlasFormula(formula, year)
        #если формула выражена smart формулой
        if SmartFormula.is_formula(formula):
            return SmartFormula(formula, year)
        #если формула выражена смещением года
        if BlasYearFormula.is_formula(formula):
            return BlasYearFormula(formula, year)
        #просто дата
        if SimpleDateFormula.is_formula(formula):
            return SimpleDateFormula(formula, year)
        # во всех остальных случаях
        raise FormulaException('формула не определена')


class Formula(object):
    dates_list = []
    year = None

    def __init__(self, formula, year=None):
        self.formula = formula
        if not year:
            self.year = date.get_current_year()
        else:
            self.year = int(year)

    def sort_dates_list(self):
        '''
        сортировка
        '''
        self.dates_list.sort(
            key=lambda date: '{2:02d}-{1:02d}-{0:02d}'.format(*date)
        )


class SimpleDateFormula(Formula):
    '''
    формула выраженная просто датой 11.01
    или 11.01.2011 (т.е не зависимая от входящего года)
    '''

    @classmethod
    def is_formula(cls, formula):
        return bool(re.search(
            '^\d{1,2}\.\d{1,2}\.\d{4}?$|^\d{1,2}\.\d{1,2}$',
            formula
        ))

    @classmethod
    def explain(cls, formula):
        cnt = formula.count('.')
        if cnt == 1:
            return formula.split('.') + [(None)]
        elif cnt == 2:
            return formula.split('.')
        raise FormulaException('формула не SimpleDateFormula')


class BlasYearFormula(Formula):
    '''
    если умная формула выражена смещением года
    11.06.+1
    '''
    reg = '^(\d{1,2}\.\d{1,2})\.([-+]\d+)$'

    @classmethod
    def is_formula(cls, formula):
        return bool(re.search(cls.reg, formula))

    @classmethod
    def explain(cls, formula):
        return re.findall(cls.reg, formula)[0]


class BlasFormula(Formula):
    '''
    умная форумула выраженная смещением
    12>12.01
    '''

    @staticmethod
    def is_formula(formula):
        #проверим что сначала идет пареметры смещения
        if not re.search('^-?\d+[<>].+', formula):
            return False
        #проверим что смещение корректно т.е один указатель смещения
        level = 0
        blas = 0
        for alfa in formula:
            if alfa == '[':
                level += 1
            if alfa == ']':
                level -= 1
            if (alfa == '>' or alfa == '<') and not level:
                blas += 1
        return blas == 1

    @staticmethod
    def explain(formula):
        parts = re.findall('^(-?\d+)([<>])(.+)', formula)[0]
        blas = int(parts[0]) if parts[1] == '>' else -int(parts[0])
        sub_formula = parts[2]
        return (blas, sub_formula)


    def generatelist(self):
        blas, formula = BlasFormula.explain(self.formula)
        formula_obj = FormulaFactory.getClass(formula)
        formula_obj.generatelist()
        if len(formula_obj.dates_list) != 1:
            raise FormulaException('Дата не должны быть списком')
        date_begin = formula_obj.dates_list[0]
        self.dates_list = [date.date_shift(*date_begin + (blas,))]
        


class SmartFormula(Formula):
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

    @staticmethod
    def explain(formula):
        '''
        отделяем смартформулу от года
        '''
        formula = formula[1:-1]
        parts = re.findall('^(.*)\((.*)\)$', formula)
        if parts:
            s_formula, year = parts[0]
        else:
            # берем год установленный
            s_formula, year = formula, None
        return [s_formula, year]

    def check(self):
        if not self.sub_formula in ('be', 'b', 'e', 'Pascha'):
            raise FormulaException('Неопределенная формула')

    def process(self, year):
        if self.sub_formula == 'be':
            return '01.01~31.12'
        elif self.sub_formula == 'b':
            return '01.01'
        elif self.sub_formula == 'e':
            return '31.12'
        elif self.sub_formula == 'Pascha':
            pascha = date.Pascha(self.year if not year else year)
            return '{0:02d}.{1:02d}'.format(pascha[0], pascha[1])
        else:
            raise FormulaException('Неопределенная формула')

    def get_list(self):
        self.sub_formula, year = SmartFormula.explain(formula)
        self.check()
        formula = self.process(year)
        formula_obj = FormulaFactory.getClass(formula, year)
        self.dates_list = formula_obj.get_list()


class DiapasonFormula(Formula):
    '''
    умная формула выраженная диапазоном
    formula1~formula2
    возможны лишь только две субформулы
    '''
    dates_list_formula1 = []
    dates_list_formula2 = []

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

    def check(self, dates1, dates2):
        '''
        проверить что части - есть одиночные даты
        проверить что первое число меньше второго
        '''
        if len(dates1) != 1 or len(dates2) != 1:
            raise FormulaException('Даты не должны быть списком')
        if date.date_compare(*dates1[0] + dates2[0]) <= 0:
            raise FormulaException('Вторая дата должна быть старше')

    def diapason(self, dates1, dates2):
        # cгенерируем список
        self.dates_list = dates1
        current_date = dates1[0]
        while date.date_compare(*current_date + dates2[0]) == 1:
            current_date = date.date_shift(*current_date + (1,))
            self.dates_list.append(current_date)

    def generatelist(self):
        # получим формулы
        formula1, formula2 = DiapasonFormula.explain(formula)
        # получим даты формулы 1
        formula1_obj = FormulaFactory.getClass(formula1)
        formula1_obj.generatelist()
        # получим даты формулы 2
        formula2_obj = FormulaFactory.getClass(formula2)
        formula2_obj.generatelist()
        # проверяем
        self.check(formula1_obj.dates_list, formula2_obj.dates_list)
        self.diapason(formula1_obj.dates_list, formula2_obj.dates_list)


class EnumFormula(Formula):
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

    def generatelist(self):
        sub_formules = EnumFormula.explain(formula)
        self.dates_list = []
        for formula in sub_formules:
            formula_obj = FormulaFactory.getClass(formula)
            self.dates_list += formula_obj.get_list()


class FullFormula(Formula):
    '''
    умная формула выраженная в своей полной форме
    формула,фильтры
    full_formula = [formula|w_filter|d_filter]
    '''
    # фильтр дня недели
    w_filter = '1111111'
    # фильтр данных
    d_filter = '0'

    @staticmethod
    def is_formula(full_formula):
        '''
        проверяем что строка является полной формулой
        - т.е обернута в []
        '''
        return full_formula[0] == '[' and full_formula[-1] == ']'

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
        if FullFormula.is_formula(full_formula):
            # если формула представлена в виде полной формулы
            # то уберем оборачивающие символы
            full_formula = full_formula[1:-1]
        tmp_formula = re.sub('\[.*\]', '*', full_formula)
        filters_cnt = tmp_formula.count('|')
        if filters_cnt > 2:
            #возможны лишь два фильтра
            raise FormulaException('Количество фильтров превышает 2')
        # дополним временную и полную формулу
        tmp_formula = tmp_formula + "|" * (2 - filters_cnt)
        full_formula = full_formula + "|" * (2 - filters_cnt)
        #разобъем полную формулу по составляющим
        formula, w_filter, d_filter = tmp_formula.split('|')
        # сотрем область фильтров - получим формулу
        formula = re.sub(
            '\|{0}\|{1}$'.format(w_filter, d_filter), '', full_formula
        )
        # если фильтры выделить не удалось 
        # - используем значения по умолчанию
        if not w_filter:
            w_filter = '1111111'
        if not d_filter:
            d_filter = '0'
        return [formula, w_filter, d_filter]

    def week_filter(self, w_filter):
        '''
        фильтр дня недели
        '''
        if w_filter == '1111111':
            return
        if w_filter == '0000000':
            self.dates_list = []
            return
        # проходимся с конца массива дат
        for i in range(len(self.dates_list))[::-1]:
            # если дата не соответсвует маске, тоудаляем ее
            if w_filter[date.get_day_of_week(*self.dates_list[i]) - 1] == '0':
                del self.dates_list[i]

    def data_filter(self, d_filter):
        '''
        фильтр данных
        '''
        positions = map(int, d_filter.split(','))
        # если есть указатель всех данных - то возвращаем без изменений
        if 0 in positions:
            return
        # преобразуем positions - отрицательные позиции преобразуем в положительные
        positions = map(
            lambda x: x + len(self.dates_list) if x < 0 else x - 1,
            positions
        )
        for i in range(len(self.dates_list))[::-1]:
            if not i in positions:
                del self.dates_list[i]

    @staticmethod
    def check(formula, w_filter, d_filter):
        '''
        проверка что все корректно
        проверка выполняется для данных полученных explain
        '''
        if not formula:
            raise FormulaException('формула должна быть получена')
        #убедимся что фильтры корректны
        if w_filter and not re.search('^[0,1]{7}$', w_filter):
            raise FormulaException('фильтр дня недели не корректен')
        if d_filter and not re.search('^(-?\d+,)*-?\d+$', d_filter):
            raise FormulaException('фильтр данных не корректен')


    def generatelist(self):
        formula, w_filter, d_filter = FullFormula.explain(full_formula)
        FullFormula.check(formula, w_filter, d_filter)
        formula_obj = FormulaFactory.getClass(formula)
        formula_obj.generatelist()
        self.dates_list = formula_obj.dates_list
        # фильтруем
        self.week_filter(w_filter)
        self.data_filter(d_filter)
