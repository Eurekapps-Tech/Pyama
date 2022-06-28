"""
This plug-in displays a file selection dialog and opens the
stack from the file.
"""
#print("__name__ of 'load_single_stack':", __name__) #DEBUG
from .. import gui_tk
from ..stack import Stack
from ..stackviewer_tk import StackViewer

my_id = "simple_stack_reader"
__version__ = "0.1.1"

def register(meta):
    meta.name = "Read stack"
    meta.id = my_id
    meta.conf_ret = "_path"
    meta.run_dep = (my_id, "_path"), ("", "__tk-root__")
    meta.run_ret = ("stack", "_StackViewer")


def conf(d, *_, **__):
    print("Configuring 'load_single_stack'.")
    f = gui_tk.askopenfilename(parent=gui_tk.root)
    print(f)
    return {"_path": f}


def run(d, *_, **__):
    print("Running 'load_single_stack'.")
    path = d[my_id]['_path']

    # Load and show stack
    s = Stack(path)
    sv = StackViewer(root=d[""]["__tk-root__"])
    sv.set_stack(s)

    return {"stack": s,
            "_StackViewer": sv}


