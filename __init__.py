# coding: utf-8
"""
Base para desarrollo de modulos externos.
Para obtener el modulo/Funcion que se esta llamando:
     GetParams("module")

Para obtener las variables enviadas desde formulario/comando Rocketbot:
    var = GetParams(variable)
    Las "variable" se define en forms del archivo package.json

Para modificar la variable de Rocketbot:
    SetVar(Variable_Rocketbot, "dato")

Para obtener una variable de Rocketbot:
    var = GetVar(Variable_Rocketbot)

Para obtener la Opcion seleccionada:
    opcion = GetParams("option")


Para instalar librerias se debe ingresar por terminal a la carpeta "libs"
    
    pip install <package> -t .

"""

import os
import sys

base_path = tmp_global_obj["basepath"]
cur_path = base_path + 'modules' + os.sep + 'Abbyy_Vantage' + os.sep + 'libs' + os.sep
if cur_path not in sys.path:
    sys.path.append(cur_path)

from abbyy_Vantage_Obj import Abbyy_Vantage_Obj

global abbyy_I

module = GetParams("module")

try:

    if (module == "connectToAbbyy"):

        username = GetParams("username")
        password = GetParams("password")
        
        abbyy_I = Abbyy_Vantage_Obj(username, password)

        abbyy_I.requestToken()

        resultConnection = False

        if abbyy_I.accessToken:
            resultConnection = True
        
        whereToStore = GetParams("whereToStore")
        SetVar(whereToStore, resultConnection)

    if (module == "getHtmlSkillsId"):
        
        skillsId = abbyy_I.getSkills()
        SkillsId = []

        for each in skillsId:
            SkillsId.append(each["name"])
        
        SetVar("Abbyy_Vantage_fake_var", {
            "skillsId" : skillsId,
        })

    if (module == "readFile"):

        skillIdIframe = GetParams("iframe")
        fileToRead = GetParams("fileToRead")

        skillId = eval(skillIdIframe)["skillId"]

        resultRead = abbyy_I.transaction(skillId)

        whereToStore = GetParams("whereToStore")
        SetVar(whereToStore, resultRead)

except Exception as e:
    print("\x1B[" + "31;40mAn error occurred\x1B[" + "0m")
    PrintException()
    raise e