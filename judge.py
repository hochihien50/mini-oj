import subprocess
import os

def run(pid,code):

    open("main.cpp","w").write(code)

    compile=subprocess.run(
        ["g++","main.cpp","-o","main"],
        capture_output=True
    )

    if compile.returncode!=0:
        return "CE"

    inp=open(f"tests/{pid}.in").read()

    run=subprocess.run(
        ["./main"],
        input=inp,
        text=True,
        capture_output=True,
        timeout=2
    )

    out=run.stdout.strip()
    ans=open(f"tests/{pid}.out").read().strip()

    if out==ans:
        return "AC"
    else:
        return "WA"
