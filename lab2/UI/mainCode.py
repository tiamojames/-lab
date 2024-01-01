import sys
from PyQt5 import QtWidgets
import UI.MainDis, UI.False_Lable, UI.EmptyUI
import Animal.RuleBase as RB
import Animal.Inference_Engine as IE
import Animal.Inference_Engine as Inference

Save_rules_after = set()
Save_concludes = set()
def ListInSet(li, se):
    for i in li:
        if i not in se:
            return False
    return True

def judge_rule_in(lst):
    for rule_pre in lst:
        if rule_pre in Save_rules_after:
            continue
        else:
            return False
    return True

class Lable_ui(QtWidgets.QMainWindow,UI.False_Lable.Ui_Dialog):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)  # 创建主界面对象
        UI.False_Lable.Ui_Dialog.__init__(self)  # 主界面对象初始化
        self.setupUi(self)  # 配置主界面对象

class Empty_ui(QtWidgets.QMainWindow,UI.EmptyUI.Ui_Dialog):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)  # 创建主界面对象
        UI.False_Lable.Ui_Dialog.__init__(self)  # 主界面对象初始化
        self.setupUi(self)  # 配置主界面对象


class MAIN_ui(QtWidgets.QMainWindow,UI.MainDis.Ui_dialog,UI.False_Lable.Ui_Dialog):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)  # 创建主界面对象
        UI.MainDis.Ui_dialog.__init__(self)  # 主界面对象初始化
        self.setupUi(self)  # 配置主界面对象
        self.rulePushButton.clicked.connect(self.add_rule)#添加规则
        self.inferencePushButton.clicked.connect(self.inference)
        self.Lable = Lable_ui()
        self.Empty = Empty_ui()
        self.display_pre()

    def display_pre(self):
        RB.ini_rules()
        self.ruleTextBrowser.clear()
        i = 0
        RB.rules_pre = list(RB.Rules_pre).sort()
        for line in RB.Rules_pre:#将规则库放入显示框
            if i < 10 :
                str_temp = str(i) + '. '+ line
            else:
                str_temp = str(i) + '.'+ line
            self.ruleTextBrowser.append(str_temp)
            i += 1

    def add_rule(self):
        #添加新规则
        new_rule = self.inputLineEdit.toPlainText()
        self.inputLineEdit.clear()

        if new_rule == '' or new_rule == '\n':
            self.Empty.show()
            self.Empty.pushButton.clicked.connect(self.Empty.close)
            return
        new_rule = new_rule.split('\n')
        if new_rule[0] == '' or new_rule[1] == '' or new_rule[0].isspace()  or new_rule[1].isspace() :
            self.Empty.show()
            self.Empty.pushButton.clicked.connect(self.Empty.close)
            return

        new_pre = new_rule[0]
        new_pre = new_pre.split(' ')
        new_conclusion = new_rule[1]
        new_pre = [i for i in new_pre if (len(str(i)) != 0)]
        new_pre = ' '.join(new_pre)
        print(type(new_pre))
        print(new_pre)
        print(new_conclusion)
        judge_bool = False
        for i in RB.Rules.keys():
            if judge_is(i, new_pre):
                judge_bool = True
                break
        # print(judge_bool)
        if judge_bool:
            self.Lable.show()
            self.Lable.pushButton.clicked.connect(self.Lable.close)
        else:
            file = open('../UI/Rules.txt', 'a', encoding='UTF-8')
            RB.Rules[new_pre] = new_conclusion
            file.write('\n')
            file.write(new_pre)
            file.write('\n')
            file.write(new_conclusion)
            file.close()
            self.display_pre()



    def inference(self):
        #推理
        # self.outputTextBrowser.append("1")
        ini()
        self.outputTextBrowser.clear()
        self.answerTextBrowser.clear()
        rule_pre_num = self.inputFactTextEdit.toPlainText() #获取输入的事实
        rule_pre_num = rule_pre_num.split('\n')

        #删除空格元素
        rule_pre_num = list(set(rule_pre_num))
        for space in rule_pre_num:
            if space == '':
                rule_pre_num.remove('')

        rules = list(RB.Rules_pre)
        for i in rule_pre_num:
            if i.isdigit():
                if 0 <= int(i) < len(rules):
                    Save_rules_after.add(rules[int(i)])
                    # self.outputTextBrowser.append(rules[int(i)])
                else:
                    self.outputTextBrowser.clear()
                    self.outputTextBrowser.append('该前提不存在，请重新输入')
                    return
            else:
                self.outputTextBrowser.clear()
                self.outputTextBrowser.append('输入中存在非法字符，请重新输入')
                return
        i = 1
        for rule in RB.Rules:
            rule_list = rule.split(' ')
            if i == 1:
                rule_ini = rule
            if judge_rule_in(rule_list):
                Save_rules_after.add(RB.Rules[rule])
                temp = rule + '->'  +RB.Rules[rule]
                self.outputTextBrowser.append(temp)
                Save_concludes.add(RB.Rules[rule])
                rule = rule_ini

            i = i + 1
        if Save_concludes:
            for conclude in Save_concludes:
                self.answerTextBrowser.append(conclude)
        else:
            self.answerTextBrowser.append('根据已知事实无法得出结论')


def ini():
    Save_rules_after.clear()
    Save_concludes.clear()

def judge_is(rule1, rule2):
    rule1 = rule1.split(' ')
    rule2 = rule2.split(' ')
    rule1.sort()
    rule2.sort()
    if rule2 == rule1:
        return True
    else:
        return False

app = QtWidgets.QApplication(sys.argv)  # 新建窗体
MAIN_window = MAIN_ui()  # 创建主菜单的窗口对象
MAIN_window.show()  # 显示主菜单
sys.exit(app.exec_())  # 保持显示
