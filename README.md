# Pretty System Verilog
A Python script which turns System Verilog files pretty according to some configurable rules. Under development.
# Dependencies

For the RTL-Tree function, treelib is required

```bash
sudo pip3 install treelib
```
# Files

| File         | Description|
| :-           | :-         |
| psa.py       | Here I run the code during development |
| sv_parser.py | This is the main class. The functions are spread out through other files |
| sv_get.py    | Functions for extracting certain code from a System Verilog file         |
| sv_file.py   | All functions which operates on or with files are contained in this file |
| rulebook.py  | Opens a YML file containing format rules and stores them in a dictionary |

# RTL-Tree

With the RTL-Tree function you can get a hierarchy tree of your RTL project:

```bash
top_module
├── submodule00
│   ├── submodule01
│   │   └── submodule02
│   │       ├── submodule03
│   │       ├── submodule03
│   │       ├── submodule03
│   │       └── submodule03
│   └── submodule01
│       └── submodule02
│           ├── submodule03
│           ├── submodule03
│           ├── submodule03
│           └── submodule03
└── submodule01
    └── submodule02
        ├── submodule03
        ├── submodule03
        ├── submodule03
        └── submodule03
```

## Known Issues
- Excludes package files only by looking at the file ending "_pkg.sv"
- For generate: only one instance is printed