class Displayer:
    def __init__(self) -> None:
        pass

    @staticmethod
    def displayMessage(obj):
        print(">>> " + obj["username"] + ": " + obj["message"])

    @staticmethod
    def displayExcpetionMessage(obj):
        print("--------> Exception")
        print("--------> OnException Message -----> " + str(obj))

    @staticmethod
    def logMessage(obj, func_name):
        print("[LOG] Message From --> " + str(func_name))
        print("[LOG] [TIME] >>> " + obj)