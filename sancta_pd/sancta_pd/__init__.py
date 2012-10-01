# -*- coding: utf-8 -*-
from pyramid.config import Configurator
from pyramid_jinja2 import renderer_factory
import os
from sancta_pd.config.route import routing
from sqlalchemy import engine_from_config
from sancta_pd.models.db_models import DBSession

def main(global_config, **settings):
    """ This function returns a WSGI application.

    It is usually called by the PasteDeploy framework during
    ``paster serve``.
    """
    settings = dict(settings)
    settings.setdefault('jinja2.i18n.domain', 'sancta_pd')


    config = Configurator(settings=settings)
    config.add_translation_dirs('locale/')
    config.include('pyramid_jinja2')

    config.add_jinja2_search_path("sancta_pd:templates")

    config.add_static_view('static', 'static')


    # определяем роутинг
    routing(config)
    config.scan('sancta_pd')
    return config.make_wsgi_app()
