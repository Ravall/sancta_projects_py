from pyramid.i18n import TranslationStringFactory
from sancta_pd.views.event import *

_ = TranslationStringFactory('sancta_pd')

def my_view(request):
    return {'project':'sancta_pd'}

