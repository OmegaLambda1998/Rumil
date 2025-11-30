def pp(expression: object, name: str | None = None) -> None:
    if name:
        print(f"{name}:", end=" ")
    __import__("pprint").pprint(expression)
