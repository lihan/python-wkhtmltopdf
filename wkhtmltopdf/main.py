import os
import optparse

class WKhtmlToPdf(object):
    """
    Convert an html page via its URL into a pdf.
    """
    
    def __init__(self, *args, **kwargs):
        self.defaults = {
            'url': [kwargs.get('url', ""), str],
            'output_file': [kwargs.get('output_file', ""), str],
            'screen_resolution': [kwargs.get('screen_resolution', [1024, 768]), list],
            'color_depth': [kwargs.get('color_depth', 24), int],
            'flash_plugin': [kwargs.get('flash_plugin', True), bool],
            'disable_javascript': [kwargs.get('disable_javascript', False), bool],
            'delay': [kwargs.get('delay', 0.0)/1000.0, float],
            'orientation': [kwargs.get('orientation', 'Portrait'), str],
            'dpi': [kwargs.get('dpi', 100), int],
            'no_background': [kwargs.get('no_background', False), bool],
            'grayscale': [kwargs.get('grayscale', False), bool],
            'http_username': [kwargs.get('http_username', ""), str],
            'http_password': [kwargs.get('http_password', ""), str],
        }
        
        for k, v in self.defaults.items():
            if not isinstance(v[0], v[1]):
                raise TypeError("%s argument required for %s" % (v[1].__name__.capitalize(), k))
            if k is "orientation" and v[0] not in ['Portrait', 'Landscape']:
                raise TypeError("Orientation argument must be either Portrait or Landscape")
            setattr(self, k, v[0])
        
        if not self.url or not self.output_file:
            raise Exception("Missing url and output file arguments")
    
    def _create_option_list(self):
        """
        Add command option according to the default settings.
        """
        option_list = []
        if self.flash_plugin:
            option_list.append("--enable-plugins")
        if self.disable_javascript:
            option_list.append("--disable-javascript")
        if self.no_background:
            option_list.append("--no-background")
        if self.grayscale:
            option_list.append("--grayscale")
        if self.delay:
            option_list.append("--redirect-delay %s" % self.delay)
        if self.http_username:
            option_list.append("--username %s" % self.http_username)
        if self.http_password:
            option_list.append("--password %s" % self.http_password)
        option_list.append("--orientation %s" % self.orientation)
        option_list.append("--dpi %s" % self.dpi)
        
        return option_list
        
    def render(self):
        """
        Render the URL into a pdf and setup the evironment if required.
        """
        # setup the environment if it isn't set up yet
        display_env_var = os.environ.get('DISPLAY', None)
        if not display_env_var:
            os.system("Xvfb :0 -screen 0 %sx%sx%s & DISPLAY=127.0.0.1:0" % (
                self.screen_resolution[0],
                self.screen_resolution[1],
                self.color_depth
            ))
            os.environ["DISPLAY"] = '127.0.0.1:0'
        
        # execute the command
        command = "wkhtmltopdf %s %s %s" % (
            " ".join(self._create_option_list()),
            self.url,
            self.output_file
        )
        os.system(command)
        
def wkhtmltopdf(*args, **kwargs):
    wkhp = WKhtmlToPdf(*args, **kwargs)
    wkhp.render()
    
if __name__ == '__main__':
    
    # parse through the system argumants
    usage = "usage: %prog [options] arg1 arg2"
    parser = optparse.OptionParser()
    parser.add_option("-u", "--url", dest="url", default=True, help="url to convert")
    parser.add_option("-f", "--output-file", dest="output_file", default=True, help="output file path")
    parser.add_option("-F", "--flash-plugin", action="store_true", dest="flash_plugin", default=True, help="use flash plugin")
    parser.add_option("-J", "--disable-javascript", action="store_true", dest="disable_javascript", default=False, help="disable javascript")
    parser.add_option("-b", "--no-background", action="store_true", dest="no_background", default=False, help="do not print background")
    parser.add_option("-g", "--grayscale", action="store_true", dest="grayscale", default=False, help="make grayscale")
    parser.add_option("-d", "--redirect-delay", dest="delay", default=0, help="page delay before convertion")
    parser.add_option("-O", "--orientation", dest="orientation", default='Portrait', help="page orientation")
    parser.add_option("-D", "--dpi", dest="dpi", default=100, help="print dpi")
    parser.add_option("-U", "--username", dest="http_username", default="", help="http username")
    parser.add_option("-P", "--password", dest="http_password", default="", help="http password")
    (options, args) = parser.parse_args()
    options = options.__dict__
    # call the main method with parsed argumants
    wkhtmltopdf(**options)
    