def event(config):
    config.add_route('event_list', '/event/list')
    config.add_view('sancta_pd.views.event.list',
                    renderer="event/list.jinja2",
                    route_name='event_list')


def routing(config):
    event(config)