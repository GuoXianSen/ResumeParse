import os
import fitz
import pythoncom
from PIL import Image
from win32com.client import Dispatch
from win32com.client import gencache
from win32com.client import constants, gencache


# 创建简历同名文件夹
def mkdir(path):
    folder = os.path.exists(path)

    if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path)


# 读取文件夹
def findAllFile(base):
    for root, ds, fs in os.walk(base):
        for filename in fs:
            fullname = os.path.join(root, filename)
            yield fullname, filename


# pdf转png
def pdf_image(pdfPath, pdfname, imgPath, zoom_x, zoom_y, rotation_angle):
    # 打开PDF文件
    pdf = fitz.open(pdfPath)
    # 逐页读取PDF
    for pg in range(0, pdf.page_count):
        page = pdf[pg]
        # 设置缩放和旋转系数
        trans = fitz.Matrix(zoom_x, zoom_y).prerotate(rotation_angle)
        pm = page.get_pixmap(matrix=trans, alpha=False)
        # 开始写图像
        mkdir(imgPath + pdfname.replace('.pdf', ''))
        pm.save(imgPath + pdfname.replace('.pdf', '') + '/' + str(pg) + ".png")

    page_c = pdf.page_count
    pdf.close()
    return page_c


# word转pdf
def doc2pdf(filepath):
    wdFormatPDF = 17  # 转换的类型
    # bug终结者
    pythoncom.CoInitialize()
    word = Dispatch('Word.Application')
    doc = word.Documents.Open(filepath)
    doc.SaveAs(filepath.replace(".docx", ".pdf").replace('.doc', '.pdf'), FileFormat=wdFormatPDF)
    doc.Close()
    word.Quit()
# # word转pdf
# def doc2pdf(filepath):
#     wdFormatPDF = 17  # 转换的类型
#     word = Dispatch('Word.Application')
#     doc = word.Documents.Open(filepath)
#     doc.SaveAs(filepath.replace('dataset', 'temp_pdf').replace(".docx", ".pdf").replace('.doc', '.pdf'), FileFormat=wdFormatPDF)
#     doc.Close()
#     word.Quit()

def main():
    base = './dataset'
    temp_png_path = './temp_png/'  # png保存位置
    path = os.getcwd()
    for fullpath, filename in findAllFile(base):
        get_file_type = os.path.splitext(filename)
        name, filetype = get_file_type

        if filetype == '.pdf':
            pdf_image(fullpath, filename, temp_png_path, 1, 1, 0)

        elif filetype == '.png' or filetype == '.jpeg' or filetype == '.PNG' or filetype == '.JPEG':
            I = Image.open(fullpath)
            mkdir(temp_png_path + name)
            I.save(temp_png_path + name + '/' + filename)

        elif filetype == '.docx' or filetype == '.doc':
            wordpath = path + '/dataset/' + filename
            doc2pdf(wordpath)
            pdf_image(wordpath.replace('dataset', 'temp_pdf').replace(".docx", ".pdf").replace('.doc', '.pdf'),
                      filename.replace(".docx", ".pdf").replace('.doc', '.pdf'),
                      temp_png_path, 1, 1, 0)


# main()
if __name__ == '__main__':
    testpath = 'C:\\Users\\Clay_Guo\\Desktop\\【软件杯】\\Base\\django-vue-lyadmin\\backend\\media\\platform\\2023-06-24\\20230624164603_761.doc'
    test2path = r"C:\Users\Clay_Guo\Desktop\【软件杯】\Base\django-vue-lyadmin\backend\media\platform\2023-06-24\20230624174238_628.doc"
    doc2pdf(test2path)
