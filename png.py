import sys
import fitz
import os
import datetime
import urllib.request


def getFile(url):
    if not os.path.exists('pdf'):
        os.makedirs('pdf')
    pdf_name = './pdf/'+url.split('/')[-1].split('_')[0]+'.pdf'
    try:
        u = urllib.request.urlopen(url)
    except urllib.error.HTTPError:
        return 0
    block_sz = 8192

    with open(pdf_name, 'wb') as f:
        while True:
            buffer = u.read(block_sz)
            if buffer:
                f.write(buffer)
            else:
                break
    return pdf_name


def pyMuPDF_fitz(pdfPath, imagePath):
    pdfDoc = fitz.open(pdfPath)
    filename = pdfPath.split('/')[-1].split('.')[0]
    for pg in range(pdfDoc.pageCount):
        page = pdfDoc[pg]
        rotate = int(0)
        zoom_x = 2
        zoom_y = 2
        mat = fitz.Matrix(zoom_x, zoom_y).preRotate(rotate)
        pix = page.getPixmap(matrix=mat, alpha=False)

        if not os.path.exists(imagePath):
            os.makedirs(imagePath)

        pix.writePNG(imagePath+'/'+'%s.png' % filename)
    return '/static/' + filename+'.png'


def pyMuPDF2_fitz(pdfPath, imagePath):
    pdfDoc = fitz.open(pdfPath)  # open document
    for pg in range(pdfDoc.pageCount):  # iterate through the pages
        page = pdfDoc[pg]
        rotate = int(0)
        zoom_x = 1.33333333  # (1.33333333-->1056x816)   (2-->1584x1224)
        zoom_y = 1.33333333
        # 缩放系数1.3在每个维度  .preRotate(rotate)是执行一个旋转
        mat = fitz.Matrix(zoom_x, zoom_y).preRotate(rotate)
        rect = page.rect                         # 页面大小
        mp = rect.tl + (rect.bl - (0, 75/zoom_x))  # 矩形区域    56=75/1.3333
        clip = fitz.Rect(mp, rect.br)            # 想要截取的区域
        pix = page.getPixmap(matrix=mat, alpha=False, clip=clip)  # 将页面转换为图像
        if not os.path.exists(imagePath):
            os.makedirs(imagePath)
        pix.writePNG(imagePath+'/'+'psReport_%s.png' %pg)


# if __name__ == "__main__":
#     pdfPath = 'http://www.dailyqd.com/epaper/img/1/2020-08/31/12/2020083112_pdf.pdf'
#     filename = getFile(pdfPath)
#     if filename:
#         imagePath = './image'
#         pyMuPDF_fitz(filename, imagePath)

    # pyMuPDF2_fitz(pdfPath, imagePath)  # 指定想要的区域转换成图片
