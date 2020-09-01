import web
import json
import png

urls = (
    '/ping/?','ping',
    '/pdf/?','pdf',
    '/(image)/(.*)', 'static',
)
app = web.application(urls, globals())


class ping:
    def GET(self):
        return 'hi,ping'

class pdf:
    def POST(self):
        ret = {
            'code': '0',
            'msg': '',
        }
        data = web.input(name=None)
        name = data.name
        if (name == 'None'):
            return ret
        filename = png.getFile(name)
        if filename:
            imagePath = './static'
            png.pyMuPDF_fitz(filename, imagePath)
            ret = {
                'code': '1',
                'msg': png.pyMuPDF_fitz(filename, imagePath)
            }
            return ret
class static:
    def GET(self, media, file):
        try:
            f = open(media+'/'+file, 'r')
            return f.read()
        except:
            return '404! file not found'

if __name__ == "__main__":
    app.run()
