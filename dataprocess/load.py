import json

with open("contactsCN.json",'r') as load_cn:
     load_CN = json.load(load_cn)
     
with open("contactsEN.json",'r') as load_en:
     load_EN = json.load(load_en)
     
ita=iter(load_CN)
itb=iter(load_EN)
result=[]
while True:
    try :
        a=next(ita)
        b=next(itb)
        result.append({'name' : a['name']+" "+b['name'],'title' : a['title']+" "+b['title'],'office': a['office'],'tel':a['tel'],'email':a['email'],'imageUrl':a['imageUrl'],'selfIntrUrl':a['selfIntrUrl']})       
    except StopIteration:
        break
print(result)
with open("../data/contacts.json","w") as dump_f:
    json.dump(result,dump_f,ensure_ascii=False)