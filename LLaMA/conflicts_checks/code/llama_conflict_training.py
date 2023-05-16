import os,sys
from tqdm import tqdm
from random import randint as ri
from traceback_with_variables import activate_by_import
from concurrent.futures import ThreadPoolExecutor, as_completed
import numpy as np
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
nltk.download('punkt')
from nltk.tokenize import word_tokenize
from datetime import datetime

os.system('cls' if os.name == 'nt' else 'clear')

class D:
    H_1 = "Human: "
    H_CF1 = "Human: I need to run a ProLaw Conflicts Check on the following names separated by a semicolon:\n"
    H_CF1 = "Human: Parse and reformat the names for an SQL search using alternate spellings for names.\n"
    H_CF2 = "Human: "
    A_1 = "Assistant: "
    A_CF1 = "Assistant: Here is the proper syntax for a Conflicts Check on those names:\n"
    

pre = []
with open('/mnt/p/name_dataset/prefix_etl.txt','rt') as fi:
    pre_r = fi.readlines()
pre = [str(x).lower().strip() for x in pre_r]
del pre_r
len_pre = len(pre)-1
cl = []
with open('/mnt/p/name_dataset/corps_etl.txt','rt') as fi:
    cl_r = fi.readlines()
cl = [str(x).lower().strip() for x in cl_r]
del cl_r
len_cl = len(cl)-1
sf = []
with open('/mnt/p/name_dataset/sf_name_etl.txt','rt') as fi:
    sf_r = fi.readlines()
sf = [str(x).lower().strip() for x in sf_r]
del sf_r
len_sf = len(sf) -1
fd = []
with open('/mnt/p/name_dataset/f_dim_etl.txt','rt') as fi:
    fd_r = fi.readlines()
fd = [str(x).strip() for x in fd_r]
del fd_r
len_fd = len(fd) -1
md = []
with open('/mnt/p/name_dataset/m_dim_etl.txt','rt') as fi:
    md_r = fi.readlines()
md = [str(x).lower().strip() for x in md_r]
del md_r
len_md = len(md) -1
ln = []
with open('/mnt/p/name_dataset/lang_name_etl.txt.txt','rt') as fi:
    ln_r = fi.readlines()
ln = [str(x).lower().strip() for x in ln_r]
del ln_r
len_ln = len(ln)-1
waor = []
with open('/mnt/p/name_dataset/waor_etl.txt','rt') as fi:
    waor_r = fi.readlines()
waor = [str(x).lower().strip() for x in waor_r]
del waor_r
len_waor = len(waor)-1
nl = []
with open('/mnt/p/name_dataset/US_Pythonic_Clean.txt','rt') as fi:
# with open('/mnt/p/name_dataset/nl_test_set.txt','rt') as fi:
    nl_r = fi.readlines()
nl = [x.split(',') for x in nl_r]
del nl_r
len_nl = len(nl)-1
nl_f = [x[0] for x in nl]
nl_l = [x[1] for x in nl]
replace_list = [
[f"holdings",f"%hold%"],
[f"management",f"%m%g%m%t%"],
[f"mgmt.",f"%m%g%m%t%"],
[f"mgmt",f"%m%g%m%t%"],
[f"company",f"%co%"],
[f"co",f"%co%"],
[f"co.",f"%co%"],
[f"corporation",f"%co%"],
[f"corp.",f"%co%"],
[f"limited",f"%l%t%d%"],
[f"ltd",f"%l%t%d%"],
[f"ltd.",f"%l%t%d%"],
[f"l.t.d.",f"%l%t%d%"],
[f"incorporated",f"%inc%"],
[f"inc",f"%inc%"],
[f"inc.",f"%inc%"],
[f"limited partnership",f"%l%p%"],
[f"lp",f"%l%p%"],
[f"lp.",f"%l%p%"],
[f"l.p.",f"%l%p%"],
[f"limited liability partnership",f"%l%l%p%"],
[f"llp",f"%l%l%p%"],
[f"llp.",f"%l%l%p%"],
[f"l.l.p.",f"%l%l%p%"],
[f"limited liability limited partnership",f"%l%l%l%p%"],
[f"lllp",f"%l%l%l%p%"],
[f"lllp.",f"%l%l%l%p%"],
[f"l.l.l.p.",f"%l%l%l%p%"],
[f"registered limited liability partnership",f"%r%l%l%p%"],
[f"rllp",f"%r%l%l%p%"],
[f"rllp.",f"%r%l%l%p%"],
[f"r.l.l.p.",f"%r%l%l%p%"],
[f"registered limited liability limited partnership",f"%r%l%l%l%p%"],
[f"rlllp",f"%r%l%l%l%p%"],
[f"rlllp.",f"%r%l%l%l%p%"],
[f"r.l.l.l.p.",f"%r%l%l%l%p%"],
[f"limited liability company",f"%l%l%c%"],
[f"llc",f"%l%l%c%"],
[f"llc.",f"%l%l%c%"],
[f"l.l.c.",f"%l%l%c%"],
[f"holding company",f"%hol%co%"],
[f"holdco",f"%hol%co%"],
[f"holdco.",f"%hol%co%"],
[f"opco",f"%op%co%"],
[f"opco.",f"%op%co%"],
[f"trust",f"%tr%"],
[f"charitable trust",f"%ch%tr%"],
[f"manufacturing",f"%m%f%r%"],
[f"mfr",f"%m%f%r%"],
[f"mfr.",f"%m%f%r%"],
[f"l3c",f"%l%3%c%"],
[f"l3c.",f"%l%3%c%"],
[f"slp",f"%s%l%p%"],
[f"slp.",f"%s%l%p%"],
[f"cio",f"%c%i%o%"],
[f"cio.",f"%c%i%o%"],
[f"c.i.o.",f"%c%i%o%"],
[f"cic",f"%c%i%c%"],
[f"cic.",f"%c%i%c%"],
[f"c.i.c.",f"%c%i%c%"],
[f"ag",f"%a%g%"],
[f"ag.",f"%a%g%"],
[f"a.g.",f"%a%g%"],
[f"gmbh",f"%g%m%b%h%"],
[f"gmbh.",f"%g%m%b%h%"],
[f"plc",f"%p%l%c%"],
[f"plc.",f"%p%l%c%"],
[f"p.l.c.",f"%p%l%c%"],
[f"gp",f"%g%p%"],
[f"gp.",f"%g%p%"],
[f"gmk",f"%g%m%k%"],
[f"gmk.",f"%g%m%k%"],
[f"gsk",f"%g%s%k%"],
[f"gsk.",f"%g%s%k%"],
[f"sarf",f"%s%a%r%f%"],
[f"sarf.",f"%s%a%r%f%"],
[f"s.a.r.f.",f"%s%a%r%f%"],
[f"sp",f"%s%p%"],
[f"sp.",f"%s%p%"],
[f"s.p.",f"%s%p%"],
[f"sa",f"%s%a%"],
[f"sa.",f"%s%a%"],
[f"s.a.",f"%s%a%"],
[f"pllc",f"%p%l%l%c%"],
[f"pllc.",f"%p%l%l%c%"],
[f"p.l.l.c.",f"%p%l%l%c%"],
[f"ohg",f"%o%h%g%"],
[f"ohg.",f"%o%h%g%"],
[f"o.h.g.",f"%o%h%g%"],
[f"gbr",f"%g%b%r%"],
[f"ab sa",f"%a%b%s%a%"],
[f"ab. sa.",f"%a%b%s%a%"],
[f"a.b. s.a.",f"%a%b%s%a%"],
[f"ab",f"%a%b%"],
[f"ab.",f"%a%b%"],
[f"a.b.",f"%a%b%"],
[f"ick",f"i[ck]%"],
[f"phe",f"%[pv]%e%"],
[f"ea",f"%[ea]%"],
[f"ae",f"%[ae]%"],
[f"yan",f"%[iy]an"],
[f"ll",f"%l%"],
[f"pp",f"%p%"],
[f"tt",f"%t%"],
[f"mm",f"%m%"],
[f"usa",f"u[zs]a"],
[f"asm",f"a[sz]m"],
[f"jon",f"jo%n%"],
[f"ohn",f"o%n"],
[f"ron",f"r[aieyo]n"],
[f"rin",f"r[aieyo]n"],
[f"ren",f"r[aieyo]n"],
[f"ryn",f"r[aieyo]n"],
[f"ran",f"r[aieyo]n"],
[f"dd",f"%d%"],
[f"li",f"l[iy]%"],
[f"ry",f"r[yi]%"],
[f"ts",f"t[sz]"],
[f"tz",f"t[sz]"],
[f"dd",f"%d%"],
[f"nn",f"%n%"],
[f"eph",f"%e[fp]%"],
[f"mc",f"%m%c%"],
[f"itt",f"%it%"],
[f"att",f"%at%"],
[f"ett",f"%et%"],
[f"az",f"%a[sz]%"],
[f"as",f"%a[sz]%"],
[f"rr",f"%r%"],
[f"ich",f"i%ch%"]]


def r_nl()->int:
    rn = ri(0,len_nl)
    return rn
def r_sf()->int:
    rn = ri(0,len_sf)
    return rn
def r_fd()->int:
    rn = ri(0,len_fd)
    return rn
def r_md()->int:
    rn = ri(0,len_md)
    return rn
def r_ln()->int:
    rn = ri(0,len_ln)
    return rn
def r_pre()->int:
    rn = ri(0,len_pre)
    return rn
def r_waor()->int:
    rn = ri(0,len_waor)
    return rn
def r_ab()->int:
    rn = ri(0,25) 
    return rn+65
def r_nn()->int:
    rn = ri(2,2)
    return rn
def r_m()->int:
    rn = ri(1,10)
    return rn
def r_pr()->int:
    rn = ri(1,10)
    return rn
def H_rand_name()->str:
    rn_str = ""
    rnn = r_nn()
    pr_n = r_pr()
    for i in range(1,abs(rnn)):
        rm1 = r_m()
        rm2 = r_m()
        pr_n = r_pr()
        if rm1<=3:
            if pr_n>=5:
                rn_str = rn_str + f" {nl[r_nl()][0]}{chr(32)}{nl[r_nl()][1]};"
            else:
                rn_str = rn_str + f" {pre[r_pre()]}{chr(32)}{nl[r_nl()][0]}{chr(32)}{nl[r_nl()][1]};"
        if rm1>=4 and rm1<=5:
            rn_str = rn_str + f" {waor[r_waor()]} companycompanycompany;"
        else:
            if rm2>5:
                if pr_n>=5:
                    rn_str = rn_str + f" {nl[r_nl()][0]}{chr(32)}middlenamemiddlenamemiddlename{chr(32)}{chr(r_ab())}.{chr(32)}{nl[r_nl()][1]};"
                else:
                    rn_str = rn_str + f" {pre[r_pre()]}{chr(32)}{nl[r_nl()][0]}{chr(32)}middlenamemiddlenamemiddlename{chr(32)}{chr(r_ab())}.{chr(32)}{nl[r_nl()][1]};"
            else:
                if pr_n>=5:
                    rn_str = rn_str + f" {nl[r_nl()][0]}{chr(32)}{nl[r_nl()][0]}{chr(32)}{nl[r_nl()][1]};"
                else:
                    rn_str = rn_str + f" {pre[r_pre()]}{chr(32)}{nl[r_nl()][0]}{chr(32)}middlenamemiddlenamemiddlename{chr(32)}{nl[r_nl()][0]}{chr(32)}{nl[r_nl()][1]};"
    return rn_str[:len(rn_str)-1].strip().replace(chr(10),'')
def A_FML(cfh_l)->str:
        
        cf_q = ""
        n_list = []
        n_list = [str(x).lower().strip().replace(chr(10),'') for x in cfh_l]
        if cfh_l[len(cfh_l)-1]!='companycompanycompany':
            for i in range(0,len(cfh_l)-1):
                if cfh_l[i] == 'companycompanycompany':
                    cfh_l.pop(i)
                if cfh_l[i] == 'middlenamemiddlenamemiddlename':
                    cfh_l.pop(i)
            for x in ln:
                xs = [n.lower() for n in x.split(',')]
                if str(cfh_l[0]).strip().lower() in xs:
                    for xln in xs:
                        if set(str(cfh_l[0]).strip().lower()).issubset(set(xln)):
                            if len(n_list)==0:
                                n_list.append(xln.lower().strip().replace(chr(10),''))
                            else:
                                n_list.append(xln.lower().strip().replace(chr(10),''))
            for x in sf:
                xs = [n.lower() for n in x.split(',')]
                if str(cfh_l[0]).strip().lower() in xs:
                    for xln in xs:
                        if set(str(cfh_l[0]).strip().lower()).issubset(set(xln)):
                            if len(n_list)==0:
                                n_list.append(xln.lower().strip().replace(chr(10),''))
                            else:
                                n_list.append(xln.lower().strip().replace(chr(10),''))
            for x in fd:
                xs = [n.lower() for n in x.split(',')]
                if str(cfh_l[0]).strip().lower() in xs:
                    for xln in xs:
                        if set(str(cfh_l[0]).strip().lower()).issubset(set(xln)):
                            if len(n_list)==0:
                                n_list.append(xln.lower().strip().replace(chr(10),''))
                            else:
                                n_list.append(xln.lower().strip().replace(chr(10),''))
            for x in md:
                x_l = x.split(',')
                xs = [n.lower() for n in x_l]
                if str(cfh_l[0]).strip().lower() in xs:
                    for xln in xs:
                        if set(str(cfh_l[0]).strip().lower()).issubset(set(xln)):
                            if len(n_list)==0:
                                n_list.append(xln.lower().strip().replace(chr(10),''))
                            else:
                                n_list.append(xln.lower().strip().replace(chr(10),''))
        q_list = []
        qhl = []
        chl = []
        if cfh_l[len(cfh_l)-1]!='companycompanycompany':
            for i in range(0,len(cfh_l)-1):
                if cfh_l[i] == 'companycompanycompany':
                    cfh_l.pop(i)
                if cfh_l[i] == 'middlenamemiddlenamemiddlename':
                    cfh_l.pop(i)
            qx = ""
            qx = str(cfh_l[0]).lower()
            for r in replace_list:
                qx = qx.replace((r[0]),(r[1]))
            qhl.append(qx)
            del qx
            qx = ""
            qx = str(cfh_l[1]).lower()
            for r in replace_list:
                qx = qx.replace(str(r[0]),str(r[1]))
            qhl.append(qx)
            for x in n_list:
                nx = ""
                nx = str(x).lower()
                for r in replace_list:
                    nx = nx.replace(str(r[0]),str(r[1]))
                q_list.append(nx)
                del nx
            qr = []
            qr.append(str('%'+qhl[0]+'%'+qhl[1]+'%\n'))
            qr.append(str('%'+qhl[1]+'%'+qhl[0]+'%\n'))
            if len(q_list)>2:
                for x in q_list:
                    if qhl[1] != x:
                        qr.append(str('%'+qhl[1]+'%'+x+'%\n'))
                        qr.append(str('%'+x+'%'+qhl[1]+'%'+'\n'))
            q_list.clear()
            q_list = [x for x in np.unique(np.array(qr)).tolist()]
            qr.clear()
            qr = [x for x in np.unique(np.array(q_list)).tolist()]
            for x in qr:
                cf_q = cf_q + str(x).replace(str(qhl[0]+qhl[0]+'\n'),'').replace(str(qhl[1]+qhl[1]+'\n'),'')
            return cf_q.replace(chr(37)+chr(37),chr(37))
        if cfh_l[len(cfh_l)-1]=='companycompanycompany':
            cfh_l.pop(len(cfh_l)-1)
            for x in cfh_l:
                cx = ""
                cx = str(x).lower()
                for r in replace_list:
                    cx = cx.replace(str(r[0]),str(r[1]))
                if cx[:1]=="s":
                    cx = cx[:len(cx)-1]                    
                chl.append(cx)
            for x in chl:
                cf_q = cf_q +'%' + x
            cf_q = cf_q +'%\n'
            return cf_q.replace(chr(37)+chr(37),chr(37))
        
alpha_whitelist = set(f'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890 ')

def A_rand_name(cfh)->str:
    arn = ""
    arn = arn + D.A_CF1
    cfh = str(cfh).replace(chr(32)+chr(32),chr(32))
    cfh = cfh.replace(chr(32)+chr(32),chr(32))
    cfh = cfh.replace(chr(32)+chr(32),chr(32))
    cfh_s = cfh.split(';')
    for cfn in cfh_s:
        cfh_l = []
        cfh_l = str(cfn).lower().strip().split(chr(32))
        all_words = ""
        for x in cfh_l:
            all_words = all_words + x + " "
        all_words = all_words.strip().replace('\n','')
        text_tokens = word_tokenize(all_words)
        no_stop_words = []
        no_stop_words.clear()
        stops = stopwords.words('english')
        no_stop_words = [s for s in text_tokens if s.lower() not in stops and not len(s) < 2]
        cfh_l.clear()
        cfh_sw = [x for x in no_stop_words if x not in pre]
        for x in cfh_sw:
            x_str = ""
            x_strip = [''.join(str(l) for l in c if l in alpha_whitelist) for c in str(x)]
            for c in x_strip:
                x_str = x_str + c
            cfh_l.append(x_str)
            del x_str
        if cfh_l[1]=='middlenamemiddlenamemiddlename' and len(cfh_l)==4:
            cfh_l.pop(1)
            cfh_l.pop(1)
        acfh = A_FML(cfh_l)
        arn = arn + str(acfh)
    return arn

def SCENARIO_1():
        cf_q_1=""
        cf_h_rn = H_rand_name()
        cf_a_rn = A_rand_name(cf_h_rn)
        cf_h_rn = cf_h_rn.replace('companycompanycompany','').replace('middlenamemiddlenamemiddlename','')
        cf_q_1 = str(D.H_CF1 + D.H_1 + cf_h_rn + chr(10) + cf_a_rn)
        with open("/mnt/p/name_dataset/training/cf_names.txt","a") as fi:
            fi.write(cf_q_1+'\n\n')

def run(i):
    i = i
    SCENARIO_1()
    i = i
        
def main():
    with ThreadPoolExecutor(16) as executor:
        futures = [executor.submit(run, i) for i in range(1,10000)]
        for _ in as_completed(futures):
            status_bar.update(n=1)

status_bar = tqdm(total=10000, desc='Scenarios')

with open("/mnt/p/name_dataset/training/cf_names.txt","wt") as fi:
    fi.write("")

main()
