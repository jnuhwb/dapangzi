from werkzeug.utils import secure_filename
from flask import Flask,render_template,jsonify,request
import time
import os
import base64
from shutil import copyfile
 
app = Flask(__name__)

UPLOAD_FOLDER='upload'
STATIC_FOLDER='static'
HOST = 'http://127.0.0.1:5000'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
basedir = os.path.abspath(os.path.dirname(__file__))
file_dir=os.path.join(basedir,app.config['UPLOAD_FOLDER'])
static_file_dir=os.path.join(basedir, STATIC_FOLDER)
ALLOWED_EXTENSIONS = set(['txt','png','jpg','xls','JPG','PNG','xlsx','gif','GIF'])
#ALLOWED_EXTENSIONS = set(['xls','xlsx'])
 
# 用于判断文件后缀
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS
 
# 上传文件
@app.route('/api/jq_category',methods=['POST'],strict_slashes=False)
def api_upload():
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    f=request.files['myfile']  # 从表单的file字段获取文件，myfile为该表单的name值
    if f and allowed_file(f.filename):  # 判断是否是允许上传的文件类型
        fname=secure_filename(f.filename)
        print(fname)
        ext = fname.rsplit('.',1)[1]  # 获取文件后缀
        unix_time = int(time.time())
        new_filename=str(unix_time)+'.'+ext  # 修改了上传的文件名
        f.save(os.path.join(file_dir,new_filename))  #保存文件到upload目录
        
        #这里处理后保存到 static 文件夹
        if not os.path.exists(static_file_dir):
            os.makedirs(static_file_dir)
        copyfile(os.path.join(file_dir, new_filename), os.path.join(static_file_dir, new_filename))
        url = HOST + '/static/' + new_filename
 
        return jsonify({"errno":0,"errmsg":" 分类成功","url":url})
    else:
        return jsonify({"errno":1001,"errmsg":"分类失败"})
 
if __name__ == '__main__':
    app.run(debug=True)
