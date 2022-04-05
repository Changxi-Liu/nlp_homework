import yaml
import sys
import os
import re
file_loc = sys.argv[1]
begin_run=True
#begin_run=False
#    0: text
#      1: pos
#      2: chunk
#      3: ner

def merge_info( raw_data,data ):
    raw_data_list = re.split("\s+", raw_data)
    if len(raw_data_list) <= 3:
        return ""
    data_list = re.split("\s+", data)

    raw_data_list[3] = data_list[1]
    final_str = " ".join( raw_data_list)
    #print(final_str,data_list,raw_data_list)
    #exit(1)
    return final_str


with open(file_loc,'r') as f:
    yaml_obj = yaml.load(f.read())
#    print(yaml_obj)
dataname=yaml_obj['model_name']
cmd = "CUDA_VISIBLE_DEVICES=0 python train.py --config %s 2>&1|tee %s\n"%(file_loc,dataname+"-log")
cmd_gen = "CUDA_VISIBLE_DEVICES=0 python train.py --gen --test --config %s\n"%file_loc

cmd = cmd+ cmd_gen
#cmd = ""
print(cmd)
if begin_run:
    os.system(cmd)  ## at first generate on raw data
model_name = yaml_obj['model_name']
dataset_name = ""
for elem in yaml_obj['ner'].keys():
    if "FULL" in elem:
        dataset_name = elem
        break
print(dataset_name)
src_dir = yaml_obj['ner'][ dataset_name ]['data_folder']
iteration = 3
new_train_data_loc = "resources/taggers/%s/test.tsv"%(model_name)
def process_each_iteration( it):
    global new_train_data_loc
    config_file="config/%s.yaml"%(dataname+"-"+str(it))
    dst_dir=src_dir+"_iter%s"%it
    cmd_cp1 = "cp -r %s %s\n"%(src_dir,dst_dir)
    src_file = os.path.join(src_dir,"train.txt")
    dst_file = os.path.join(dst_dir,"train.txt")
    cmd_cp0 = "cp -r %s %s\n"%(new_train_data_loc,dst_file)
    cmd = cmd_cp1 + cmd_cp0
    print(cmd)
    if begin_run:
        os.system(cmd)


    final_res = ""
    if begin_run and "CONLL" in dataset_name:
        with open(dst_file,'r') as dst_f:
            with open(src_file,'r') as src_f:
                dst_lines = dst_f.readlines()
                src_lines = src_f.readlines()
                for i,src_line in enumerate( src_lines ):
                    dst_line = dst_lines[i]
                    merge_line = merge_info( src_line, dst_line )
                    final_res+=merge_line+"\n"
        with open(dst_file,'w') as f:
            f.write(final_res)
    #yaml_obj['model_name'] = dataname + str(it)
    yaml_obj['ner'][dataset_name]['data_folder']= dst_dir

    yaml_obj['ner'][dataset_name]['target_scheme_train']= "iob"
    yaml_obj['ner'][dataset_name]['target_scheme_test']= "iobes"
    yaml_obj['ner'][dataset_name]['target_scheme_dev']= "iobes"
    model_name =  dataname + str(it)
    yaml_obj['model_name'] = model_name
    with open( config_file,'w' ) as f:
        str_tmp = yaml.dump( yaml_obj ,indent = 4)
        f.write(str_tmp)
    cmd = "CUDA_VISIBLE_DEVICES=0 python train.py --config %s 2>&1|tee %s\n"%(config_file,dataname+"-log-"+str(it))
    cmd_gen = "CUDA_VISIBLE_DEVICES=0 python train.py --gen --test --config %s\n"%config_file
    new_train_data_loc="resources/taggers/%s/test.tsv"%(model_name)
    cmd = cmd+cmd_gen
    print(cmd)
    if begin_run:
        os.system(cmd)

#    cmd1="cp -r CLNER_datasets/"
process_each_iteration(1)
process_each_iteration(2)
process_each_iteration(3)
process_each_iteration(4)
#    with open(  )
#with 
