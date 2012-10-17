def event(config):
    config.add_route('event_list', '/event/list')
    config.add_route('event_edit', '/event/edit/{id}')
    config.add_route('event_add_icon', '/event/addicon/{id}')

def routing(config):
    event(config)