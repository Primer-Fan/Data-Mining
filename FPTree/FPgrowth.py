def load_data_set():
    data_set = [['bread', 'milk', 'vegetable', 'fruit', 'eggs'],
                ['noodle', 'beef', 'pork', 'water', 'socks', 'gloves', 'shoes', 'rice'],
                ['socks', 'gloves'],
                ['bread', 'milk', 'shoes', 'socks', 'eggs'],
                ['socks', 'shoes', 'sweater', 'cap', 'milk', 'vegetable', 'gloves'],
                ['eggs', 'bread', 'milk', 'fish', 'crab', 'shrimp', 'rice']]
    return data_set


def load_data_set1():
    data_set = [['r', 'z', 'h', 'j', 'p'],
                ['z', 'y', 'x', 'w', 'v', 'u', 't', 's'],
                ['z'],
                ['r', 'x', 'n', 'o', 's'],
                ['y', 'r', 'x', 'z', 'q', 't', 'p'],
                ['y', 'z', 'x', 'e', 'q', 's', 't', 'm']]
    return data_set


def transform_to_frozen_data_set(data_set):
    frozen_data_set = {}
    for items in data_set:
        frozen_items = frozenset(items)
        if frozen_items in frozen_data_set:
            frozen_data_set[frozen_items] += 1
        else:
            frozen_data_set[frozen_items] = 1
    return frozen_data_set


class TreeNode:
    def __init__(self, node_name, count, parent_node):
        self.node_name = node_name
        self.count = count
        self.parent_node = parent_node
        self.next_similar_node = None
        self.children = {}

    def increase_count(self, count):
        """
        计数加一

        :param count: 增量
        :return: None
        """
        self.count += count

    def display(self, indentation=0):
        """
        递归输出节点, 供测试fp树使用

        :param indentation: 缩进控制量
        :return: None
        """
        print('   ' * indentation, self.node_name, ' ', self.count)
        for child in self.children.values():
            child.display(indentation + 1)


def create_tree(frozen_data_set, min_support=1):
    """
    根据支持度和数据集创建相应的fp增长树

    :param frozen_data_set: 经过frozen处理过的要进行建树的数据集
    :param min_support: 最小支持度对应的出现次数
    :return: fp树, 头部节点链表
    """
    # 第一遍扫描数据集, 找出满足最小支持度的项集
    head_node_table = {}
    for items in frozen_data_set:
        for item in items:
            head_node_table[item] = head_node_table.get(item, 0) + frozen_data_set[items]
    head_node_table = {key: value for key, value in head_node_table.items() if value >= min_support}
    frequent_items = set(head_node_table.keys())

    # 如果没有频繁项, 返回空树与空头部节点链表
    if len(frequent_items) == 0:
        return None, None

    # 格式化头部节点链表 {'name': [count, next_similar_node]}
    for key in head_node_table:
        head_node_table[key] = [head_node_table[key], None]
    fp_tree = TreeNode('null', 1, None)

    # 第二遍扫描数据集, 建树
    for items, count in frozen_data_set.items():
        frequent_items_record = {}
        for item in items:
            if item in frequent_items:
                frequent_items_record[item] = head_node_table[item][0]
        if len(frequent_items_record) > 0:
            ordered_frequent_items = [v[0] for v in sorted(frequent_items_record.items(), key=lambda v: v[1],
                                                           reverse=True)]
            update_fp_tree(fp_tree, ordered_frequent_items, head_node_table, count)
    return fp_tree, head_node_table


def update_fp_tree(fp_tree, ordered_frequent_items, head_node_table, count):
    """
    用排序好的频繁项集更新fp树与头部节点链表

    :param fp_tree: 当前fp(子)树根节点
    :param ordered_frequent_items: 排序好的频繁项集
    :param head_node_table: 头结点链表
    :param count: 当前频繁项集对应的items的数量
    :return: None
    """
    # 处理当前频繁项集首项
    if ordered_frequent_items[0] in fp_tree.children:
        fp_tree.children[ordered_frequent_items[0]].increase_count(count)
    else:
        fp_tree.children[ordered_frequent_items[0]] = TreeNode(ordered_frequent_items[0], count, fp_tree)

        # 更新头部节点链表
        if head_node_table[ordered_frequent_items[0]][1] is None:
            head_node_table[ordered_frequent_items[0]][1] = fp_tree.children[ordered_frequent_items[0]]
        else:
            update_head_node_table(head_node_table[ordered_frequent_items[0]][1],
                                   fp_tree.children[ordered_frequent_items[0]])
    # 递归处理频繁项集其他项
    if len(ordered_frequent_items) > 1:
        update_fp_tree(fp_tree.children[ordered_frequent_items[0]], ordered_frequent_items[1:], head_node_table, count)


def update_head_node_table(head_node_table_begin_node, target_node):
    """
    将新节点加入头部节点链表尾端

    :param head_node_table_begin_node: 当前项对应的链表的头结点
    :param target_node: 要加入表的节点
    :return: None
    """
    while head_node_table_begin_node.next_similar_node is not None:
        head_node_table_begin_node = head_node_table_begin_node.next_similar_node
    head_node_table_begin_node.next_similar_node = target_node


def mine_fp_tree(head_node_table, prefix, frequent_patterns, min_support):
    """
    挖掘fp树上的频繁项集极其支持度

    :param head_node_table: 头部节点表
    :param prefix: 前缀频繁项集
    :param frequent_patterns: 频繁项集 {frozen({'item', ...}): support}
    :param min_support: 最小支持数
    :return: None
    """
    head_node_items = [v[0] for v in sorted(head_node_table.items(), key=lambda v: v[1][0])]
    if len(head_node_items) == 0:
        return

    for head_node_item in head_node_items:
        new_prifix = prefix.copy()
        new_prifix.add(head_node_item)
        support = head_node_table[head_node_item][0]
        frequent_patterns[frozenset(new_prifix)] = support

        prefix_path = get_prefix_path(head_node_table, head_node_item)
        if prefix_path != {}:
            conditional_fp_tree, conditional_head_node_table = create_tree(prefix_path, min_support)
            if conditional_head_node_table is not None:
                mine_fp_tree(conditional_head_node_table, new_prifix, frequent_patterns, min_support)


def get_prefix_path(head_node_table, head_node_item):
    """
    获取当前头结点链表上的所有节点的前缀路径

    :param head_node_table: 头部节点表
    :param head_node_item: 头部节点项
    :return: 当前头结点链表上的所有节点的前缀路径
    """
    prefix_path = {}
    begin_node = head_node_table[head_node_item][1]
    prefixs = ascend_tree(begin_node)
    if prefixs:
        prefix_path[frozenset(prefixs)] = begin_node.count
    while begin_node.next_similar_node is not None:
        begin_node = begin_node.next_similar_node
        prefixs = ascend_tree(begin_node)
        if prefixs:
            prefix_path[frozenset(prefixs)] = begin_node.count
    return prefix_path


def ascend_tree(tree_node):
    """
    返回当前节点对应的前缀路径

    :param tree_node:
    :return:当前节点对应的前缀路径
    """
    prefixs = []
    while (tree_node.parent_node is not None) and (tree_node.parent_node.node_name != 'null'):
        tree_node = tree_node.parent_node
        prefixs.append(tree_node.node_name)
    return prefixs


def generate_rules(frequent_patterns, min_confidence, rules):
    """
    产生关联规则

    :param frequent_patterns: 包含支持度的频繁项集
    :param min_confidence: 最小置信度
    :param rules: 规则表
    :return: None
    """
    for frequent_set in frequent_patterns:
        if len(frequent_set) > 1:
            get_rules(frequent_set, frequent_set, rules, frequent_patterns, min_confidence)


def get_rules(frequent_set, current_set, rules, frequent_patterns, min_confidence):
    """
    获取当前频繁项集下的关联规则

    :param frequent_set: 当前频繁项集
    :param current_set: 当前可以拆分形成左项的频繁项集
    :param rules: 规则表
    :param frequent_patterns: 包含支持度的频繁项集
    :param min_confidence: 最小置信度
    :return: None
    """
    for frequent_element in current_set:
        # 取得左项集
        subset = remove_item(current_set, frequent_element)
        confidence = frequent_patterns[frequent_set] / frequent_patterns[subset]
        if confidence >= min_confidence:
            is_insert = False
            for rule in rules:
                if rule[0] == subset and rule[1] == frequent_set - subset:
                    is_insert = True
            if not is_insert:
                rules.append((subset, frequent_set - subset, confidence))
            # 递归找出所有的合法左项集
            if len(subset) > 1:
                get_rules(frequent_set, subset, rules, frequent_patterns, min_confidence)


def remove_item(set, item):
    """
    获取去除item项后的set集frozen副本

    :param set: 原频繁项集
    :param item: 待删除项
    :return: 去除item项后的set的frozen集
    """
    temporary_set = []
    for element in set:
        if element != item:
            temporary_set.append(element)
    temporary_frozen_set = frozenset(temporary_set)
    return temporary_frozen_set


if __name__ == '__main__':
    data_set = load_data_set1()
    frozen_data_set = transform_to_frozen_data_set(data_set)
    min_support = 3
    fp_tree, head_node_table = create_tree(frozen_data_set, min_support)
    fp_tree.display()
    frequent_patterns = {}
    print("frequent_patterns:", frequent_patterns)
    prefix = set([])
    mine_fp_tree(head_node_table, prefix, frequent_patterns, min_support)
    min_confidence = 0.6
    rules = []
    generate_rules(frequent_patterns, min_confidence, rules)
    print("rules", rules)
