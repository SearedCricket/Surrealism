import cx_Freeze
import sys
import os

build_exe_options = {
    "packages": [
        "pygame",
        "pyttsx3",
        "speech_recognition",
        "queue",
        "comtypes",
        "pyaudio",
        "tkinter",
        "aifc",  
        "wave",  
        "audioop",
        "chunk"
    ],
    "excludes": [
        "numpy",
        "opencv-python",
        "PyQt5",
        "tornado",
        "boto3",
        "tensorflow"
    ],
    "include_files": [
        ("Recursos", "Recursos"),
    ],
    "include_msvcr": True,
}

executaveis = [
    cx_Freeze.Executable(
        script="main.py",
        icon="Recursos/Icone/Icone.ico",
        base="Win32GUI" if sys.platform == "win32" else None,
        target_name="Surrealism.exe"
    )
]

cx_Freeze.setup(
    name="Surrealism",
    version="1.0",
    description="Surrealism Game",
    options={"build_exe": build_exe_options},
    executables=executaveis
)