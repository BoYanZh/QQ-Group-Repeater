import json
def getemail(this):
    return this['email']

with open("contactsCN.json", 'r') as load_cn:
    load_CN = json.load(load_cn)
    load_CN.sort(key=getemail)
with open("contactsEN.json", 'r') as load_en:
    load_EN = json.load(load_en)
    load_EN.sort(key=getemail)

ita = iter(load_CN)
itb = iter(load_EN)
result = []
while True:
    try:
        a = next(ita)
        b = next(itb)
        if (a['email']==b['email']):
            result.append({'name': a['name']+" "+b['name'], 'title': a['title']+" "+b['title'], 'office': a['office'],
                      'tel': a['tel'], 'email': a['email'], 'imageUrl': a['imageUrl'], 'selfIntrUrl': a['selfIntrUrl']})
        else : print("Wrong pair.")
    except StopIteration:
        break
print(result)
with open("../data/contacts.json", "w") as dump_f:
    json.dump(result, dump_f, ensure_ascii=False)
