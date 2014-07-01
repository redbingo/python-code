import os
import socket,shutil
import magic
def is_alive(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
       sock.bind(('localhost', int(port)))
       sock.bind(('localhost', int(port)))
       #sock.close()
       return False 
    except Exception,e:
       print e
       sock.close()
       return True 

def is_alive2(port):
    net_tcp = "/proc/net/tcp"
    f_tcp = open(net_tcp, 'r')
    lines = f_tcp.readlines()
    for line in lines:
        line_list = line.split(' ')
        if len(line_list) >= 2: 
           line_port = line_list[1].split(':')
           if len(line_port) >= 2:
               if int(port) == int(line_port[1],16):
                   return True 
    return False 

def is_alive3(port):
    port = str(hex(int(port)))[2:].upper()
    print port
    net_tcp = "/proc/net/tcp"
    f_tcp = open(net_tcp, 'r')
    lines = f_tcp.read()
    f_tcp.close()
    if lines.find(':'+port+' ') > -1:
        return True
    else:
        return False

def cp_rf(from_dir, to_dir):
        from_list = []
        to_list = []
        if '/' == from_dir[-1]:
            from_dir = from_dir[0:-1]
        base = os.path.basename(from_dir)
        if not os.path.exists(to_dir):
            shutil.copytree(from_dir, to_dir)
        else:
            from_list = os.listdir(from_dir)
            if from_list:
                 to_list = os.listdir(to_dir)
                 for from_f in from_list:
                     abs_from = os.path.join(from_dir, from_f)
                     if os.path.isfile(abs_from):
                         if from_f in to_list:
                             abs_to = os.path.join(to_dir, from_f)
                             if os.path.isfile(abs_to):  
                                 os.remove(abs_to)
                         shutil.copy(os.path.join(from_dir, from_f), \
                                 os.path.join(to_dir, from_f))
        return
        
def get_procids(procname, is_all = True):
    id_list = []
    path = '/proc'
    for f in os.listdir(path):
        if f.isdigit():
            abs_f = os.path.join(path, f)
            if os.path.isdir(abs_f):
                f_r = open(os.path.join(abs_f, 'status'), 'r')
                line = f_r.readline()
                f_r.close()
                if line:
                    key_v = line.split(':')
                    if len(key_v) >= 2:
                       name = key_v[1].strip()
                       if name == procname:
                          id_list.append(int(f))
                          if not is_all:
                             break
    return id_list  

def rm_dirs(root, n = 0):
        dir_list = []
        if root:
           tmp_list = os.listdir(root)
           if tmp_list:
                for f in tmp_list:
                    dir =  os.path.join(root,f)
                    if os.path.isdir(dir):
                        dir_list.append(dir)
                        result_list = rm_dirs(dir, n + 1)
                        if result_list:
                             dir_list = dir_list + result_list
                        os.rmdir(dir)
                    else:
                        os.remove(dir)
           if 0 == n:
              os.rmdir(root)
        return dir_list

def cp_dirs(root, dst_dir):
    dir_list = []
    if root:
       if '/' == root[-1]:
            root = root[0:-1]
       base = os.path.basename(root)
       dst_dir = os.path.join(dst_dir, base)
       if not os.path.exists(dst_dir):
           os.makedirs(dst_dir)
       print dst_dir
       tmp_list = os.listdir(root)
       if tmp_list:
            for f in tmp_list:
                dir =  os.path.join(root,f)          
                if os.path.isdir(dir):
                    dir_list.append(dir)
                    result_list = cp_dirs(dir, dst_dir)
                    if result_list:
                         dir_list = dir_list + result_list
                else:
                    dst_f = os.path.join(dst_dir, f)
                    print dst_f 
                    if os.path.exists(dst_f):
                        os.remove(dst_f)
                    shutil.copy(dir, dst_f)
    return dir_list

if __name__ == '__main__':
   port = 50021 
   print is_alive(port)
   print is_alive2(port)
   print is_alive3(port)
   path = '/test/data'
   print "______________",get_procids('apatch')
   file_list = os.listdir(path)
   #cp_rf('/test/a','/tmp/b')
   #cp_rf('/test/a','/tmp/b')
   #tmp_list = get_dirs('/data/test')
   #cp_dirs('/test/a','/tmp')
   rm_dirs('/tmp/23/')