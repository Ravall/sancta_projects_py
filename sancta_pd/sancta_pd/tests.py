import unittest
from pyramid import testing,registry
from pyramid.i18n import TranslationStringFactory
from sancta_pd.models import app_model
from paste.deploy.loadwsgi import appconfig
from pyramid.config import Configurator
from sancta_pd.models import app
import os



_ = TranslationStringFactory('sancta_pd')


here = os.path.dirname(__file__)
settings = appconfig('config:' + os.path.join(here, '../../', 'test.ini'))


class AppModelTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.config.scan()
        testing.setUp()
        
    def tearDown(self):
        testing.tearDown()

    def test_add_icon(self):
        xx = registry.Registry()
        print xx.settings
        app.get_config('ss')
        #event = app_model.mfEvent()
        #event.set_connection('mysql://root@localhost/mindfly_test')
        #icon = event.add_icon(title='tilte1', alt='annonce1',file='blablabla1')
        #print icon.id
