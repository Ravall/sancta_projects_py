# -*- coding: utf-8 -*-
import datetime


def find_close_bracket(str, start=0):
    '''
    Для скобки на позиции $start находим закрывающую скобку
    '''
    try:
        start = float(start)
    except ValueError, TypeError:
        return False
    if start > len(str) - 2:
        return False
    try:
        cb_dict = {'{': '}', '(': ')', '[': ']'}
        cb = cb_dict[str[start]]
    except KeyError:
        return False
    n = 1
    #for i in range($start+1, )
    #for($i=$start+1; $i<$len; ++$i)
    #{
        #if($str[$i]==$cb)
        #{
            #$n--;
            #if($n==0) return $i;
        #} else if($str[$i]==$str[$start])
        #{
            #$n++;
        #}
    #}
    return False


def smart_date_function(formula, year=None):
    if year is None:
        # Год по умолчанию - текущий
        dt = datetime.datetime.now()
        year = dt.year
    #[даты|фильтр1|фильтр2]
    # сотрем лишнее. Мало ли.
    formula = formula.strip()
    if len(formula) == 0:
        return list()

    if (formula[0] == '[' and find_close_bracket(formula, 0) == len(formula) - 1):
        formula = substr($formula, 1, len(formula) - 2)
