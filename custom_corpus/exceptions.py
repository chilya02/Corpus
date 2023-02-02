class StepsException(Exception):
    def __init__(self, *args) -> None:
        super().__init__(*args)
        if args:
            self.message = args[0]
        else:
            self.message = None
    
    def __str__(self) -> str:
        if self.message:
            return f'Ошибка в количестве стоп \n\n{self.message}'
        return f'Ошибка в количестве стоп'