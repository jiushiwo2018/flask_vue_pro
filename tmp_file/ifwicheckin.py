import re
import sys
import os
import time
import logging
import smtplib
import requests
import py7zlib
import traceback
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
import urllib2
import zipfile
import shutil
import subprocess
from base64 import encodestring
from datetime import datetime
from bs4 import BeautifulSoup

username = r"sys_syswhitleyoss"
password = r"juikv48$"
base_link = r"https://ubit-artifactory-or.intel.com/artifactory/server-bios-staging-local/nightly/whitley/"
downloadList = []
DL_path = r"C:\IFWI_autoCheckin133\daily"
zippath = r"C:\IFWI_autoCheckin133\checkinBin"
tempZipPath = r"C:\IFWI_autoCheckin133\tempZipPath"
checkin_dict = {}

org_txt = os.path.join(DL_path, "org.txt")
ret = False
ck_ret = False

log_name = "IFWIAutoCheckin.log"


class Logger:
    def __init__(self, path, clevel=logging.DEBUG, Flevel=logging.DEBUG):
        self.logger = logging.getLogger(path)
        self.logger.setLevel(logging.DEBUG)
        fmt = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s', '%Y-%m-%d %H:%M:%S')
        # set CMD log
        sh = logging.StreamHandler()
        sh.setFormatter(fmt)
        sh.setLevel(clevel)
        # set log file
        fh = logging.FileHandler(path)
        fh.setFormatter(fmt)
        fh.setLevel(Flevel)
        self.logger.addHandler(sh)
        self.logger.addHandler(fh)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def war(self, message):
        self.logger.warn(message)

    def error(self, message):
        self.logger.error(message)

    def cri(self, message):
        self.logger.critical(message)


def get_logger():
    return logging.getLogger(log_name)


def print_and_log(message, log_level):
    print(message)
    if log_level == logging.WARNING:
        get_logger().warning(message)
    elif log_level == logging.DEBUG:
        get_logger().debug(message)
    elif log_level == logging.INFO:
        get_logger().info(message)
    elif log_level == logging.ERROR:
        get_logger().error(message)
    elif log_level == logging.CRITICAL:
        get_logger().critical(message)


def sent_mail(content):
    mail_host = 'smtp.intel.com'  # set sever
    sender = 'yan.lin@intel.com'
    receivers = ['kunpengx.hu@intel.com', 'laura.liang@intel.com']  # reciver

    message = MIMEMultipart()
    message['From'] = Header(
        "From https://ubit-artifactory-or.intel.com/artifactory/server-bios-staging-local/nightly/whitley/", 'utf-8')
    message['To'] = ','.join(receivers)

    subject = '133 IFWI Packages Auto Checkin notice'
    message['Subject'] = Header(subject, 'utf-8')

    if content == False:
        message.attach(
            MIMEText('<font color=red>IFWI Packages Checkin to 133 failed, please check %s.\n</font>' % log_name,
                     'html', 'utf-8'))
    elif len(content) == 0:
        message.attach(MIMEText('133 No IFWI Packages updated\n', 'plain', 'utf-8'))
    else:
        message.attach(MIMEText('IFWI Packages Checkin to 133 successfully:\n%s\n' % content, 'html', 'utf-8'))
    att1 = MIMEText(open('IFWIAutoCheckin.log', 'rb').read(), 'base64', 'utf-8')
    att1["Content-Type"] = 'application/octet-stream'
    att1["Content-Disposition"] = 'attachment; filename="IFWIAutoCheckin.log"'
    message.attach(att1)

    try:
        server = smtplib.SMTP(mail_host, 25)
        server.sendmail(sender, receivers, message.as_string())
        print_and_log("sent email", logging.INFO)
    except smtplib.SMTPException:
        print_and_log("Error: can't sent", logging.INFO)


def pkg_download(url, DL_NAME, local_path):
    if not os.path.exists(local_path):
        os.makedirs(local_path)
    try:
        r = requests.get(url, stream=True)
        with open(os.path.join(local_path, DL_NAME), "wb") as pdf:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    pdf.write(chunk)
        return True
    except Exception as ERR:
        print_and_log("Download fail: %s" % ERR, logging.INFO)
        return False


def URL_OPEN(url, strx):
    try:
        packages_list = []
        page = urllib2.urlopen(url, timeout=10)
        data = page.read()
        # print data
        soup = BeautifulSoup(data, "html.parser")
        # print soup
        targets = soup.find_all(strx)
        for a in targets:
            packages = a.getText().encode('utf-8')
            # print packages
            if re.search(r'\d', packages):
                # print packages.isalnum
                packages_list.append(packages)
        # print len (packages_list)
        return packages_list
    except Exception as ERR:
        print_and_log("open URL fail:%s" % ERR, logging.INFO)


def writeToTxt(list_name, txtfile):
    try:
        with open(txtfile, "w+") as fw:
            for item in list_name:
                fw.write(str(item) + "\n")
    except IOError:
        print_and_log("fail to open file", logging.INFO)


def readtxtTolist(file_path):
    cmpList = []
    try:
        with open(file_path, "r+") as fr:
            for lines in fr.readlines():
                line = lines.replace("\n", "")
                cmpList.append(line)
    except IOError:
        print_and_log("fail to read file", logging.INFO)
    return cmpList


# print len (readtxtTolist(org_txt))

def extractBinFile(path, zpfile):
    ext_ret = False
    try:
        with open(zpfile, 'rb') as fp:
            archive = py7zlib.Archive7z(fp)
            for name in archive.getnames():
                # print name
                if re.search(r'^W(.*?)bin$', name):
                    print_and_log("-------- {0} : {1}--------".format(zpfile.split('\\')[-1], name), logging.INFO)
                if re.search(r'^W(.*?)_LBG_SPS.bin$', name) or re.search(r'^W(.*?)_LBG_SPS_ICXR.bin$', name):
                    # print "----name: %s"%name
                    if zpfile.split('\\')[-2] in checkin_dict.keys():
                        checkin_dict[zpfile.split('\\')[-2]] = checkin_dict[zpfile.split('\\')[
                            -2]] + '\n' + r"IFWI_{}.zip".format(re.findall(r"WR.64.(.+?)_P", name)[0])
                    else:
                        checkin_dict[zpfile.split('\\')[-2]] = r"IFWI_{}.zip".format(
                            re.findall(r"WR.64.(.+?)_P", name)[0])
                    print_and_log("-------- {0} Start extracting package:{1}--------".format(
                        time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), name), logging.INFO)
                    outfilename = os.path.join(path, name)
                    outdir = os.path.dirname(outfilename)
                    if not os.path.exists(outdir):
                        os.makedirs(outdir)
                    outfile = open(outfilename, 'wb')
                    outfile.write(archive.getmember(name).read())
                    outfile.close()
        ext_ret = True
        return ext_ret
    except IOError:
        print_and_log("extract file error", logging.INFO)
        return ext_ret


def dl_checkin(dl_list):
    for i in dl_list:
        if re.search(r"whitley.", i, re.I):
            if not os.path.exists(org_txt):
                pathlist = os.path.join(base_link, i)
                templist = URL_OPEN(pathlist, "a")
                # print templist
                if r"WhitleyRp_Release_ICX_4S_LBG_VS15/" in templist:
                    intersection_path = r"WhitleyRp_Release_ICX_4S_LBG_VS15/"
                elif r"WhitleyRp_Release_ICXR/" in templist:
                    intersection_path = r"WhitleyRp_Release_ICXR/"
                elif r"WhitleyRp_Release/" in templist:
                    intersection_path = r"WhitleyRp_Release/"
                else:
                    print_and_log("err:No such download path--> %s" % i, logging.INFO)
                    continue
                templist1 = URL_OPEN(os.path.join(pathlist, intersection_path), "a")
                for j in templist1:
                    if re.search(r'(.*?)BuildPkg.7z$', j):
                        target = os.path.join(os.path.join(pathlist, intersection_path), j)
                        downloadList.append(target)
            else:
                if i not in readtxtTolist(org_txt):
                    pathlist = os.path.join(base_link, i)
                    templist = URL_OPEN(pathlist, "a")
                    if r"WhitleyRp_Release_ICX_4S_LBG_VS15/" in templist:
                        intersection_path = r"WhitleyRp_Release_ICX_4S_LBG_VS15/"
                    elif r"WhitleyRp_Release_ICXR/" in templist:
                        intersection_path = r"WhitleyRp_Release_ICXR/"
                    elif r"WhitleyRp_Release/" in templist:
                        intersection_path = r"WhitleyRp_Release/"
                    else:
                        print_and_log("err:No such download path--> %s" % i, logging.INFO)
                        continue
                    templist1 = URL_OPEN(os.path.join(pathlist, intersection_path), "a")
                    for j in templist1:
                        if re.search(r'(.*?)BuildPkg.7z$', j):
                            target = os.path.join(os.path.join(pathlist, intersection_path), j)
                            downloadList.append(target)
    # print downloadList
    if not len(downloadList):
        return True
    for z in downloadList:
        # print downloadList
        DL_NAME = z.split('/')[-1]
        print_and_log("-------- {0} Start downloading package:{1}--------".format(
            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), z), logging.INFO)
        dl_ret = True
        while dl_ret:
            # print z.split('/')[-3]
            pkg_download(z, DL_NAME, os.path.join(DL_path, z.split('/')[-3]))
            LocalFileSize = getLocalFileSize(os.path.join(os.path.join(DL_path, z.split('/')[-3]), DL_NAME))
            SourceFileSize = getSourceFileSize(z)
            if LocalFileSize == SourceFileSize and LocalFileSize != 0:
                print_and_log("sourceSize:%d M, localSize:%d M" % (SourceFileSize, LocalFileSize), logging.INFO)
                dl_ret = False
            else:
                print_and_log("re-Download simics package %s to share folder......" % z, logging.INFO)
                pkg_download(z, DL_NAME, os.path.join(DL_path, z.split('/')[-3]))

        # print (os.path.join(DL_path, z.split('/')[-3]) + DL_NAME)
        if not extractBinFile(zippath, os.path.join(os.path.join(DL_path, z.split('/')[-3]), DL_NAME)):
            return False
    for zpf in os.listdir(zippath):
        zpfile = r"IFWI_{}.zip".format(re.findall(r"WR.64.(.+?)_P", zpf)[0])
        print_and_log("start zip file to : %s" % zpfile, logging.INFO)
        zf = zipfile.ZipFile(os.path.join(tempZipPath, zpfile), "w", zipfile.zlib.DEFLATED)
        zf.write(os.path.join(zippath, zpf), zpf)
        zf.close()
    try:
        for c in listFiles(tempZipPath):
            print_and_log("-------- {0} Start checkin {1} to OSS--------".format(
                time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), c.split('\\')[-1]), logging.INFO)
            # print re.findall(r"IFWI_(.+?).zip", c)[0]
            output_ret = os.popen(
                'python C:\\IFWI_autoCheckin133\\checkin_API_dev_nosubmit.py -u %s -p %s -j 133 -n IFWI -f %s -e no -v %s -o RHEL7.5,WinRS5,ESXi6.7 -b no' % (
                username, password, c, re.findall(r"IFWI_(.+?).zip", c)[0]))
            # print test.read()
            time.sleep(3)
            if "check-in finish result is True" in output_ret.read():
                writeToTxt(dl_list, org_txt)
                print_and_log("-------- {0} {1} checkin successed--------".format(
                    time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), c.split('\\')[-1]), logging.INFO)
                ck_ret = True
            else:
                ck_ret = False
                print_and_log("-------- {0} {1} checkin failed--------".format(
                    time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), c.split('\\')[-1]), logging.INFO)
                return ck_ret
        return ck_ret
    except Exception as err:
        print_and_log("checkin fail:%s" % err, logging.INFO)
        return False


def listFiles(dirPath):
    fileList = []
    for root, dirs, files in os.walk(dirPath):
        for fileObj in files:
            fileList.append(os.path.join(root, fileObj))
    return fileList


def zipFile(dirname, zipfilename):
    try:
        filelist = []
        if os.path.isfile(dirname):
            filelist.append(dirname)
        else:
            for root, dirs, files in os.walk(dirname):
                for name in files:
                    filelist.append(os.path.join(root, name))
        zf = zipfile.ZipFile(zipfilename, "w", zipfile.zlib.DEFLATED)
        for tar in filelist:
            arcname = tar[len(dirname):]
            # print arcname
            zf.write(tar, arcname)
        zf.close()
    except IOError:
        print_and_log("extract file error", logging.INFO)


def getLocalFileSize(path):
    try:
        size = os.path.getsize(path)
        return int(size) / 1024 / 1024
    except Exception as err:
        print_and_log("get local file size fail : %s" % err, logging.INFO)
        return 0


def getSourceFileSize(link):
    opener = urllib2.build_opener()
    try:
        request = urllib2.Request(link)
        request.get_method = lambda: 'HEAD'
        response = opener.open(request)
        response.read()
    except Exception as e:
        print_and_log("get source file size fail : %s" % e, logging.INFO)
        return 0
    else:
        fileSize = dict(response.headers).get('content-length', 0)
        return int(fileSize) / 1024 / 1024


def table_generator():
    d = ''
    html = ''

    if len(downloadList):
        # for i in downloadList:
        for k, v in checkin_dict.items():
            d = d + """
			<tr>
			  <td>""" + str(k) + """</td>
			  <td>""" + str(v) + """</td>
			</tr>"""
        # print d
        html = """\
	<head>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />


	<body>
	<div id="container">
	<p><strong>IFWI Daily Package:</strong></p>
	<div id="content">
	 <table width="auto" border="2" bordercolor="blue" cellspacing="2" cellpadding="2">
	<tr>
	  <td width="40"><strong>Daily Version</strong></td>
	  <td width="50"><strong>Package Name</strong></td>
	</tr>""" + d + """
	</table>
	</div>
	</div>
	</div>
	</body>
	</html>
		  """
    return html


# main-----------------------------------------------------------------------------------------------------------------------
logger = Logger(log_name, logging.WARNING, logging.DEBUG)
print_and_log("--------Start Logging-----------", logging.INFO)
try:
    if not os.path.exists(DL_path):
        os.makedirs(DL_path)
    if not os.path.exists(tempZipPath):
        os.makedirs(tempZipPath)
    if not os.path.exists(zippath):
        os.makedirs(zippath)

    ret = dl_checkin(URL_OPEN(base_link, "a"))
    # print "ret:%s"%ret
    # print(downloadList)
    if os.path.exists(tempZipPath):
        print_and_log("remove zip file and folder: %s" % tempZipPath, logging.INFO)
        shutil.rmtree(tempZipPath)
    if os.path.exists(zippath):
        print_and_log("remove BIOS bin file and folder: %s" % zippath, logging.INFO)
        shutil.rmtree(zippath)
except Exception as err:
    print_and_log("updated fail:%s" % err, logging.INFO)
    print_and_log(traceback.print_exc(), logging.INFO)
    ret = False
if ret:
    sent_mail(table_generator())
else:
    sent_mail(ret)



