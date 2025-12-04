# mergeman
# 2024 Kanoguti

import os
import glob
import shutil
import sys
import pathlib

def fix_path(path):
    temp_return=pathlib.Path(path)
    if temp_return.is_absolute()==False:
        temp_return=temp_return.resolve()
    return str(temp_return)

def fix_separator(path):
    path=path.replace("\\","/")
    path=path.replace("/",os.sep)
    return path

def filelist(path):
    temp_list=[]
    for get in glob.glob(fix_path(path+"/**/*"),recursive=True):
        temp_list.append(get)
    return temp_list

def check_lua_path(lua_path_list,path):
    return_data=[]

    path=fix_path(path)

    for get_lua_path in lua_path_list:
        get_lua_path=fix_path(get_lua_path)
        question_mark_pos=get_lua_path.find("?",0)
        if question_mark_pos==-1:
            get_lua_path_a=get_lua_path
            get_lua_path_b=""
        else:
            get_lua_path_a=get_lua_path[:question_mark_pos]
            get_lua_path_b=get_lua_path[question_mark_pos+1:]

        if path.find(get_lua_path_a,0)==0:
            module_name=""
            temp_words=list(path.replace(os.getcwd()+os.sep,""))
            temp_flag=False
            for temp_word in temp_words:
                module_name+=temp_word
                if path==get_lua_path_a+module_name+get_lua_path_b:
                    temp_flag=True
                    break

            if temp_flag==True:
                return_data.append(module_name.replace(os.sep,"."))
        
    return return_data

def main():
    current_path=os.getcwd()

    DEFAULT_LUA_PATH="."+os.sep+"?.lua;."+os.sep+"?"+os.sep+"init.lua;"
    LUA_PATH=";;"
    if os.environ.get("LUA_PATH")!=None:
        LUA_PATH=os.environ.get("LUA_PATH")
    LUA_PATH=LUA_PATH.replace(";;",DEFAULT_LUA_PATH,1)
    LUA_PATH_list=LUA_PATH.split(";")
    LUA_PATH_list=[LUA_PATH_list[temp_cnt] for temp_cnt in range(len(LUA_PATH_list)) if LUA_PATH_list[temp_cnt]!=""]

    argv_data={}
    argv_data["project"]=None
    argv_data["entry"]=None
    argv_data["output"]=None
    argv_data["obfuscate"]=None
    argv_data["exclude"]=[]
    argv_data["clean"]=False
    argv_data["blank"]=False
    argv_data["protect"]=False

    if len(sys.argv)-1<=0:
        print("=Usage=")
        print("./mergeman --project <project directory> --entry <entry file> [--output <save file>] [--obfuscate <obfuscate count>] [--exclude <exclude path>] [--clean or --blank] [--protect]")
        print("")
        print("=Example=")
        print("./mergeman --project \"path/to/project\" --entry main.lua --output out.lua --obfuscate 1 --exclude \"path/to/exclude/dir\" --exclude \"path/to/exclude/script.lua\"")
        sys.exit()

    temp_mode=None
    for temp_cnt in range(1,len(sys.argv)):
        temp_get=sys.argv[temp_cnt]
        if temp_mode==None:
            if temp_get=="--project" and argv_data["project"]==None:
                temp_mode="project"
            elif temp_get=="--entry" and argv_data["entry"]==None:
                temp_mode="entry"
            elif temp_get=="--output" and argv_data["output"]==None:
                temp_mode="output"
            elif temp_get=="--obfuscate" and argv_data["obfuscate"]==None:
                temp_mode="obfuscate"
            elif temp_get=="--exclude":
                temp_mode="exclude"
            elif temp_get=="--clean" and argv_data["clean"]==False and argv_data["blank"]==False:
                argv_data["clean"]=True
            elif temp_get=="--blank" and argv_data["clean"]==False and argv_data["blank"]==False:
                argv_data["blank"]=True
            elif temp_get=="--protect":
                argv_data["protect"]=True
        else:
            if temp_mode=="project" and os.path.isdir(fix_path(temp_get))==True:
                argv_data["project"]=fix_path(temp_get)
            elif temp_mode=="entry" and argv_data["project"]!=None and os.path.isfile(fix_separator(argv_data["project"]+os.sep+temp_get))==True:
                argv_data["entry"]=temp_get
            elif temp_mode=="output" and argv_data["project"]!=None:
                argv_data["output"]=temp_get
            elif temp_mode=="obfuscate":
                argv_data["obfuscate"]=int(temp_get)
                if argv_data["obfuscate"]<0:
                    argv_data["obfuscate"]=0
                if argv_data["obfuscate"]>5:
                    argv_data["obfuscate"]=5
            elif temp_mode=="exclude":
                argv_data["exclude"].append(fix_separator(temp_get))
            temp_mode=None

    if argv_data["project"]==None:
        print("=Error=")
        print("Check the contents of the \"--project\" argument.")
        sys.exit()

    if argv_data["entry"]==None:
        print("=Error=")
        print("Check the contents of the \"--entry\" argument.")
        sys.exit()

    if argv_data["output"]==None:
        argv_data["output"]=argv_data["entry"]
    if os.path.isdir(fix_separator(argv_data["project"]+os.sep+argv_data["output"]).rsplit(os.sep,1)[0])==False:
        print("=Error=")
        print("Check the contents of the \"--output\" argument.")
        sys.exit()
    
    if argv_data["obfuscate"]==None:
        argv_data["obfuscate"]=0

    print("=Entered settings=")
    print("--project : \""+argv_data["project"]+"\"")
    print("--entry : \""+argv_data["entry"]+"\"")
    print("--output : \""+argv_data["output"]+"\"")
    print("--obfuscate : \""+str(argv_data["obfuscate"])+"\"")
    if len(argv_data["exclude"])>0:
        for temp_get in argv_data["exclude"]:
            print("--exclude : \""+temp_get+"\"")
    else:
        print("--exclude : None")
    if argv_data["clean"]==False:
        print("--clean : False")
    else:
        print("--clean : True")
    if argv_data["blank"]==False:
        print("--blank : False")
    else:
        print("--blank : True")
    if argv_data["protect"]==False:
        print("--protect : False")
    else:
        print("--protect : True")
    
    import_path=argv_data["project"]
    
    def temp_func(path):
        temp_return=None
        temp_cnt=0
        while(True):
            temp_return=path+"_export("+str(temp_cnt)+")"
            if os.path.isdir(temp_return)==False:
                break
            temp_cnt+=1
        return temp_return
    export_path=temp_func(import_path)

    shutil.copytree(import_path,export_path)

    os.chdir(export_path)

    LUA_PATH_list=[fix_path(LUA_PATH_list[temp_cnt]) for temp_cnt in range(len(LUA_PATH_list))]
    LUA_PATH_list=[LUA_PATH_list[temp_cnt].replace(export_path+os.sep,"",1) for temp_cnt in range(len(LUA_PATH_list)) if LUA_PATH_list[temp_cnt].find(export_path+os.sep,0)==0]

    export_files=filelist(export_path)

    temp_entry_data=""
    if os.path.isfile(argv_data["entry"])==True:
        temp_file=open(argv_data["entry"],"r",encoding="utf-8")
        temp_entry_data=temp_file.read()
        temp_file.close()

    cleaning_list=[]
    
    export_file=open(argv_data["output"],"w",encoding="utf-8")
    export_file.write("local ___defaultRequire=require"+"\n")
    export_file.write("local ___requireTable={}"+"\n")
    export_file.write("local function require(p_module)"+"\n")
    export_file.write("local module_name=p_module:gsub(\"/\",\".\")"+"\n")
    export_file.write("while module_name:find(\"..\",1,true)~=nil do module_name=module_name:gsub(\"%.%.\",\".\") end"+"\n")
    export_file.write("if ___requireTable[module_name]~=nil then return ___requireTable[module_name](p_module) end"+"\n")
    export_file.write("return ___defaultRequire(module_name)"+"\n")
    export_file.write("end"+"\n")

    for temp_get in export_files:
        temp_get_name=temp_get
        if temp_get_name.find(export_path)==0:
            temp_get_name=temp_get.replace(export_path+os.sep,"",1)

        module_name_list=check_lua_path(LUA_PATH_list,temp_get_name)

        temp_flag=False
        if len(module_name_list)>=1:
            if fix_separator(temp_get_name)!=fix_separator(argv_data["entry"]) and fix_separator(temp_get_name)!=fix_separator(argv_data["output"]):
                temp_flag=True
                if len(argv_data["exclude"])>0:
                    for temp_exclude in argv_data["exclude"]:
                        if os.path.exists(fix_separator(temp_exclude))==True:
                            if fix_separator(temp_get_name).find(fix_separator(temp_exclude))==0:
                                temp_flag=False
                                break

        if temp_flag==True:
            if argv_data["clean"]==True or argv_data["blank"]==True:
                cleaning_list.append(fix_separator(temp_get_name))
            
            if len(module_name_list)>=1:
                export_file.write("___requireTable[\""+ module_name_list[0] +"\"]=function(...)"+"\n")
                temp_file=open(fix_separator(temp_get_name),"r",encoding="utf-8")
                export_file.write(temp_file.read()+"\n")
                temp_file.close()
                export_file.write("end"+"\n")
                export_file.write("package.preload[\""+ module_name_list[0] +"\"]=___requireTable[\""+ module_name_list[0] +"\"]"+"\n")

                if len(module_name_list)>=2:
                    for temp_cnt in range(1,len(module_name_list)):
                        export_file.write("package.preload[\""+ module_name_list[temp_cnt] +"\"]=package.preload[\""+ module_name_list[0] +"\"]"+"\n")

    export_file.write(temp_entry_data+"\n")
    export_file.close()

    if argv_data["clean"]==True or argv_data["blank"]==True:
        temp_get_name=argv_data["entry"]
        if temp_get_name.find(export_path)==0:
            temp_get_name=temp_get.replace(export_path+os.sep,"",1)
        if(argv_data["entry"]!=argv_data["output"]):
            cleaning_list.append(fix_separator(temp_get_name))

    if argv_data["obfuscate"]>0:
        for temp_cnt in range(argv_data["obfuscate"]):
            temp_file=open(argv_data["output"],"r",encoding="utf-8")
            temp_data="".join([ r"\{:03d}".format(temp_byte) for temp_byte in temp_file.read().encode() ])
            temp_file.close()
            temp_file=open(argv_data["output"],"w",encoding="utf-8")
            temp_file.write("return loadstring(\""+ temp_data +"\")()")
            temp_file.close()

    if len(cleaning_list)>0:
        for temp_get in cleaning_list:
            if argv_data["clean"]==True:
                if os.path.exists(temp_get)==True:
                    os.remove(temp_get)
            elif argv_data["blank"]==True:
                temp_file=open(temp_get,"w",encoding="utf-8")
                temp_file.close()

    if argv_data["protect"]==False:
        temp_files=filelist(".")[::-1]
        for temp_file in temp_files:
            if os.path.isdir(temp_file):
                if len(filelist(temp_file))==0:
                    shutil.rmtree(temp_file)

    os.chdir(current_path)

    print("=Success!=")
    print(export_path)

if __name__=="__main__":
    main()