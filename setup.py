# pip install cx_freeze
import cx_Freeze
executaveis = [ 
               cx_Freeze.Executable(script="main.py", icon="Recursos\Icone\Icone.ico") ]
cx_Freeze.setup(
    name = "Surrealism",
    options={
        "build_exe":{
            "packages":["pygame", "pyttsx3", "speech_recognition"],
            "include_files":["Recursos/"],
            "include_msvcr": True
        }
    }, executables = executaveis
)

# python setup.py build
# python setup.py bdist_msi
