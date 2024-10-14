#
# Copyright 2024 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import sys
from com.xebialabs.xlrelease.builder import TaskBuilder
from com.xebialabs.xlrelease.builder import VariableBuilder
from java.util import ArrayList
from java.util import Date
from java.text import SimpleDateFormat

def stringToBoolean(s):
    if s.lower() == "true":
        return True
    elif s.lower() == "false":
        return False
    else:
        print "Invalid value for Boolean/Checkbox variable: %s.  Valid values are True, False.\n" % s
        raise Exception

def stringToInteger(s):
    try:
        return int(s)
    except:
        print "Invalid value for Number/Integer variable %s.\n" % s
        raise Exception

def stringToDate(s, simpleDateFormat):
    sdf = SimpleDateFormat(simpleDateFormat)
    try:
        return sdf.parse(s)
    except:
        print "Invalid value for Date variable %s\n" % s
        raise Exception

def stringToListString(s):
    print "stringToListString() not implemented for %s\n" %s
    raise Exception

def stringToMapStringString(s):
    print "stringToMapStringString() not implemented for %s\n" %s
    raise Exception

def stringToSetString(s):
    print "stringToSetString() not implemented for %s\n" %s
    raise Exception

def getTaskPosition(task):
    for t in task.container.tasks:
        if t.id == task.id:
            return task.container.tasks.index(t)

def buildTemplateVariableList(templateVariables, templateVariableDelimiter, dateFormat):
    templateVariableList = []

    for item in templateVariables:
        (varKey, varType, varValue) = item.split(templateVariableDelimiter)
        if varType == "Text":
            templateVariableList.append(VariableBuilder.newStringVariable(varKey, varValue).build())
        elif varType == "Password":
            templateVariableList.append(VariableBuilder.newPasswordStringVariable(varKey, varValue).build())
        elif varType == "Checkbox":
            templateVariableList.append(VariableBuilder.newBooleanVariable(varKey, stringToBoolean(varValue)).build())
        elif varType == "Number":
            templateVariableList.append(VariableBuilder.newIntegerVariable(varKey, stringToInteger(varValue)).build())
        elif varType == "List":
            templateVariableList.append(VariableBuilder.newListStringVariable(varKey, stringToListString(varValue)).build())
        elif varType == "Date":
            templateVariableList.append(VariableBuilder.newDateVariable(varKey, stringToDate(varValue, dateFormat)).build())
        elif varType == "Key-value Map":
            templateVariableList.append(VariableBuilder.newMapStringStringVariable(varKey, stringToMapStringString(varValue)).build())
        elif varType == "Set":
            templateVariableList.append(VariableBuilder.newSetStringVariable(varKey, stringToSetString(varValue)).build())
        else:
            print "Ignoring entry due to invalid type for %s\n" % item

    return templateVariableList

print "Executing xlr.DynamicCreateReleaseTask.py"

currentPhase = getCurrentPhase()
currentTask = getCurrentTask()

tbTask = TaskBuilder.newCreateReleaseTask() \
    .withTitle("Dynamically-added Create Release Task") \
    .withTemplateId(templateId) \
    .withNewReleaseTitle(newReleaseTitle) \
    .withFolderId(folderId) \
    .withStartRelease(startRelease) \
    .withVariables(buildTemplateVariableList(templateVariables, templateVariableDelimiter, dateFormat)) \
    .build()

phaseApi.addTask(currentPhase.id, tbTask, getTaskPosition(currentTask) + 1)
