import os


def pathInfo(filePath: str, parentCond: bool = False):
    if "/" in filePath:
        splitter = "/"
    if "\\" in filePath:
        splitter = "\\"
    fullPathArray = filePath.split(splitter)
    file = fullPathArray[-1]
    if parentCond:
        parentPath = splitter.join(fullPathArray[0:-1])
        return file, parentPath
    else:
        return file


def validate(filePath: str, Error: bool = False):
    file, parentPath = pathInfo(filePath, parentCond=True)
    try:
        os.chdir(parentPath)
        files = os.listdir()
        if file in files:
            return True
        else:
            return False
    except Exception as e:
        if Error:
            return False, e
        else:
            return False
