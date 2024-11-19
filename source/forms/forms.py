
from ..backend import Console

class Field:
    def __init__(self, label: str = '', help_text: str = '', error_msg: str = '', opcional: bool = False, password: bool = False):
        self._label = label
        self._help_text = help_text
        self._error_msg = error_msg
        self._opcional = opcional
        self._password = password
        self._value = None
    

        self.help_text()
        if self._password:
            self._value = Console.ReadLine(f"{self._label}: ", password=self._password)
        else:
            self._value = Console.ReadLine(f"{self._label}: ")

    def help_text(self):
        Console.Write(self._help_text, fg='lightwhite_ex')
        
        if self._opcional:
            Console.Write("Campo Opcional", fg='lightmagenta_ex')

    @property
    def error_msg(self):
        return self._error_msg

    @property
    def opcional(self):
        return self._opcional
    
    @property
    def empty_value(self):
        return f"{self._label} é obrigatório."
    
    @property
    def value(self):
        return self._value.strip()
    
    @value.setter
    def value(self, new):
        self._value = new
        return self._value

class TextField(Field):
    def __init__(self, label = '', help_text = '', error_msg = '', opcional = False):
        super().__init__(label, help_text, error_msg, opcional)

class PasswordField(Field):
    def __init__(self, label = '', help_text = '', error_msg = '', opcional = False):
        super().__init__(label, help_text, error_msg, opcional, password=True)

