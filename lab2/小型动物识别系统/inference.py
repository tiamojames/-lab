# 用于储存中间过程
data_process_list = []
# 用于存储过程对应的结果
data_result_list = []
# 存储用于查询的数据
list_data = []
# 用于存储输出结果
dict_input = {}

# # 规则库
# txt = '''
# 有奶，是哺乳动物
# 有毛发，是哺乳动物
# 有羽毛，是鸟
# 会飞，会下蛋，是鸟
# 是哺乳动物，有爪，有犬齿，眼盯前方，是食肉动物
# 是哺乳动物，吃肉，是食肉动物
# 是哺乳动物，有蹄，是有蹄动物
# 是有蹄动物，反刍食物，是偶蹄动物
# 是食肉动物，黄褐色，有黑色条纹，是老虎
# 是食肉动物，黄褐色，有黑色斑点，是金钱豹
# 是有蹄动物，长腿，长脖子，黄褐色，有暗斑点，是长颈鹿
# 是有蹄动物，白色，有黑色条纹，是斑马
# 是鸟，不会飞，长腿，长脖子，黑白色，是驼鸟
# 是鸟，不会飞，会游泳，黑白色，是企鹅
# 是鸟，善飞，不怕风浪，是海燕
# 有毛发，有奶，善跳跃，唇裂，是兔子
# 有毛发，有奶，善捕鼠，脚有肉垫，是猫
# 有毛发，有奶，鼻子上有角，褐色，皮糙肉厚，有蹄，是犀牛
# 有毛发，有奶，黑眼圈，四肢短小，是熊猫
# 有羽毛，卵生，上嘴鹰钩，能模仿人说话，是鹦鹉
# 有羽毛，卵生，腿短，嘴扁平，善潜水游泳，是鸭子
# 有羽毛，卵生，有爪，吃肉，上嘴鹰钩，是鹰
# 有羽毛，卵生，善游泳，嘴扁平，腿短，是鸭子
# 有羽毛，卵生，善潜水游泳，白色或黑色，颈长，嘴大，腿长，颈部有肉只凸起，是鹅
# 有羽毛，卵生，黑色，嘴大，是鸦
# 有羽毛，卵生，有爪，吃肉，上嘴鹰钩，是鹰
# 有羽毛，卵生，上嘴鹰钩，能模仿人说话，是鹦鹉
# 卵生，生活在水中，生活在陆地，有皮肤呼吸，用肺呼吸，皮肤光滑，吃昆虫，会变色，是青蛙
# 卵生，生活在水中，生活在陆地，有皮肤呼吸，用肺呼吸，吃昆虫，皮肤粗糙，四肢扁，背部黑色，是蝾螈
# 卵生，生活在水中，生活在陆地，有皮肤呼吸，用肺呼吸，吃昆虫，皮肤粗糙，是蟾蜍
# 用鳃呼吸，身体有鳍，生活在海洋中，身体扁平，两眼在头部同侧，是比目鱼
# 用鳃呼吸，身体有鳍，生活在淡水中，身体扁平，头高尾部窄，是鲫鱼
# 生活在陆地，用肺呼吸，胎生，身体有鳞或甲，身体圆而细长，吃小动物，是蛇
# 生活在陆地，用肺呼吸，胎生，身体有鳞或甲，有四肢，尾巴细长易断，吃昆虫，是壁虎
# 生活在陆地，用肺呼吸，胎生，身体有鳞或甲，身体圆而扁，有坚硬的壳，是乌龟
# 生活在陆地，用肺呼吸，胎生，身体有鳞或甲，壳为黄褐色，皮肤光滑，有黑斑，是玳瑁
# 生活在陆地，用肺呼吸，胎生，身体有鳞或甲，有四肢，善游泳，皮硬黑褐色，是鳄鱼
# '''
# # datas = txt.split('\n')
#
# with open('./rules.txt','r',encoding='utf-8') as f:
#     # 将数据预处理
#     datas = f.readlines()
#     datas = datas.split('\n')
# print(datas)
# for data in datas:
#     data = data.split('，')
#     data_process_list.append(data[:-1])
#     data_result_list.append(data[-1].replace('\n', ''))

# 使用文件路径
rules_file_path = './rules.txt'

with open(rules_file_path, 'r', encoding='utf-8') as f:
    # 读取并预处理数据
    datas = f.readlines()

# 以下是处理每一行数据的逻辑
data_process_list = []
data_result_list = []
for data in datas:
    data = data.strip()  # 移除每行末尾的换行符
    if data:  # 检查字符串是否为空
        rule_parts = data.split('，')
        data_process_list.append(rule_parts[:-1])
        data_result_list.append(rule_parts[-1])

# 清理 data_process_list 中的元素
cleaned_data_process_list = []
for item in data_process_list:
    # 去除空元素
    if item:
        # 去除每个特征字符串前后的空格
        # print(item)
        cleaned_item = [feature.strip() for feature in item]
        cleaned_item = [feature.lstrip('是') for feature in item]
        # print(cleaned_item)
        cleaned_data_process_list.append(cleaned_item)
data_process_list = cleaned_data_process_list
# print(data_process_list)
# 清理 data_result_list 中的元素
cleaned_data_result_list = [result.strip() for result in data_result_list if result]
data_result_list = cleaned_data_result_list
# print("data_process_list:",data_process_list)
# print("data_result_list",data_result_list)


# 最终结果列表
result_list = ['老虎', '金钱豹', '长颈鹿', '斑马', '驼鸟',
               '企鹅', '海燕',
               '兔子', '猫', '犀牛', '熊猫', '鹦鹉', '鸭子', '鹰', '鹅', '鸦', '青蛙', '蝾螈', '蟾蜍', '比目鱼',
               '鲫鱼', '蛇',
               '壁虎', '乌龟', '玳瑁', '鳄鱼']

# 数据库对应
database = {
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


def find_data(process_data_list, rules_applied=None):
    # 初始化已应用规则列表，如果未提供则设置为空列表
    if rules_applied is None:
        rules_applied = []

    # 初始化一个列表来存储过程中新发现的特征
    new_features = []
    # 初始化一个标记，用于指示是否找到了最终结果
    final_result_found = False

    # 遍历所有规则。data_process_list 包含规则的前提条件，data_result_list 包含对应的结论
    for epoch, data_process in enumerate(data_process_list):
        # 检查当前规则的所有前提条件是否都在已知特征列表中
        if all(feature in process_data_list for feature in data_process):
            # 从结果列表中获取当前规则的结果部分
            result = data_result_list[epoch].lstrip('是')

            # 构建表示当前规则的字符串
            applied_rule = '，'.join(data_process) + "，" + result

            # 如果该规则尚未被应用，将其添加到已应用规则列表中
            if applied_rule not in rules_applied:
                rules_applied.append(applied_rule)

            # 检查当前规则的结果是否是最终结果（在结果列表中）
            if result in result_list:
                # 如果是最终结果，设置标记并退出循环
                final_result_found = True
                break
            # 如果结果是一个新的特征，且尚未出现在已知特征列表中，将其添加到新特征列表中
            elif result not in process_data_list and result not in new_features:
                new_features.append(result)

    # 检查是否找到最终结果或发现新特征
    if final_result_found:
        # 如果找到最终结果，返回 1 和已应用的规则列表
        return 1, rules_applied
    elif new_features:
        # 如果发现新特征，将其添加到已知特征列表中，然后递归调用 find_data 函数
        for feature in new_features:
            process_data_list.append(feature)
        return find_data(process_data_list, rules_applied)

    # 如果既没有找到最终结果也没有发现新特征，返回 0 和已应用的规则列表
    return 0, rules_applied


def classify_animals(features):
    global data_process_list, data_result_list, result_list, dict_input
    dict_input = {}
    # 初始化规则应用记录字符串
    rules_text = '使用的规则和调用次序:\n'

    # 将特征转换为数据库中的相应条目
    # list_data = [database[feature] for feature in features if feature in database]

    # 调用 find_data 函数并记录规则应用信息
    end_result, rules_applied = find_data(features)

    # 将规则应用信息加入到规则文本
    for idx, rule in enumerate(rules_applied, 1):
        rules_text += f"{idx}. {rule}\n"

    # 准备最终结果文本
    result_text = ''
    if end_result == 1:
        # 如果找到最终结果，从 rules_applied 中获取最后一条规则作为结果
        final_rule = rules_applied[-1] if rules_applied else ''
        result_text = f'所识别的动物为 {final_rule.split("，")[-1]}'
    else:
        final_rule = rules_applied[-1] if rules_applied else ''
        # result_text = f'所识别的动物为 {final_rule.split("，")[-1]}'
        result_text = '无法识别具体动物'

    return rules_text, result_text





if __name__ == '__main__':
    # 用于储存中间过程
    data_process_list = []
    # 用于存储过程对应的结果
    data_result_list = []
    # 存储用于查询的数据
    list_data = []
    # 用于存储输出结果
    dict_input = {}
    # 将数据预处理
    datas = txt.split('\n')
    for data in datas:
        data = data.split('，')
        data_process_list.append(data[:-1])
        data_result_list.append(data[-1].replace('\n', ''))
    # 清理 data_process_list 中的元素
    cleaned_data_process_list = []
    for item in data_process_list:
        # 去除空元素
        if item:
            # 去除每个特征字符串前后的空格
            cleaned_item = [feature.strip() for feature in item]
            cleaned_item = [feature.lstrip('是') for feature in item]
            cleaned_data_process_list.append(cleaned_item)
    data_process_list = cleaned_data_process_list
    # 清理 data_result_list 中的元素
    cleaned_data_result_list = [result.strip() for result in data_result_list if result]
    data_result_list = cleaned_data_result_list
    # print("data_process_list:",data_process_list)
    # print("data_result_list",data_result_list)

    # 循环进行输入，直到碰见0后退出
    while 1:
        term = input("")
        if term == '0':
            break
        if database[term] not in list_data:
            list_data.append(database[term])
    # 打印前提条件
    print('前提条件为：')
    print(' '.join(list_data) + '\n')
    # 进行递归查找，直到找到最终结果,返回1则找到最终结果
    print(list_data)
    end_result,rules=find_data(list_data)
    if end_result == 1:
        print('推理过程如下：')
        # 将结果进行打印
        for i in dict_input.keys():
            print(f"{i}->{dict_input[i]}")
            # 得到最终结果即输出所识别动物
            if dict_input[i].lstrip("是") in result_list:
                print(f'所识别的动物为：{dict_input[i]}')
    else:
        # 将结果进行打印
        for i in dict_input.keys():
            print(f"推理过程：{i}->{dict_input[i]}")
    # list_data = ['黄褐色', '有黑色条纹', '食肉动物']
    # rules_text, result_text = classify_animals(list_data)
    # print("rules:",rules_text+'\n'+"result:",result_text)





# 通过传入的列表寻找结果
# def find_data(process_data_list):
#     # 依次进行循环查找并对过程排序
#     rules_applied = []  # 添加一个列表来记录应用的规则
#
#     for epoch, data_process in enumerate(data_process_list):
#         # 用于判断此过程是否成立
#         num = 0
#         for i in process_data_list:
#             if i in data_process:
#                 num += 1
#         # 过程成立则数值相同，可以进入下一步
#         if num == len(data_process):
#             # 此过程中结果是否为最终结果，不是将此过程结果加入到过程中
#             if data_result_list[epoch].lstrip('是') not in result_list:
#                 # print("data_result_list", data_result_list[epoch].lstrip('是'))
#                 # 弹出过程和此过程结果，因为此过程已经进行过，此结果存入需要查找的过程中
#                 result = data_result_list.pop(epoch)
#                 process = data_process_list.pop(epoch)
#                 # 判断结果是否已经存在过程中，存在则重新寻找，不存在则加入过程，并将其存入最终结果
#                 if result not in process_data_list:
#                     dict_input['，'.join(process)] = result
#                     rules_applied.append('，'.join(process))  # 记录应用的规则
#                     end_result,rules_applied = find_data(process_data_list + [result])
#                     if end_result == 1:
#                         return 1, rules_applied
#                     else:
#                         return 0, rules_applied
#                 # 存在则直接寻找
#                 else:
#                     end_result = find_data(process_data_list)
#                     if end_result == 1:
#                         return 1, rules_applied
#                     else:
#                         return 0, rules_applied
#             # 找到最终结果，取出结果后返回
#             else:
#                 process = data_process_list.pop(epoch)
#                 dict_input['，'.join(process)] = data_result_list[epoch]
#                 return 1, rules_applied
#     return 0, rules_applied  # 在没有找到结果的情况下返回

# def find_data(process_data_list, rules_applied=None):
#     if rules_applied is None:
#         rules_applied = []
#     print("当前处理的特征列表:", process_data_list)
#     new_features = []
#     final_result_found = False
#     for epoch, data_process in enumerate(data_process_list):
#         if all(feature in process_data_list for feature in data_process):
#             result = data_result_list[epoch].lstrip('是')
#
#             # 记录应用的规则
#             applied_rule = '，'.join(data_process) + "，" + result
#             if applied_rule not in rules_applied:
#                 rules_applied.append(applied_rule)
#
#             # 如果是最终结果
#             if result in result_list:
#                 final_result_found = True
#                 break
#                 # return 1, rules_applied
#             # 如果不是最终结果，继续递归查找
#             elif result not in process_data_list and result not in new_features:
#                 new_features.append(result)
#                 # process_data_list.append(result)
#                 # return find_data(process_data_list, rules_applied)
#         #如果找到最终结果或者有新特征时进一步处理时
#         if final_result_found:
#             return 1,applied_rule
#         elif new_features:
#             for feature in new_features:
#                 process_data_list.append(feature)
#                 return find_data(process_data_list,rules_applied)
#     return 0, rules_applied  # 在没有找到结果的情况下返回



# def classify_animals(features):
#     global data_process_list, data_result_list, result_list, dict_input
#     dict_input = {}
#     # 初始化规则应用记录字符串
#     rules_text = '使用的规则和调用次序:\n'
#     print("传入的特征:", features)
#     # 将特征转换为数据库中的相应条目
#     list_data = [database[feature] for feature in features if feature in database]
#     # print(list_data)
#     # 调用 find_data 函数并记录规则应用信息
#     end_result, rules_applied = find_data(list_data)
#     # print(end_result,rules_applied)
#     # 将规则应用信息加入到规则文本
#     # for idx, rule in enumerate(rules_applied, 1):
#     #     rules_text += f"{idx}. {rule}\n"
#     for i in rules_applied:
#         rules_text += i
#     # 准备最终结果文本
#     # rules_text = '推理过程如下：\n'
#     result_text=''
#     if end_result == 1:
#         for i in dict_input.keys():
#             rules_text += f"{i} -> {dict_input[i]}\n"
#             if dict_input[i].lstrip("是") in result_list:
#                 rules_text += f'所识别的动物为 {dict_input[i]}'
#                 result_text = f'所识别的动物为 {dict_input[i]}'
#     else:
#         for i in dict_input.keys():
#             rules_text += f"{i} -> {dict_input[i]}\n"
#             if dict_input[i].lstrip("是") in result_list:
#                 rules_text += f'所识别的动物为 {dict_input[i]}'
#                 result_text = f'所识别的动物为 {dict_input[i]}'
#         # rules_text += '无法识别具体动物'
#     print("rules:",rules_text+'\n'+"result:",result_text)
#     return rules_text, result_text