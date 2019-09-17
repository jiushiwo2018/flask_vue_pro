#!/usr/bin/env python2
# __VERSION = 2.0
from __future__ import print_function
import json
import re
import os
import shutil
from subprocess import Popen, PIPE
import sys
import getopt
import traceback



#host='http://oss-sh.ccr.corp.intel.com:8000'
host='https://dcg-oss.intel.com'


try:
    import requests
    from requests.packages.urllib3.exceptions import InsecureRequestWarning
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
except Exception as e:
    print(e)
    print('import requests error ,please install request first')
    input()
    exit()


def download_file_from_link(link, username, password):
    basename = os.path.basename(link)  # return last name of file
    folder = 'tmp'
    file_path = folder + '/' + basename
    print(os.path.abspath(file_path))

    if 'http' in link:  # download file by http
        if not os.path.isdir(folder):
            os.mkdir(folder)
        res = requests.get(url=link, stream=True, verify=False)
        with open(file_path, 'wb') as f:
            for chunk in res.iter_content(chunk_size=512):
                if chunk:
                    f.write(chunk)
        return file_path

    elif 'file:' in link or re.match(r'\\\\', link):
        if not os.path.isdir(folder):
            os.mkdir(folder)
        remote_path = link.replace('file:///', '')
        remote_host = re.split(r'[/\\]+', remote_path)[1]
        remote_folder = re.split(r'[/\\]+', remote_path)[2]
        command = r'net use z: \\%s\%s %s /user:%s' % (remote_host, remote_folder, password, username)
        print(command)
        proc = Popen(command, stdout=PIPE, shell=True)
        print(proc.stdout.read())
        shutil.copy(remote_path, file_path)
        return file_path

    else:
        return link


class CheckAPI(object):
    def __init__(self, proj_id, ingredient_name, check_file, is_extract, checkin_version, checkin_os_name_list, build,
                 checkin_notes=None, checkin_ipscan=None, checkin_klocwork=None, username='', password='',
                 re_username='', re_password='', host='https://dcg-oss.intel.com'):
        self.proj_id = proj_id
        self.ingredient_name = ingredient_name
        self.check_file = check_file
        self.is_extract = is_extract
        self.checkin_version = checkin_version
        self.checkin_os_name_list = checkin_os_name_list
        self.build = build
        self.checkin_notes = checkin_notes
        self.checkin_ipscan = checkin_ipscan
        self.checkin_klocwork = checkin_klocwork
        self.username = username
        self.password = password
        self.re_username = re_username if re_username else username
        self.re_password = re_password if re_password else password
        self.host = host
        self.my_data = {'username': username, 'password': password, 'proj_id': proj_id}
        self.req = requests.session()
        self.req.verify = False

    def login(self):
        login_page = '%s/login/' % self.host
        retries = 3
        retries_done = 0
        while retries_done < retries:
            response = self.req.post(login_page, data=self.my_data)
            print('START DEBUG INFO: login(self)')
            print('Attempt: ',retries_done+1,'/',retries)
            print('login_page: ',login_page)
            print('HTTP status code: ',response.status_code)
            if response.status_code != 200:
                print('response encoding: ',response.encoding)
                print('Response text content:')
                try:
                    print('========== returned page =============')
                    print(response.text)
                except UnicodeEncodeError:
                    print(response.text.decode('utf-8'))
                retries_done += 1
            print('END DEBUG INFO: : login(self)')
            if response.status_code == 200:
                break
        if response.status_code != 200:
            print('login error, see messages above')
            return False
        else:
            # print('login success')
            return True

    def __get_checkin_os_id_list(self):
        ingredient_page = '%s/check_upload_components_dev/%s/' % (self.host, self.proj_id)
        print(self.my_data)
        response = self.req.post(ingredient_page, self.my_data)
        result = response.text
        print ('get_list')
        print (result)
        print ('get_list2')
        if re.findall(r'ingredient_dict =', result)[0]:
            print('login success')
        else:
            print('login error may have no access')
        print('nowissue1')
        print (result)
        ingredient_dict_json = re.findall(r'ingredient_dict = (\{.*\})', result)[0]#get useable ingredient list
        print(ingredient_dict_json)
        print('nowissue2')
        ingredient_dict = json.loads(ingredient_dict_json)
        print(self.ingredient_name)
        os_tuples = ingredient_dict[self.ingredient_name]
        print("os_tuples=%s"% os_tuples)
        checkin_os_id_list = []
        print ('checkin_os_name_list=%s'% self.checkin_os_name_list)
        for checkin_os_name in self.checkin_os_name_list:
            for name, id in os_tuples:
                if name == checkin_os_name:
                    checkin_os_id_list.append(id)
                    break
        print("checkin_os_id_list=%s"% checkin_os_id_list)
        return checkin_os_id_list

    def __checkin_validate(self):
        # checkin validate
        validate_page = '%s/checkin_validate_dev/%s/' % (self.host, self.proj_id)
        self.my_data['check_type'] = self.ingredient_name
        self.my_data['is_extract'] = self.is_extract
        self.my_data['checkin_version'] = self.checkin_version
        checkin_os_id_list = self.__get_checkin_os_id_list()
        self.my_data['checkin_os'] = checkin_os_id_list

        self.check_file = download_file_from_link(self.check_file, self.re_username, self.re_password)

        files = {'check_file': open(self.check_file, 'rb')}
        if self.checkin_notes:
            self.checkin_notes = download_file_from_link(self.checkin_notes, self.re_username, self.re_password)
            files['check_notes'] = open(self.checkin_notes, 'rb')
        if self.checkin_ipscan:
            self.checkin_ipscan = download_file_from_link(self.checkin_ipscan, self.re_username, self.re_password)
            files['check_ipscan'] = open(self.checkin_ipscan, 'rb')
        if self.checkin_klocwork:
            self.checkin_klocwork = download_file_from_link(self.checkin_klocwork, self.re_username, self.re_password)
            files['check_klocwork'] = open(self.checkin_klocwork, 'rb')

        response = self.req.post(validate_page, data=self.my_data, files=files)
        print ('validate_page1')
        print (self.my_data)
        print (response)
        print ('validate_page2')
        if response.status_code == 200:
            result = response.json()
        else:
            print('checkin validate failed')
            result = []
        return result

    def checkin_submit(self):
        result = self.__checkin_validate()
        # checkin submit
        submit_page = '%s/checkin_submit_dev_upload_xml/%s/' % (self.host, self.proj_id)
        self.my_data['pkg_location'] = result['pkglocation']
        #server local path
        self.my_data['checkin_file_name'] = result['name']     #if extract "NA"
        self.my_data['notes_location'] = result['releasenotes'] #none
        self.my_data['ipscan_location'] = result['ipscan']         #none
        self.my_data['klockwork_location'] = result['klocwork']     #none
        print(self.my_data)
        response = self.req.post(submit_page, data=self.my_data)
        #page_info = response.text
        print('page info')
        print ('submit_page1')
        #print(page_info)
        print ('submit_page2')
        try:
            jsonstr = json.loads(response.text)
        except:
            print("upload success")
            return True

        if jsonstr:
            status = jsonstr["status"]
        if status:
            return False



        # triggle build
        if self.build == 'yes':
            print ('this script can not trigger')
            return True


if __name__ == '__main__':
    usage = '''
    required(
    -u username (for oss authentication)
    -p password
    -j proj_id: project id
    -n xxx: check in ingredient name
    -f xxx:  check in ingredient file
    -e (yes/no): If yes, the package would be extract during build.
    -v xxx : check in ingredient version
    -o xxx,xxx: check in os list
    -b (yes/no): If yes ,will triggle build)
    choosable(
    -r xxx: check in release note
    -i xxx: check in ipscan
    -k xxx: check in klocwork)
    -c xxx: remote username(used for authentication while check in file is a link,ignored if  same with oss)
    -d xxx; remote password
    -h :get this message
    '''

    try:
        opts, args = getopt.getopt(sys.argv[1:], "u:p:c:d:j:n:f:e:v:o:r:i:k:b:h:")


        op_re_username = ''
        op_re_password = ''
        op_checkin_notes = ''
        op_checkin_ipscan = ''
        op_checkin_klocwork = ''

        for op, value in opts:
            if op == '-u':
                op_username = value
            elif op == '-p':
                op_password = value
            elif op == '-c':
                op_re_username = value
            elif op == '-d':
                op_re_password = value
            elif op == '-j':
                op_proj_id = value
            elif op == '-n':
                op_ingredient_name = value
            elif op == '-f':
                op_check_file = value
            elif op == '-e':
                op_is_extract = value
            elif op == '-v':
                op_checkin_version = value
            elif op == '-o':
                op_checkin_os_name_list = value.split(',')
            elif op == '-r':
                op_checkin_notes = value
            elif op == '-i':
                op_checkin_ipscan = value
            elif op == '-k':
                op_checkin_klocwork = value
            elif op == '-b':
                op_build = value
            elif op == '-h':
                print(usage)
                raw_input()
                exit()
            else:
                print(usage)
                exit()
        checkinobj = CheckAPI(op_proj_id, op_ingredient_name, op_check_file, op_is_extract, op_checkin_version,
                              op_checkin_os_name_list, op_build,
                              op_checkin_notes, op_checkin_ipscan, op_checkin_klocwork, op_username, op_password,
                              op_re_username, op_re_password,host)

        if checkinobj.login():
            result = checkinobj.checkin_submit()
    except Exception as e:
        print(traceback.print_exc())
        print(e)
        print(usage)
        input()
        exit()
    print(r'check-in finish result is %s'% result)

    # checkinobj = CheckAPI(54, 'CONFIG',
    #                       r'file:///\\ecs.intel.com\common2\Proj\Bios\IFWIRelease\BasinFalls\1SWS\Alpha\2016.42.3.01\BSF_1SWS_CORP_NOPTT_PreProd_BIOS_33.01_609_ME1131_WW42_3_01.7z',
    #                       'no', 'test',
    #                       ['RHEL7.3'], 'no',
    #                       username='leizha9x', password='', host='http://127.0.0.1:8000')
    #
    # if checkinobj.login():
    #     checkinobj.checkin_submit()
