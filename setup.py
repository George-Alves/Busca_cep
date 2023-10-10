import sys
from cx_Freeze import setup, Executable

build_exe_options = {
    "packages": ["sqlite3", "tkinter", "requests"],  # Inclua todas as bibliotecas que você está usando
    "include_files": ["cep_database.db"],  # Inclua todos os arquivos adicionais necessários
}

base = None
if sys.platform == "win32":
    base = "Win32GUI"  # Use "Win32GUI" se não desejar que uma janela de console apareça no Windows

setup(
    name="BuscaCEP",
    version="1.0",
    description="Sua descrição aqui",
    options={"build_exe": build_exe_options},
    executables=[Executable("busca_cep.py", base=base)],
)
