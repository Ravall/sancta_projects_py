from tinymce.widgets import TinyMCE, get_language_config, smart_unicode

from django.forms.widgets import flatatt
from django.utils.html import escape
from django.utils import simplejson
from django.utils.safestring import mark_safe
import tinymce.settings


class Widget(TinyMCE):

    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        value = smart_unicode(value)
        final_attrs = self.build_attrs(attrs)
        final_attrs['name'] = name
        assert 'id' in final_attrs, \
            "TinyMCE widget attributes must contain 'id'"

        mce_config = tinymce.settings.DEFAULT_CONFIG.copy()
        mce_config.update(get_language_config(self.content_language))
        if tinymce.settings.USE_FILEBROWSER:
            mce_config['file_browser_callback'] = "djangoFileBrowser"
        mce_config.update(self.mce_attrs)
        if not 'mode' in mce_config:
            mce_config['mode'] = 'exact'
        if mce_config['mode'] == 'exact':
            mce_config['elements'] = final_attrs['id']
        mce_config['strict_loading_mode'] = 1

        # Fix for js functions
        js_functions = {}
        for k in ('paste_preprocess', 'paste_postprocess', 'setup'):
            if k in mce_config:
                js_functions[k] = mce_config[k]
                del mce_config[k]
        mce_json = simplejson.dumps(mce_config)

        pos = final_attrs['id'].find('__prefix__')
        if pos != -1:
            mce_json = mce_json.replace(
                u'"%s"' % final_attrs['id'], u'elements'
            )

        for k in js_functions:
            index = mce_json.rfind('}')
            mce_json = mce_json[:index] + ', ' + k \
                + ':' + js_functions[k].strip() \
                + mce_json[index:]
        html = [
            u'<textarea%s>%s</textarea>' % (
                flatatt(final_attrs), escape(value)
            )
        ]
        if tinymce.settings.USE_COMPRESSOR:
            compressor_config = {
                'plugins': mce_config.get('plugins', ''),
                'themes': mce_config.get('theme', 'advanced'),
                'languages': mce_config.get('language', ''),
                'diskcache': True,
                'debug': False,
            }
            # pylint: disable=W0612
            compressor_json = simplejson.dumps(compressor_config)

        if pos != -1:
            html.append(u'''<script type="text/javascript">
setTimeout(function () {
    var id = '%s';

    if (typeof(window._tinymce_inited) == 'undefined') {
        window._tinymce_inited = [];
    }

    if (typeof(window._tinymce_inited[id]) == 'undefined') {
        window._tinymce_inited[id] = true;
    } else {
        var elements = id.replace(/__prefix__/, parseInt(document.getElementById('%sTOTAL_FORMS').value) - 1);
        console.log(elements);
        if (document.getElementById(elements)) {
            tinymce.init(%s);
        }
    }
}, 0);
</script>''' % (final_attrs['id'], final_attrs['id'][0:pos], mce_json))
        else:
            html.append(
                u'<script type="text/javascript">'
                'tinyMCE.init(%s)</script>' % mce_json
            )

        return mark_safe(u'\n'.join(html))
