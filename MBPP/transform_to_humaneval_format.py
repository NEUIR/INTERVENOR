# transform the mbpp dataformat to humaneval dataformat
import json
import re

# 寻找函数名
def find_function_name(code):
    lines = code.split('\n')
    for line in lines:
        if line.strip().startswith("def "):
            return line.split()[1].split('(')[0]
    return None

# 寻找函数签名
def find_function_signature(code):
    lines = code.split('\n')
    for line in lines:
        if line.strip().startswith("def "):
            return line.strip()
    return None

# 寻找函数签名及其前面的代码
def find_function_and_code(code):
    lines = code.split('\n')
    for i, line in enumerate(lines):
        if line.strip().startswith("def "):
            return '\n'.join(lines[:i])+ '\n'
    return None, None


def get_test(test_list,function_name):
    test = f"def check({function_name}):\n"
    for i in range(len(test_list)):
        test += "    " + test_list[i] + "\n"
    return test

def main():
    # 读取jsonl文件到列表
    mbpp_data = []
    with open("./data/mbpp.jsonl", "r") as fp:
        for line in fp:
            if any(not x.isspace() for x in line):
                mbpp_data.append(json.loads(line))

    mbpp_humaneval_format = []

    for i in range(len(mbpp_data)):
        line = {}
        line["task_id"] = "MBPP/{0}".format(mbpp_data[i]["task_id"])
        function_name = find_function_name(mbpp_data[i]["code"])
        function_signature = find_function_signature(mbpp_data[i]["code"])
        code_before_function = find_function_and_code(mbpp_data[i]["code"])
        prompt = "# {}".format(mbpp_data[i]["text"]) + "\n" + code_before_function + function_signature
        line["prompt"] = prompt
        line["entry_point"] = function_name
        line["canonical_solution"] = mbpp_data[i]["code"]
        test_list = mbpp_data[i]["test_list"]
        line["test"] = get_test(test_list,function_name)
        mbpp_humaneval_format.append(line)


    # 输出到jsonl文件
    with open("./data/mbpp_humaneval_format.jsonl", "w") as fp:
        for line in mbpp_humaneval_format:
            fp.write(json.dumps(line) + '\n')

    print("done")




if __name__ == '__main__':

    main()
