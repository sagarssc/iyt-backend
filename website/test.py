from collections import defaultdict

def list_files(input_str):
    dependencies = defaultdict(list)
    func_map = defaultdict()
    processed = set()

    lines = input_str.split('\n')
    for line in lines:
        parts = line.strip().split(': ')
        if len(parts) != 2:
            continue
        filename, dependencies_list = parts
        dependencies_list = dependencies_list.split('; ')
        for dependency in dependencies_list:
            if dependency[:2] == "pr":
              func_name = dependency.split("(")[1].split(")")[0]
              func_map["rq("+func_name+")"] = filename
            else:
              dependencies[filename].append(dependency.replace(";",""))

    result = []
    print("dependencies  " ,dependencies)
    print("dependencies_list ",dependencies_list)
    print("func_map ", func_map)
    def dfs(file):
        if file in processed:
            return
        processed.add(file)
        for dep in dependencies[file]:
            dfs(func_map[dep])
        print("addding  ", file)
        result.append(file)

    for file in list(dependencies.keys()):
        dfs(file)

    return result

input_str = '''a.js: pr("A"); rq("B"); rq("C");
b.js: pr("B"); rq("D"); rq("F");
c.js: pr("C"); rq("E");
d.js: pr("D");
f.js: pr("F");
e.js: pr("E");'''


file_order = list_files(input_str)
print(file_order)
