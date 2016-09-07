# -*- coding: utf-8 -*-
class smart_button:
    def __init__(self, btn_num = 10):
        self.__btn_dic = {}
        self.__btn_num = btn_num
        self.__btn_running_num = 0
    def UpdateButton(self, content):
        del_btn_name = None
        print("try add {}".format(content))
        self.__btn_running_num = self.__btn_running_num + 1
        if len(content) is 0:
            return del_btn_name
        #check content exist
        #if self.__btn_dic.has_key(content) is True:
        if content in self.__btn_dic is True:
            #print("key exist")
            weight = self.__btn_dic[content]
            self.__btn_dic.update({content:[(weight[0] + 1), self.__btn_running_num]})
        else:
            #print("key not exist")
            #Add key if passable
            if (len(self.__btn_dic) >= self.__btn_num):
                #do reweight
                key_list = self.__btn_dic.keys()
                weight_list = self.__btn_dic.values()
                sorted_weight_list = sorted(weight_list)
                if (sorted_weight_list[0][0] == 0):
                    del_running_num = sorted_weight_list[0][1]
                    # del key
                    for i in range(self.__btn_num):
                        if weight_list[i][1] == del_running_num:
                            del self.__btn_dic[key_list[i]]
                            del_btn_name = key_list[i]
                            key_list[i] = content
                            weight_list[i] = [1, self.__btn_running_num]
                            self.__btn_dic[content] = [1, self.__btn_running_num]
                            break
                # reweight
                for i in range(self.__btn_num):
                    if weight_list[i][0] > 0:
                        self.__btn_dic[key_list[i]] = [weight_list[i][0] - 1, weight_list[i][1]]
            else:
                self.__btn_dic[content] = [0, self.__btn_running_num]
        return del_btn_name
    def Debug(self):
        print(self.__btn_dic)

    def DeleteButton(self, content):
        del self.__btn_dic[content]
        return 0

    def ForceButton(self, content):
        # TODO:
        return 0

    def UnForceButton(self, content):
        # TODO:
        return 0

    def ExportButtonCfg(self):
        # TODO:
        return 0

    def ImportButtonCfg(self):
        # TODO:
        return 0

    def GetButtonInfo(self, btn_idx):
        key_list = list(self.__btn_dic.keys())
        if (len(key_list) > btn_idx):
            return key_list[btn_idx]
        else:
            return None

#===test code===
#smart_btn = smart_buttton(btn_num = 3)
#smart_btn.UpdateButton("A3")
#smart_btn.Debug()
#smart_btn.UpdateButton("A3")
#smart_btn.Debug()
#smart_btn.UpdateButton("B2")
#smart_btn.Debug()
#smart_btn.UpdateButton("B2")
#smart_btn.Debug()
#smart_btn.UpdateButton("A3")
#smart_btn.Debug()
#smart_btn.UpdateButton("C2")
#smart_btn.Debug()
#smart_btn.UpdateButton("C2")
#smart_btn.Debug()
#smart_btn.UpdateButton("D3")
#smart_btn.Debug()
#smart_btn.UpdateButton("D3")
#smart_btn.Debug()
#smart_btn.UpdateButton("D3")
#smart_btn.Debug()
