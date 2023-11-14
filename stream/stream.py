""" streamXBlock main Python class"""

import pkg_resources
from django.template import Context, Template

from xblock.core import XBlock
from xblock.fields import Scope, Integer, String, Boolean
from xblock.fragment import Fragment


class streamXBlock(XBlock):

    '''
    Icon of the XBlock. Values : [other (default), video, problem]
    '''
    icon_class = "video"

    '''
    Fields
    '''
    display_name = String(display_name="Display Name",
                          default="Stream",
                          scope=Scope.settings,
                          help="This name appears in the horizontal navigation at the top of the page.")

    url = String(display_name="URL",
                 default="https://stream.mux.com/VZtzUzGRv02OhRnZCxcNg49OilvolTqdnFLEqBsTwaxU.m3u8",
                 scope=Scope.content,
                 help="The URL of your video.")

    thumbnail_url = String(display_name="Thumbnail URL",
                 default="",
                 scope=Scope.content,
                 help="The Thumbnail URL of your video.")
    '''
    Util functions
    '''

    def load_resource(self, resource_path):
        """
        Gets the content of a resource
        """
        resource_content = pkg_resources.resource_string(
            __name__, resource_path)
        # return unicode(resource_content, 'utf-8')
        return resource_content.decode('utf-8')

    def render_template(self, template_path, context={}):
        """
        Evaluate a template by resource path, applying the provided context
        """
        template_str = self.load_resource(template_path)
        return Template(template_str).render(Context(context))

    '''
    Main functions
    '''

    def student_view(self, context=None):
        """
        The primary view of the XBlock, shown to students
        when viewing courses.
        """

        context = {
            'display_name': self.display_name,
            'url': self.url,
            'thumbnail_url': self.thumbnail_url,
        }

        html = self.render_template('static/html/stream_view.html', context)

        frag = Fragment(html)
        frag.add_css(self.load_resource("static/css/stream.css"))

        '''
        No need to load dash.all.min.js as I have already added it from cdn in stream_view.html
        frag.add_javascript(self.load_resource("static/js/dash.all.debug.js"))
        <script src="https://cdn.dashjs.org/latest/dash.all.min.js"></script>
        '''
        frag.add_javascript(self.load_resource("static/js/stream_view.js"))
        frag.initialize_js('streamXBlockInitView')
        return frag

    def studio_view(self, context=None):
        """
        The secondary view of the XBlock, shown to teachers
        when editing the XBlock.
        """
        context = {
            'display_name': self.display_name,
            'url': self.url,
            'thumbnail_url': self.thumbnail_url,
        }
        html = self.render_template('static/html/stream_edit.html', context)

        frag = Fragment(html)
        frag.add_javascript(self.load_resource("static/js/stream_edit.js"))
        frag.initialize_js('streamXBlockInitStudio')
        return frag

    @XBlock.json_handler
    def save_stream(self, data, suffix=''):
        """
        The saving handler.
        """
        self.display_name = data['display_name']
        self.url = data['url']
        self.thumbnail_url = data['thumbnail_url']

        return {
            'result': 'success',
        }
