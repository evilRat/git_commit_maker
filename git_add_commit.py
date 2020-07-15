#-- coding:utf8 --

import shutil
import os
import json
import random
import time
import datetime


def get_file(root_path,all_files=[]):
    '''
    递归函数，遍历该文档目录和子目录下的所有文件，获取其path
    '''
    files = os.listdir(root_path)
    for file in files:
        if not os.path.isdir(root_path + '/' + file):   # not a dir
            all_files.append(root_path + '/' + file)
        else:  # is a dir
            get_file((root_path+'/'+file),all_files)
    return all_files


def copy_delete_file(source_file,target_file):
    '''
    复制文件
    '''
    source_path = source_file[0:source_file.rindex("/")]
    target_path = target_file[0:target_file.rindex("/")]
    if not os.path.exists(target_path):
        os.makedirs(target_path)
        print("create " + source_path)
    print(source_file)
    print(target_file)
    if os.path.exists(target_file):
        print("准备删除文件： " + target_file)
        os.remove(target_file)
        print("删除了文件： " + target_file)
    else:
        print("准备复制文件： " + target_file)
        shutil.copyfile(source_file,target_file)
        print("复制了文件： " + target_file)

def git_operating(month, name, times):
    # 根据每月次数循环
    for i in range(times):
        # 选取当前操作文件
        file_index = random.randint(0, len(file_list)-1)
        print("第 " + str(i) + " 次操作，本次index " +str(file_index) + "\n")
        cur_file=file_list[file_index]
        # 复制文件/删除文件
        copy_delete_file(cur_file,cur_file.replace("source", "new"))
        # 随机获取时间拼接到年月
        cur_time = month + "-" + str(random.randint(1,28)) + " " + str(random.randint(1,23)) + ":" + str(random.randint(1,59)) + ":" + str(random.randint(1,59))
        result_time = datetime.datetime.strptime(cur_time, '%Y-%m-%d %H:%M:%S')
        print(result_time)
        result_time = time.strftime('%a %b %d %H:%M:%S %Y')
        print(result_time)

        # git操作
        os.system("git add .")
        os.system('git commit -m "add ' + cur_file[cur_file.rindex("/"):] +'" --author "' + name + '" --date "' + result_time + '"')



###流程开始

#if __name__ == "__main__":
# 获取所有文件
old_repo="/mnt/d/yusys/requirement/智能模型实验室平台研发项目加计扣除/repos_source/model-server"
new_repo="/mnt/d/yusys/requirement/智能模型实验室平台研发项目加计扣除/repo_new/model-server"
global file_list
file_list = get_file(old_repo)

print("从旧git仓库读取了  " + str(len(file_list)) + " 个文件")
print(file_list[1])

# 读取配置文件
data_file = open('people-server.json')
data_json = json.loads(data_file.read())
data_file.close()

print("读取人员数据：" + str(data_json))



# 根据月分循环
for month, people_data in data_json.items():
    print(month + " || " + str(people_data) + "\n")
    # 根据人员循环
    for name, times in people_data.items():
        print("\t" + name + " || " + str(times) + "\n")
        # git操作
        git_operating(month, name, times)


