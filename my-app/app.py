from flask import Flask, request, jsonify
from flask import Flask, send_file
from flask_cors import CORS

import os
import base64
import random
import string
import subprocess
from datetime import datetime
import paramiko
import shutil

app = Flask(__name__)
CORS(app)
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect("10.107.36.34", username="jc", password="lab103", timeout=800)

#要存入跟輸出的位置
"""
UPLOAD_FOLDER = os.path.expanduser("~/DECA/examples")
RESULT_FOLDER = os.path.expanduser("~/DECA/results")
"""
UPLOAD_FOLDER = "/home/jc/DECA/TestSamples/examples"
RESULT_FOLDER = "/home/jc/DECA/TestSamples/examples/results"
LOCAL_TMP_FOLDER='/tmp'



@app.route('/upload', methods=['POST'])
def upload_image():
    #接收前端圖片並存入 DECA examples
    data = request.get_json()
    if not data or 'image' not in data:
        return jsonify({'message': 'No image provided'}), 400

    img_data = data['image'].split(',')[1]
    img_bytes = base64.b64decode(img_data)
    filename = store_image(img_bytes)
    result_obj=run_deca_on_remote(filename)
    #回傳result_obj 到前端
    return send_file(result_obj, mimetype="application/octet-stream", as_attachment=True)





def store_image(img_bytes):
    """ 清空資料夾並存入圖片 """
    ssh.connect("10.107.36.34", username="jc", password="lab103", timeout=800)
    if ssh.get_transport() is None:
        print("SSH 連線失敗，無法執行命令")
    #清空 `/home/jc/DECA/TestSamples/examples`
    if os.path.exists(LOCAL_TMP_FOLDER):
        shutil.rmtree(LOCAL_TMP_FOLDER)  # 刪除資料夾
    os.makedirs(LOCAL_TMP_FOLDER, exist_ok=True)  # 重新建立資料夾

    # 生成檔名（基於存入時間）
    filename = datetime.now().strftime("%Y%m%d_%H%M%S")+".png"

    # 存入 `UPLOAD_FOLDER`
    file_path = os.path.join(LOCAL_TMP_FOLDER, filename)
    try:
        with open(file_path, "wb") as f:
            f.write(img_bytes)
        print(f"圖片已存入: {file_path}")
    except Exception as e:
        print(f"圖片存入失敗: {e}")


    stdin, stdout, stderr = ssh.exec_command(f"ls ~/DECA/TestSamples/examples/{filename}.png")
    print(stdout.read().decode())  # 確保圖片存在
    return filename
REMOTE_FOLDER = "/home/jc/DECA/TestSamples/examples"  # Ubuntu DECA 目錄

def upload_to_deca(filename):
    """ 把 Windows 的圖片上傳到 Ubuntu DECA 伺服器 """
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect("10.107.36.34", username="jc", password="lab103")

    sftp = ssh.open_sftp()
    sftp.put(LOCAL_TMP_FOLDER, remote_path)  # **上傳圖片**
    sftp.close()
    ssh.close()

    file_path = os.path.join(UPLOAD_FOLDER, filename)
    remote_path = f"{REMOTE_FOLDER}/{filename}"

    # **執行上傳**
    upload_to_deca(file_path, remote_path)
    print(f"圖片已成功上傳到 Ubuntu: {remote_path}")


#連線DECA
def run_deca_on_remote(filename):    
    # 執行 DECA 模型
    ssh.connect("10.107.36.34", username="jc", password="lab103", timeout=800)
    if ssh.get_transport() is None:
        print("SSH 連線失敗，無法執行命令")
    command="conda activate deca-env"
    #print(ssh.exec_command(command))
    stdin, stdout, stderr = ssh.exec_command(f"ls ~/DECA/TestSamples/examples")
    print(stdout.read().decode())  # 確保圖片存在
    command = f"python ~/DECA/demos/demo_reconstruct.py -i ~/DECA/TestSamples/examples --saveDepth True --saveObj True"
    stdin, stdout, stderr = ssh.exec_command(command)
    output = stdout.read().decode()
    #print(output)
    
    # 讀取處理後的結果
    result_path=f"{RESULT_FOLDER}/{filename}/{filename}.obj"

    # 確保檔案已生成
    stdin, stdout, stderr = ssh.exec_command(f"ls {result_path}")
    #print(stdout)
    if stdout.read().decode().strip() == "":
        return {"message": "DECA 處理失敗"}
    else:
        #之後: 清空tmp
        # 載入obj至本地的tmp
        local_tmp_path = os.path.join(LOCAL_TMP_FOLDER, f"{filename}.obj")
        sftp = ssh.open_sftp()
        sftp.get(result_path, local_tmp_path)
        sftp.close()
        ssh.close()
        return {"message": "DECA 處理完成", "file": local_tmp_path}

ssh.close()
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)