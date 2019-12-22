import traceback
import jpype
from jpype import JClass

mystr = "i'm a string"

jvm_path = jpype.getDefaultJVMPath()
print("jvm path : {}".format(jvm_path))

jpype.startJVM(jvm_path, convertStrings=False)

try:
    print("\nTest: jpype.JObject")
    jstr = jpype.JObject(mystr, JClass("java.lang.String"))
    print(jstr)
    print("OK")
except Exception as e:
    exstr = traceback.format_exc()
    print("Error: {}, stack{}".format(e, exstr))

try:
    print("\nTest:  use Class")
    StringClass = JClass("java.lang.String")
    jstr = StringClass(mystr)
    print("OK")
except Exception as e:
    exstr = traceback.format_exc()
    print("Error: {}, stack{}".format(e, exstr))

try:
    print("\nTest: JString")
    jstr = jpype.JString(mystr)
    print(jstr)
    print("OK")
except Exception as e:
    exstr = traceback.format_exc()
    print("Error: {}, stack{}".format(e, exstr))

try:
    print("\nTest: encoding GBK")
    jstr = jpype.JObject(mystr.encode("GBK"), JClass("java.lang.String"))
    print("OK")
except Exception as e:
    exstr = traceback.format_exc()
    print("Error: {}, stack{}".format(e, exstr))

try:
    print("\nTest: encoding utf-8")
    jstr = jpype.JObject(mystr.encode("utf-8"), JClass("java.lang.String"))
    print("OK")
except Exception as e:
    exstr = traceback.format_exc()
    print("Error: {}, stack{}".format(e, exstr))

jpype.shutdownJVM()

print("TODO use JPype1==0.7.1")
print("TODO use JPype1-py3")
