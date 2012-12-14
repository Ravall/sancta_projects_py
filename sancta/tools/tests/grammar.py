# -*- coding: utf-8 -*-
from django.test import TestCase
from tools.testutil import data_provider
import tools.grammar as grammar

class GrammarTest(TestCase):

    def provider_translite():
        return (
            (u'тест', 'test'),
            (u'конИ Педальные', 'koni_pedalnye'),
        )

    @data_provider(provider_translite)
    def test_translite(self, str_from, str_to):
        str_trance = grammar.translite(str_from)
        self.assertEquals(str_trance, str_to)
        # дважды транслитирируем
        self.assertEquals(grammar.translite(str_trance), str_to)
        

        

