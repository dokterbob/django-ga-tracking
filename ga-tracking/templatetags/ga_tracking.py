from django.conf import settings

from django import template

register = template.Library()

@register.simple_tag
def tracking_url(source, medium, term, content, campaign):
    """ Please refer to the Google Analytics URL builder at
        http://www.google.com/support/googleanalytics/bin/answer.py?hl=en&answer=55578
    """
    import urllib
    url_dict = {}
    
    if source:
        url_dict.update({'utm_source' : source})

    if medium:
        url_dict.update({'utm_medium' : medium})

    if content:
        url_dict.update({'utm_term' : term})

    if content:
        url_dict.update({'utm_content' : content})
    
    if campaign:
        url_dict.update({'utm_campaign' : campaign})
    
    return urllib.urlencode(url_dict)

import unittest

class GaTrackingTests(unittest.TestCase): 
    def setUp(self): 
        self.context = template.Context()
        
    def test_tracking_url(self): 
        """Test the tag""" 
        template.libraries['django.templatetags.ga_tracking'] = register 

        t = template.Template('{% load ga_tracking %}{% tracking_url "source" "medium" "term" "content" "campaign" %}')
        
        result = 'utm_term=term&utm_medium=medium&utm_campaign=campaign&utm_source=source&utm_content=content'
        self.assertEqual(t.render(self.context), result)

        t = template.Template('{% load ga_tracking %}{% tracking_url "source" "" "term" "content" "campaign" %}')
        
        result = 'utm_term=term&utm_campaign=campaign&utm_source=source&utm_content=content'
        self.assertEqual(t.render(self.context), result)

if __name__ == '__main__': 
    settings.configure()
    unittest.main() 