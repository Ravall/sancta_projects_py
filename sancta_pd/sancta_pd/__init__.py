from pyramid.config import Configurator
from pyramid_jinja2 import renderer_factory
from sancta_pd.models import get_root

def main(global_config, **settings):
    """ This function returns a WSGI application.

    It is usually called by the PasteDeploy framework during
    ``paster serve``.
    """
    settings = dict(settings)
    settings.setdefault('jinja2.i18n.domain', 'sancta_pd')

    config = Configurator(root_factory=get_root, settings=settings)
    config.add_translation_dirs('locale/')
    config.include('pyramid_jinja2')
    config.add_jinja2_search_path("sancta_pd:templates")

    config.add_static_view('static', 'static')


    config.add_view('sancta_pd.views.event.my_view',
                    context='sancta_pd.models.MyModel',
                    renderer="mytemplate.jinja2")

    config.add_route('event_list', '/event/list')
    config.add_view('sancta_pd.views.event.list',
                    renderer="event/list.jinja2",route_name='event_list')

    return config.make_wsgi_app()
