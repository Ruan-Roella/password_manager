from source.core import Backend, Console, TextField, PasswordField, Cryptography, InvalidToken, PasswordGenerate
from source.core.db import Users, Passwords

import time, os
import pyperclip

class Application(Backend):
    def __init__(self):
        super().__init__()
        self.running = True
        self.clean_prompt = os.system("cls")
        self.errors = None
    
    def header(self):
        
        os.system('cls')

        Console.Write("=="*18, fg='white')
        Console.Write('\t', "Gerenciador de Senhas", fg='blue', weight='bright')
        Console.Write("=="*18, fg='white')

    def menu_option(self, *options: object):
        if not self.is_registred():
            Console.Write("Bem-Vindo, por favor gere sua chave\nantes de começar. Obrigado!", fg='lightcyan_ex', weight='bright')
        
        if isinstance(options[0], tuple):
            Console.Write(f" #  Domínio\t\tDescrição")
            for opt in options:
                Console.Write(f"[{opt[0]}] {opt[1]}\t\t{opt[2]}")
        else:
            for idx, item in enumerate(options, start=1):
                Console.Write(f"[{idx}] {item}")

        try: 
            opt = int(Console.ReadLine("Selecione: "))
        except ValueError:
            Console.Write('Opção inválida.', fg='red')
            time.sleep(1)
            os.system('cls')
        else:
            return opt

    def secure_pincode(self, title: str, confirm: bool = False):

        while True:
            self.header()

            Console.Write(title, fg='magenta', weight='bright')

            if self.errors:
                Console.Write(self.errors, fg='lightred_ex')

            pin = PasswordField("PIN", "Digitos mín 4 max 6.", error_msg="Pin inválido, Tente novamente.")
            if pin.value == '':
                self.errors = pin.empty_value
                continue
            
            if len(pin.value) < 4 or len(pin.value) > 6:
                self.errors = pin.error_msg
                continue

            if not pin.value.isdigit():
                self.errors = "PIN pode ser apenas digitos."
                continue
            
            if confirm:
                pin2 = PasswordField("Confirme o PIN", error_msg="Os PIN são diferentes.")

                if pin.value != pin2.value:
                    self.errors = pin2.error_msg
                    continue
            break
        return pin

    def generate_key(self):
        
        if self.is_registred():

            self.header()
            Console.Write("Você já tem uma chave. Use para\ncriptografar suas senhas na opção\n\"Salvar uma senha\".", fg='yellow')
            Console.ReadLine("← Voltar ")
            return
        
        pincode = self.secure_pincode(title="Crie um PIN.", confirm=True)

        self.header()
        
        token = Cryptography.generate_key()
        user = Users(
            pin = self.set_pincode(pincode.value),
            key = token.decode()
        )
        user.save()

        Console.Write("Gerando...", fg='magenta')
        time.sleep(1)

        Console.Write("Parabéns, sua Chave foi criada com sucesso.", fg='lightgreen_ex')
        Console.ReadLine("← Voltar ")

    def save_password(self):
        self.header()

        if not self.is_registred():
            Console.Write("Você ainda não gerou sua chave.", fg='lightred_ex')
            Console.ReadLine("← Voltar ")
            return
        

        Console.Write("Lembrando que, as senhas serão\nCriptografadas para sua segurança.", fg='lightcyan_ex')
        Console.Write("Cuidado: Não perca, altere ou apague\nsua Chave, pois a criptografia é única.", fg='lightyellow_ex', weight='bright')
        Console.ReadLine('Vamos lá ')

        # Domain Field
        while True:
            self.header()
            if self.errors:
                Console.Write(self.errors, fg='lightred_ex')
            
            domain = TextField(label='Domínio', help_text="O domínio refere-se ao site que você\ndeseja salvar a senha. Exemplo: Youtube")

            if domain.value == "":
                self.errors = domain.empty_value
                continue
            
            self.errors = None
            break

        # Username Field
        while True:
            self.header()
            if self.errors:
                Console.Write(self.errors, fg='lightred_ex')

            username = TextField(label="Descrição", help_text="Uma descrição ao que se refere,\nPode ser Nome de Usuário.", opcional=True)
            
            break

        # Password Field
        while True:
            self.header()
            if self.errors:
                Console.Write(self.errors, fg='lightred_ex')

            password = PasswordField( label="Senha", help_text="Senha do seu domínio especificado.", error_msg="Senha muito curta.")

            if password.value == "":
                self.errors = password.empty_value
                continue
            
            if len(password.value) < 4:
                self.errors = password.error_msg
                continue

            self.errors = None
            break

        pincode = self.secure_pincode(title="Para confirmar que é você mesmo.\nInforme seu PIN.")

        if self.pin_isvalid(pincode.value):
            crypt = Cryptography(Cryptography.signature())
            pwd = crypt.encrypt(password.value).decode()

            objects = Passwords(
            domain=domain.value,
            description=username.value,
            password=pwd
            )

            objects.save()
            Console.Write("Senha criptografada com sucesso.", fg='green')
            Console.ReadLine("← Voltar ")
            return
        
        Console.Write("Oops... Houve algo de errado.", fg='green')
        Console.ReadLine("← Voltar ")

    def show_password(self):
        self.header()

        if not self.is_registred():
            Console.Write("Você ainda não gerou sua chave.", fg='lightred_ex')
            Console.ReadLine("← Voltar ")
            return
        
        if not self.select_from('Body'):
            Console.Write("Você Ainda não tem nenhuma senha salva.")
            Console.ReadLine("← Voltar ")
            return

        while True:
            self.header()
            if self.errors:
                Console.Write(self.errors, fg='lightred_ex')
            
            Console.Write("Escolha uma das opções para copiar a\nsenha criptografada do banco de dados.", fg='magenta')
            menu = self.select_from('Body', ['id', 'domain', 'description'])
            opt = self.menu_option(*menu)

            clipbord = self.get_password(opt)
            pyperclip.copy(clipbord)
            Console.Write("Senha copiada con sucesso.", fg='lightgreen_ex')
            Console.ReadLine("Continuar → ")
            break


        # Password Field
        while True:
            self.header()
            if self.errors:
                Console.Write(self.errors, fg='lightred_ex')

            password = PasswordField(label="Senha", help_text="Senha criptografada.")

            if password.value == "":
                self.errors = password.empty_value
                continue
            
            self.errors = None
            break

        try:
            crypt = Cryptography(Cryptography.signature())
            descrypted = crypt.decrypt(password.value)
        except InvalidToken:
            Console.Write("Senha inválida ou criptografia não foi feita com esta chave.", fg='red')
            Console.ReadLine("← Voltar ")
            return
        
        data = self.show_details(opt)
        data[2] = descrypted.decode()
        texts = ('Domínio', 'Usuário', 'Senha', 'Data de Registro')
        Console.Write("Resultado: ")
        for label, value in zip(texts, data):
            Console.Write(f"{label}: {value}", fg='green', weight='bright')
        Console.ReadLine("← Voltar ")

    def generate_password(self):
        self.header()

        
        while True:
            self.header()
            Console.Write("Um gerador de senhas seguras para\nvocê utilizar nas suas aplicações.", fg='lightcyan_ex')
            Console.Write("OBS: A senha gerada ainda não está\ncriptografada.", fg='yellow')
            
            Console.Write("Escolha umas das opções abaixo")
            opt = self.menu_option("Padrão de senha PIN", "Senha Alfanumérica", "Sair")

            match opt:
                case 1:

                    self.header()
                    Console.Write("Senha numérica de cerca de 4 dígitos,\npodendo atingir até 6 dígitoss", fg='white')

                    Console.Write("Padrão de senha PIN", fg='lightmagenta_ex')
                    opt = self.menu_option("Continuar", "Voltar")

                    if opt == 1:
                        while True:
                            self.header()
                            if self.errors:
                                Console.Write(self.errors, fg="lightred_ex")

                            length = TextField(label="Tamanho", help_text="mínimo 4 e máximo 6.", error_msg="Tamnho inválido.")

                            if length.value == "":
                                self.errors = length.empty_value
                                continue
                            
                            if int(length.value) < 4 or int(length.value) > 6:
                                self.errors = length.error_msg
                                continue
                            
                            self.errors = None
                            break

                        pin_code = PasswordGenerate.pin_code(length.value)
                        Console.Write("PIN gerado com sucesso.", fg='lightgreen_ex')
                        Console.Write(f"Sua Senha: {pin_code}")
                        Console.ReadLine("← Voltar ")

                    if opt == 2:
                        continue

                case 2:

                    self.header()
                    Console.Write("A senha alfanumérica é a mais\nabrangente, pode englobar letras\nmaiúsculas, minúsculas, números\ne caracteres especiais.", fg='white')

                    Console.Write("Senha Alfanumérica", fg='lightmagenta_ex')
                    opt = self.menu_option("Continuar", "Voltar")

                    if opt == 1:
                        while True:
                            self.header()
                            if self.errors:
                                Console.Write(self.errors, fg='lightred_ex')

                            alnum = TextField(label="Tamanho", help_text="mínimo 8 e máximo 23.", error_msg="Tamanho inválido.")

                            if alnum.value == "":
                                self.errors = alnum.empty_value
                                continue
                            
                            if int(alnum.value) < 8 or int(alnum.value) > 23:
                                self.errors = alnum.error_msg
                                continue
                            
                            self.errors = None
                            break

                        alnumeric = PasswordGenerate.alnumeric(alnum.value)
                        Console.Write("Senha gerada com sucesso.", fg='lightgreen_ex')
                        Console.Write(f"Senha: {alnumeric}")
                        Console.ReadLine("← Voltar ")

                    if opt == 2:
                        continue

                case 3: break
                case _: continue