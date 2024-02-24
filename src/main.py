import os, sys, requests

global code

if len(sys.argv) == 2:
    code = open(str(sys.argv[1]))
    code = code.readlines()
elif len(sys.argv) == 3:
    if sys.argv[2] == "--http":
        code = requests.get(sys.argv[1]).text
else:
    print("Error:\tFile not specified")
    os._exit(1)

venv = {}
vfn = []

for line in code:
    if " = " in line:
        var = line.split(" = ")[0]
        val = line.split(" = ")[1].split("\n")[0]

        venv[var] = val
    if "fn " in line:
        name = line.split("fn ")[1]
        name = name.split(" {")[0]

        params = name.split("(")[1]
        params = params.split(")")[0]
        if ", " in params:
            params.split(", ")

        name = name.split("(")[0]

        cmd = []

        for line in code[code.index(line) + 1:]:
            if "}" in line:
                res = line.split("}")[0]
                break
            res = line

            cmd.append(res)

        res = {
            "name": name,
            "parameters": params,
            "commands": cmd
        }

        vfn.append(res)

def run(name, params):
    for fn in vfn:
        if fn["name"] == name:
            for i in params:
                eval(
                    "{} = {}".format(
    fn["parameters"][params.index(i)], i
                    )
                )
            for cmd in fn["commands"]:
                if cmd == "\n": pass
                elif ", " in cmd:
                    eval(str("""
                        if {}:
                            {}
                    """.format(
                        cmd.split(", ")[1],
                        cmd.split(", ")[0]
                    )
                    ))
                else: eval(str(cmd))

run("main", [])


