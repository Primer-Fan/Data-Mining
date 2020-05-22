def load_data_set():
    data_set = [['打喷嚏', '护士', '感冒'],
                ['打喷嚏', '农民', '过敏'],
                ['头痛', '建筑工人', '脑震荡'],
                ['头痛', '建筑工人', '感冒'],
                ['打喷嚏', '教师', '感冒'],
                ['头痛', '教师', '脑震荡']]
    return data_set


def bayes(data_set, features: list):
    diseases = list(set([items[2] for items in data_set]))
    result, rate = None, 0.0
    PA = 1.0
    for feature in features:
        PA = PA * len([i for i in data_set if feature in i]) / len(data_set)
    if PA == 0.0:
        return None
    for disease in diseases:
        PC = len([i for i in data_set if i[2] == disease]) / len(data_set)
        PAC = 1.0
        for feature in features:
            PAC = PAC * len([i for i in data_set if feature in i and i[2] == disease]) / len([i for i in data_set if i[2] == disease])
        P = PAC * PC / PA
        if P > rate:
            result = disease
            rate = P
    return result, rate

if __name__ == '__main__':
    data_set = load_data_set()
    features = input('Please enter the patient\'s symptoms:').split(' ')
    result, rate = bayes(data_set, features)
    print(result, rate)