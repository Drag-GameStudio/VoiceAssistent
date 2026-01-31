import re
# service name|key="value"|key="value"

def read_command(command: str):
    splited_comand = command.split("|")
    service_name = splited_comand[0]
    kwargs = {}
    for key_args in splited_comand[1:]:
        key = key_args.split("=")[0]
        value = "".join(re.split(r'([=])', key_args)[1:])
        value = value[2:len(value) - 1]
        kwargs[key] = value

    return service_name, kwargs

def check_raw_answer(raw_answer: str) -> tuple[bool, str]:
    if raw_answer.split()[0] == "RUNMODULE":
        return True, raw_answer.split(maxsplit=1)[-1]

    return False, raw_answer