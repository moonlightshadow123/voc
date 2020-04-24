import requests
import json
import re
from utils import try_deco, print_f
dict_key = "28807962-c095-4619-9eab-47b83f2e88c9"
thes_key = "5ad3d92b-b84a-474a-b498-1627051c0b60"
dict_url = "https://www.dictionaryapi.com/api/v3/references/collegiate/json/{}?key={}"
thes_url = "https://www.dictionaryapi.com/api/v3/references/thesaurus/json/{}?key={}"
audi_url = "https://media.merriam-webster.com/soundc11/{}/{}.wav"
temp_name = "temp.wav"

def searchKey(data, skey):
    # res = None
    if type(data) == list:
        for each in data:
            subres = searchKey(each, skey)
            if subres != None:
                return subres
    if type(data) == dict:
        for key,val in data.items():
            if key == skey:
                return val
            else:
                subres = searchKey(val, skey)
                if subres != None:
                    return subres
    return None

def searchAll(data, skey):
    # print("hello")
    res = []
    if type(data) == list:
        for each in data:
            subres = searchAll(each, skey)
            if subres != None:
                res += subres
    if type(data) == dict:
        for key,val in data.items():
            if key == skey:
                # print(val)
                res.append(val)
            subres = searchAll(val, skey)
            if subres != None:
                res += subres
    return res
 
def searchAllPS(data, skey, psdata, pskey):
    # print("hello")
    res = []
    if type(data) == list:
        for each in data:
            subres = searchAllPS(each, skey, psdata, pskey)
            if subres != None:
                res += subres
    if type(data) == dict:
        for key,val in data.items():
            if key == skey:
                # print(val)
                if type(val) == dict: val[pskey] = psdata
                elif type(val) == list: val.append([pskey, psdata]) 
                res.append(val)
            elif key == pskey:
                psdata = val
            subres = searchAllPS(val, skey, psdata, pskey)
            if subres != None:
                res += subres
    return res

class MWapi:

    @try_deco
    def lookup(self, word):
        # requests
        dict_data = self.getDict(word)
        thes_data = self.getThes(word)
        self.downAudio(searchKey(dict_data, "audio"))
        # print(dict_data)
        # data process
        defs = self.getDefs(dict_data)
        stems = self.getStems(dict_data)
        syns = self.getSyns(thes_data)
        ants = self.getAnts(thes_data)
        # print("Definitions:")
        print_f([("class:info", "Definitions:        ")])
        for idx,item in enumerate(defs):
            # print(item)
            arr = []
            string = "    {}. ".format(idx); arr.append(("class:warning", string))
            if item["fl"]: string = "*{}* ".format(item["fl"].upper()); arr.append(("class:danger", string))
            string = "{}. ".format(item["text"].strip()); arr.append(("class:success", string))
            if item["vis"]: arr.append(("class:danger", "*EG*"));string = " {}.".format(item["vis"].strip(".")); arr.append(("class:primary", string))
            print_f(arr)
            # else: print("\t{}. {}.".format(idx, item["text"]))
            # print(string)
        if stems:
            print_f([("class:info", "Stems:        ")])
            print_f([('class:warning','    '),('class:primary',', '.join(stems))])
            # print_f("\t{}".format(", ".join(stems)))
        # for idx, item in enumerate(stems):
        #    print("\t{}. {}".format(idx, item))
        if syns:
            print_f([("class:info", "Synonyms:        ")])
            print_f([('class:warning','    '),('class:primary',', '.join(syns))])
        #for idx, item in enumerate(syns):
        #    print("\t{}. {}".format(idx, item))
        if ants:
            print_f([("class:info", "Antonyms:        ")])
            print_f([('class:warning','    '),('class:primary',', '.join(ants))])
        #for idx, item in enumerate(ants):
        #    print("\t{}. {}".format(idx, item))

    def processStr(self, string):
        # print(string)
        string = re.sub(r"\{([^\|]*?)\}", r"", string)
        string = re.sub(r"\{([^\|]*?)\|([^\|]*?)\}", r"\g<2>", string)
        string = re.sub(r"\{([^\|]*?)\|([^\|]*?)\|([^\|]*?)\}", r"\g<2>", string)
        string = re.sub(r"\{([^\|]*?)\|([^\|]*?)\|([^\|]*?)\|([^\|]*?)\}", r"\g<2>", string)
        return string

    '''Requests related'''

    @try_deco
    def downAudio(self, audio):
        if not audio: return
        subd = ""
        if re.match(r"bix.*", audio):
            subd = "bix"
        elif re.match(r"gg.*", audio):
            subd = "gg"
        elif re.match(r"[^a-zA-Z].*", audio):
            subd = "number"
        else:
            subd = audio[0]
        url = audi_url.format(subd, audio)
        res = requests.get(url)  
        with open(temp_name, 'wb') as f:
            f.write(res.content)

    @try_deco
    def getDict(self, word):
        url = dict_url.format(word, dict_key)
        res = requests.get(url)
        json_data = json.loads(res.text)
        return json_data

    @try_deco
    def getThes(self, word):
        url = thes_url.format(word,thes_key)
        res = requests.get(url)
        json_data = json.loads(res.text)
        return json_data

    '''From Dict'''

    def getDefs(self, data):
        data = searchAllPS(data, "dt", "", "fl")
        res = []
        for eachDt in data:
            cur_dict = {"text":"", "vis":"", "fl":""}
            for item in eachDt:
                if len(item) < 2:
                    continue
                if item[0] == "text":
                    cur_dict["text"] = self.processStr(item[1])
                elif item[0] == "vis":
                    cur_dict["vis"] = self.processStr(item[1][0]["t"])
                elif item[0] == "fl":
                    cur_dict["fl"] = self.processStr(item[1])
            if cur_dict["text"] != "" : res.append(cur_dict)
        return res

    def getStems(self, data):
        data = searchKey(data, "stems")
        return data if data else None

    ''' From Thes'''

    def getSyns(self, data):
        data = searchKey(data, "syns")
        return data[0] if data else None

    def getAnts(self, data):
        data = searchKey(data, "ants")
        return data[0] if data else None


if __name__ == "__main__":
    mw = MWapi()
    mw.lookup("after")