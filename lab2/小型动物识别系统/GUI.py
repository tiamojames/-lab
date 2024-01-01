# -*- coding: utf-8 -*-

# 导入必要的模块
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import inference

# UI主类
class Ui_Form(object):
    def __init__(self):
        self.feature_attributes = {
            '1': '有奶', '2': '有毛发', '3': '有羽毛', '4': '会飞', '5': '会下蛋',
            '6': '吃肉', '7': '有爪', '8': '有犬齿', '9': '眼盯前方', '10': '有蹄',
            '11': '反刍食物', '12': '黄褐色', '13': '有黑色条纹', '14': '有黑色斑点',
            '15': '长腿', '16': '长脖子', '17': '不会飞', '18': '会游泳', '19': '黑白色',
            '20': '善飞', '21': '不怕风浪', '22': '善跳跃', '23': '唇裂', '24': '善捕鼠',
            '25': '脚有肉垫', '26': '鼻子上有角', '27': '皮糙肉厚', '28': '黑眼圈',
            '29': '四肢短小', '30': '上嘴鹰钩', '31': '能模仿人说话', '32': '腿短',
            '33': '嘴扁平', '34': '颈长', '35': '嘴大', '36': '颈部有肉只凸起',
            '37': '卵生', '38': '生活在水中', '39': '生活在陆地', '40': '有皮肤呼吸',
            '41': '用肺呼吸', '42': '皮肤光滑', '43': '皮肤粗糙', '44': '会变色',
            '45': '四肢扁', '46': '背部黑色', '47': '用鳃呼吸', '48': '身体有鳍',
            '49': '生活在海洋中', '50': '身体扁平', '51': '两眼在头部同侧',
            '52': '生活在淡水中', '53': '头高尾部窄', '54': '胎生', '55': '身体有鳞或甲',
            '56': '身体圆而细长', '57': '吃小动物', '58': '尾巴细长易断', '59': '身体圆而扁',
            '60': '有坚硬的壳', '61': '壳为黄褐色', '62': '有黑斑', '63': '善游泳',
            '64': '皮硬黑褐色', '65': '哺乳动物', '66': '鸟', '67': '食肉动物', '68': '有蹄动物',
            '69': '偶蹄动物'
        }

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(700, 800)  # 调整窗体尺寸

        # 创建滚动区域以适应大量复选框
        self.scrollArea = QtWidgets.QScrollArea(Form)
        self.scrollArea.setGeometry(QtCore.QRect(10, 10, 480, 450))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")

        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 480, 450))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")

        #增删改查
        self.ruleInput = QtWidgets.QLineEdit(Form)
        self.ruleInput.setGeometry(QtCore.QRect(10, 500, 300, 30))  # 更改位置和大小
        self.ruleInput.setPlaceholderText("输入新规则，例如：有奶，是哺乳动物")

        self.addRuleButton = QtWidgets.QPushButton("添加规则", Form)
        self.addRuleButton.setGeometry(QtCore.QRect(320, 500, 90, 30))  # 更改位置和大小

        self.deleteRuleButton = QtWidgets.QPushButton("删除规则", Form)
        self.deleteRuleButton.setGeometry(QtCore.QRect(420, 500, 90, 30))  # 更改位置和大小

        self.modifyRuleButton = QtWidgets.QPushButton("修改规则", Form)
        self.modifyRuleButton.setGeometry(QtCore.QRect(520, 500, 90, 30))  # 设置位置和大小

        # # 绑定按钮事件
        self.modifyRuleButton.clicked.connect(self.modify_rule)
        self.addRuleButton.clicked.connect(self.add_rule)
        self.deleteRuleButton.clicked.connect(self.delete_rule)


        self.verticalLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setObjectName("verticalLayout")

        self.createCheckBoxes()

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        # 创建按钮
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(10, 470, 100, 30))
        self.pushButton.setObjectName("pushButton")

        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(600, 470, 100, 30))
        self.pushButton_2.setObjectName("pushButton_2")


        # 创建用于显示规则应用和调用次序的文本区域
        self.rulesTextBrowser = QtWidgets.QTextBrowser(Form)
        self.rulesTextBrowser.setGeometry(QtCore.QRect(500, 10, 190, 450))
        self.rulesTextBrowser.setObjectName("rulesTextBrowser")

        # 创建用于显示最终结果的文本区域
        self.resultTextBrowser = QtWidgets.QTextBrowser(Form)
        self.resultTextBrowser.setGeometry(QtCore.QRect(10, 550, 680, 140))
        self.resultTextBrowser.setObjectName("resultTextBrowser")

        self.pushButton.setText("识别动物")
        self.pushButton.clicked.connect(self.buttonClick)

        self.pushButton_2.setText("退出系统")
        self.pushButton_2.clicked.connect(self.buttonClick2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

        # 在 setupUi 方法中添加重置按钮
        self.resetButton = QtWidgets.QPushButton(Form)
        self.resetButton.setGeometry(QtCore.QRect(120, 470, 100, 30))
        self.resetButton.setObjectName("resetButton")
        self.resetButton.setText("重置")
        self.resetButton.clicked.connect(self.resetButtonClick)


    def createCheckBoxes(self):
        # 读取规则文件
        with open('rules.txt', 'r', encoding='utf-8') as file:
            rules = file.readlines()

        # 解析规则以获取特征，并保持它们的顺序
        features = []
        for rule in rules:
            parts = rule.strip().split('，')
            if parts[-1].startswith('是'):
                for part in parts[:-1]:
                    if part not in features:
                        features.append(part)

        # 创建复选框
        for i, feature in enumerate((features)):
            checkBox = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
            checkBox.setObjectName(f"checkBox_{i + 1}")
            checkBox.setText(f"特征 {i + 1}: {feature}")  # 显示特征的描述
            self.verticalLayout.addWidget(checkBox)

        # 创建复选框
    # def createCheckBoxes(self):
    #     # 假设有 69 个特征
    #     # 数据库对应
    #     for i in range(69):  # 假设有 69 个特征
    #         checkBox = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
    #         feature_number = str(i + 1)
    #         feature_text = self.feature_attributes.get(feature_number, f"特征 {feature_number}")
    #         checkBox.setObjectName(f"checkBox_{feature_number}")
    #         checkBox.setText(f"特征 {i + 1}:{feature_text}")  # 显示特征的描述
    #         self.verticalLayout.addWidget(checkBox)

    # def buttonClick(self):
    #     try:
    #         # self.feature_attributes
    #         # checkboxState = [self.feature_attributes[str(i + 1)] for i in range(69) if
    #         #                  self.findChild(QtWidgets.QCheckBox, f"checkBox_{i + 1}").isChecked()]
    #         inference.dict_input = {}
    #         checkboxState = [self.feature_attributes[str(i + 1)] for i in range(69) if
    #                          self.findChild(QtWidgets.QCheckBox, f"checkBox_{i + 1}").isChecked()]
    #         print(checkboxState)
    #         rules, result_text = inference.classify_animals(checkboxState)
    #         self.rulesTextBrowser.setText(rules)
    #         self.resultTextBrowser.setText(result_text)
    #         # 点击处理后重置所有复选框
    #         for i in range(69):
    #             checkBox = self.findChild(QtWidgets.QCheckBox, f"checkBox_{i + 1}")
    #             if checkBox:
    #                 checkBox.setChecked(False)
    #     except Exception as e:
    #         print(f"发生错误：{e}")
    #         self.resultTextBrowser.setText(f"发生错误：{e}")
    def buttonClick(self):
        try:
            # 获取选中的复选框对应的特征
            checkboxState = []
            for i in range(self.verticalLayout.count()):
                checkBox = self.verticalLayout.itemAt(i).widget()
                if checkBox.isChecked():
                    # 从复选框文本中提取特征
                    feature = checkBox.text().split(': ')[1]
                    checkboxState.append(feature)

            print(checkboxState)
            rules, result_text = inference.classify_animals(checkboxState)
            self.rulesTextBrowser.setText(rules)
            self.resultTextBrowser.setText(result_text)

            # 点击处理后重置所有复选框
            for i in range(self.verticalLayout.count()):
                checkBox = self.verticalLayout.itemAt(i).widget()
                if checkBox:
                    checkBox.setChecked(False)

        except Exception as e:
            print(f"发生错误：{e}")
            self.resultTextBrowser.setText(f"发生错误：{e}")

    # 创建重置按钮的点击事件处理函数
    def resetButtonClick(self):
        for i in range(69):
            checkBox = self.findChild(QtWidgets.QCheckBox, f"checkBox_{i + 1}")
            if checkBox:
                checkBox.setChecked(False)
        # 清空文本区域
        self.rulesTextBrowser.setText('')
        self.resultTextBrowser.setText('')
    def buttonClick2(self):
        sys.exit(app.exec_())

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "动物识别系统"))

    def updateInferenceData(self):
        # 清空现有的数据结构
        inference.data_process_list = []
        inference.data_result_list = []
        inference.result_list = []

        # 重新从 rules.txt 读取并解析规则
        with open('rules.txt', 'r', encoding='utf-8') as file:
            rules = file.readlines()

        for rule in rules:
            parts = rule.strip().split('，')
            if parts[-1].startswith('是'):
                inference.data_process_list.append(parts[:-1])
                inference.data_result_list.append(parts[-1].lstrip('是'))
                if parts[-1].lstrip('是') not in inference.result_list:
                    inference.result_list.append(parts[-1].lstrip('是'))

    def loadRulesAndUpdateCheckboxes(self):
        # 清除旧的复选框
        for i in reversed(range(self.verticalLayout.count())):
            self.verticalLayout.itemAt(i).widget().setParent(None)

        # 从 rules.txt 读取并解析规则
        with open('rules.txt', 'r', encoding='utf-8') as file:
            rules = file.readlines()

        # 解析规则以获取特征，并保持它们的顺序
        features = []
        for rule in rules:
            parts = rule.strip().split('，')
            if parts[-1].startswith('是'):
                for part in parts[:-1]:
                    if part not in features:
                        features.append(part)
        self.updateInferenceData()

        # 根据新的特征集创建复选框，保持原始顺序
        for i, feature in enumerate(features):
            checkBox = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
            checkBox.setObjectName(f"checkBox_{i + 1}")
            checkBox.setText(f"特征 {i + 1}: {feature}")
            self.verticalLayout.addWidget(checkBox)

    def add_rule(self):
        rule = self.ruleInput.text()
        # rule = self.ruleInput.text()
        with open('rules.txt', 'a', encoding='utf-8') as file:
            file.write(rule + '\n')  # 将新规则追加到文件末尾\
        self.ruleInput.clear()  # 清空文本框
        self.loadRulesAndUpdateCheckboxes()


    def delete_rule(self):
        rule = self.ruleInput.text()
        with open('rules.txt', 'r', encoding='utf-8') as file:
            lines = file.readlines()
        with open('rules.txt', 'w', encoding='utf-8') as file:
            for line in lines:
                if line.strip() != rule:
                    file.write(line)  # 只写回非删除规则
        self.ruleInput.clear()  # 清空文本框
        self.loadRulesAndUpdateCheckboxes()

    def modify_rule(self):
        rule_change = self.ruleInput.text()  # 获取输入框中的规则更改
        if '->' in rule_change:
            old_rule, new_rule = rule_change.split('->')
            old_rule = old_rule.strip()
            new_rule = new_rule.strip()

            # 从 rules.txt 中删除旧规则
            with open('rules.txt', 'r', encoding='utf-8') as file:
                lines = file.readlines()
            with open('rules.txt', 'w', encoding='utf-8') as file:
                for line in lines:
                    if line.strip() != old_rule:
                        file.write(line)

            # 添加新规则到 rules.txt
            with open('rules.txt', 'a', encoding='utf-8') as file:
                file.write(new_rule + '\n')

            # 清空文本框并更新界面
            self.ruleInput.clear()
            self.loadRulesAndUpdateCheckboxes()
            self.updateInferenceData()
        else:
            print("请以 '旧规则 -> 新规则' 的格式输入规则更改")
    # def modify_rule(self):
    #     old_rule = self.ruleInput.text()  # 获取旧规则
    #     new_rule = self.modifyRuleInput.text()  # 获取新规则
    #
    #     # 从 rules.txt 中删除旧规则
    #     with open('rules.txt', 'r', encoding='utf-8') as file:
    #         lines = file.readlines()
    #     with open('rules.txt', 'w', encoding='utf-8') as file:
    #         for line in lines:
    #             if line.strip() != old_rule:
    #                 file.write(line)
    #
    #     # 添加新规则到 rules.txt
    #     with open('rules.txt', 'a', encoding='utf-8') as file:
    #         file.write(new_rule + '\n')
    #
    #     # 清空文本框并更新界面
    #     self.ruleInput.clear()
    #     self.modifyRuleInput.clear()
    #     self.loadRulesAndUpdateCheckboxes()
    #     self.updateInferenceData()


# 应用类
class AnimalRecognitionApp(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        Ui_Form.__init__(self)
        self.setupUi(self)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = AnimalRecognitionApp()
    mainWindow.show()
    sys.exit(app.exec_())
