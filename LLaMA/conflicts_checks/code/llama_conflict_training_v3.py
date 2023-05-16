import sys
from tqdm import tqdm
from random import randint as ri
from concurrent.futures import ThreadPoolExecutor, as_completed

pl = []
with open('/mnt/p/name_dataset/salutation_list.txt','rt') as fi:
    pl = fi.readlines()
print(len(pl))
len_pl = len(pl)-1

nl = []
with open('/mnt/p/name_dataset/US_Pythonic_Clean.txt','rt') as fi:
    nl_r = fi.readlines()
nl = [x.split(',') for x in nl_r]
del nl_r
print(len(nl))
len_nl = len(nl)-1

cl = []
with open('/mnt/p/name_dataset/corp_list.txt','rt') as fi:
    cl_r = fi.readlines()
cl = [x.split(',') for x in cl_r]
del cl_r
print(len(cl))
len_cl = len(cl)-1

sf = []
with open('/mnt/p/name_dataset/short_form_names.txt','rt') as fi:
    sf_r = fi.readlines()
sf = [x.split(',') for x in sf_r]
del sf_r
print(len(sf))
len_sf = len(sf) -1

ln = []
with open('/mnt/p/name_dataset/LANG_NAME_CCU_UNIQ_FIXED.txt','rt') as fi:
    ln_r = fi.readlines()
ln = [x.split(',') for x in ln_r]
del ln_r
print(len(ln))
len_ln = len(ln)-1

waor = []
with open('/mnt/p/name_dataset/WAOR_ALPHA.txt','rt') as fi:
    waor = fi.readlines()
print(len(waor))
len_waor = len(waor)-1

def r_n()->int:
    rn = ri(0,len_nl)
    return rn
def r_sf()->int:
    rn = ri(0,len_sf)
    return rn
def r_ln()->int:
    rn = ri(0,len_ln)
    return rn
def r_ab()->int:
    rn = ri(0,25) 
    return rn+65
def r_nn()->int:
    rn = ri(3,5)
    return rn
def r_m()->int:
    rn = ri(1,10)
    return rn

def H_rand_name()->str:
    rn_str = ""
    rnn = r_nn()
    for i in range(1,abs(rnn)):
        rm1 = r_m()
        rm2 = r_m()        
        if rm1>3:
            rn_str = rn_str + f" {nl[r_n()][0]}{chr(32)}{nl[r_n()][1]}"
        else:
            if rm2>5:
                rn_str = rn_str + f" {nl[r_n()][0]}{chr(32)}{chr(r_ab())}.{chr(32)}{nl[r_n()][1]}"
            else:
                rn_str = rn_str + f" {nl[r_n()][0]}{chr(32)}{nl[r_n()][0]}{chr(32)}{nl[r_n()][1]}"
    return rn_str[:len(rn_str)-1].strip().replace(chr(10),';').strip()

def A_FML(cfh_l)->str:
    try:
        cf_q = ""
        cf_q_check = 0
        cf_syn = []
        if len(cfh_l)==2:
            cf_syn.append(str(f"%{cfh_l[0]}%{cfh_l[1]}%").replace('y','%').replace('an','%n').replace('en','%n').replace('ph','[pv]%'))
            cf_syn.append(str(f"%{cfh_l[1]}%{cfh_l[0]}%").replace('y','%').replace('an','%n').replace('en','%n').replace('ph','[pv]%'))
        elif len(cfh_l)==3:
            cf_syn.append(str(f"%{cfh_l[0]}%{cfh_l[2]}%").replace('y','%').replace('an','%n').replace('en','%n').replace('ph','[pv]%'))
            cf_syn.append(str(f"%{cfh_l[2]}%{cfh_l[0]}%").replace('y','%').replace('an','%n').replace('en','%n').replace('ph','[pv]%'))            
        for x in cf_syn:
            cf_q = cf_q + x + '\n'
    except Exception as e:
        print(e)
    return cf_q, cf_q_check

def A_rand_name(cfh)->str:
    arn = ""
    arn = arn + D.A_CF1
    cfh_s = cfh.split(';')
    for cfn in cfh_s:
        cfn = cfn.strip()
        cfh_l = [str(x).strip() for x in str(cfn).strip().split(chr(32))]
        acfh, cf_q_check = A_FML(cfh_l)
        arn = arn + str(acfh)
    return arn

def sc_1_gen()->str:
    cf_q_1 = ""
    cf_h_rn = H_rand_name()
    cf_a_rn = A_rand_name(cf_h_rn)     
    cf_q_1 = cf_q_1 + D.H_CF1 + D.H_1 + cf_h_rn + '\n' + cf_a_rn
    cfc = ""
    cfc = cf_q_1.replace(str(cf_q_1 + D.H_CF1 + D.H_1 + cf_h_rn + '\n').strip(),'')
    return cf_q_1, len(cfc)

class D:
    H_1 = "Human: "
    H_CF1 = "Human: I need to run a ProLaw Conflicts Check on the following names separated by a semicolon:\n"
    A_1 = "Assistant: "
    A_CF1 = "Assistant: Here is the proper syntax for a Conflicts Check on those names:\n"
    H_CF2 = "Human: what are some of the alternate spellings for "
    A_CF2 = "Assistant: Here are variations of the name "

def SCENARIO_1():
    sc_check = True
    while sc_check is True:
        cf_q_1,cfc = sc_1_gen()
        if cfc > 20:
            sc_check = False
            break
        if cfc < 20:
            continue
    with open("/mnt/p/name_dataset/training/cf_names.txt","a") as fi:
        fi.write(cf_q_1)
        fi.write('\n\n')

def sc_2_names():
    lnsf = ri(1,2)
    cf2_l = []
    cf2_str = ""
    if lnsf == 1:
        lnsf_r = ln[r_ln()]
        cf2_n = lnsf_r[ri(0,len(lnsf_r)-1)]
        cf2_n = cf2_n.strip()
        for x in ln:
            xs = [ll.lower() for ll in x]
            if cf2_n.strip().lower() in xs:
                for xln in xs:
                    cf2_l.append(xln.strip().replace(chr(10),''))
    if lnsf == 2:
        lnsf_r = sf[r_sf()]
        cf2_n = lnsf_r[ri(0,len(lnsf_r)-1)]
        cf2_n = cf2_n.strip()
        for x in sf:
            xs = [ll.lower() for ll in x]
            if cf2_n.strip().lower() in xs:
                for xln in xs:
                    cf2_l.append(xln.strip().replace(chr(10),''))
    cf2_str = cf2_str + D.H_CF2 + cf2_n + '\n' + D.A_CF2.strip() + ' ' +  cf2_n.strip() + '\n' + D.A_1
    for x in cf2_l:
        cf2_str = cf2_str + x + ', '
    cf2_str = cf2_str.strip()
    cf2_str = cf2_str[:len(cf2_str)-1]
    cf2_check = len(cf2_l)
    return cf2_str,cf2_check

def SCENARIO_2():
    cf2_iter = True
    while cf2_iter is True:
        cf2_str,cf2_check = sc_2_names()
        if cf2_check>=2:
            cf2_iter = False
            continue
        else:
            continue

    with open("/mnt/p/name_dataset/training/cf_names.txt","a") as fi:
        fi.write(cf2_str)
        fi.write('\n\n\n')

def run(i):
    i = i - 1
    SCENARIO_1()
    i = i + 1

def main():
    try:
        with ThreadPoolExecutor(32) as executor:
            futures = [executor.submit(run, i) for i in range(0,20000)]
            for _ in as_completed(futures):
                status_bar.update(n=1)
    except KeyboardInterrupt:
        sys.exit()
    except Exception as e:
        print(e)
        pass
    finally: pass

status_bar = tqdm(total=20000, desc='Scenarios')

with open("/mnt/p/name_dataset/training/cf_names.txt","wt") as fi:
    fi.write("")

main()
