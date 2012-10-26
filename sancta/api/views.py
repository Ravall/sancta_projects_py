from django.http import HttpResponse

def get_icons_by_event_id(request, event_id):
	return HttpResponse("Hello, world. You're at the poll index.")