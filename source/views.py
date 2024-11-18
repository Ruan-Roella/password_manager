from .backend import Console, Backend, Cryptography, InvalidToken, PasswordGenerate
from .backend import emojis
from source.forms import forms
from .models import Passwords

import time, os

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
        if not self.check_key:
            Console.Write("Bem-Vindo, por favor gere sua chave\nantes de começar. Obrigado!", fg='lightcyan_ex', weight='bright')
        
        menu ={ k: v for k,v in enumerate(options, start=1) }
        #Console.Write("\n")
        
        menu_items = [f'[{i}] {opt}\n' for i, opt in menu.items()]
        Console.Write(*menu_items)

        try: 
            opt = int(Console.ReadLine("Selecione: "))
        except ValueError:
            Console.Write('Opção inválida.', fg='red')
            time.sleep(1)
            os.system('cls')
        else:
            return opt

    def generate_key(self):
        
        if self.check_key:

            self.header()
            Console.Write("Você já tem uma chave. Use para\ncriptografar suas senhas na opção\n\"Salvar uma senha\".", fg='yellow')
            Console.ReadLine("← Voltar ")
            return
        
        self.header()
        token = Cryptography.generate_key()
        
        Console.Write("Gerando...", fg='magenta')
        self.save(token)
        time.sleep(1)

        Console.Write("Parabéns, sua Chave foi criada com sucesso.")
        Console.Write(f"{emojis('1F511')} Chave: {token.decode()}")
        Console.Write(f'Sua chave foi salva no diretório abaixo ↓:')
        Console.Write(self.key_path, fg='lightmagenta_ex')
        Console.ReadLine("← Voltar ")

    def save_password(self):
        self.check_db
        self.header()

        if not self.check_key:
            Console.Write("Você ainda não gerou sua chave.", fg='lightred_ex')
            Console.ReadLine("← Voltar ")
            return
        

        Console.Write("Lembrando que, as senhas serão\nCriptografadas para sua segurança.", fg='lightcyan_ex')
        Console.Write("Cuidado: Não perca ou apague sua Chave,\npois a criptografia é única.", fg='lightyellow_ex', weight='bright')
        Console.ReadLine('Vamos lá ')

        # Domain Field
        while True:
            self.header()
            if self.errors:
                Console.Write(self.errors, fg='lightred_ex')
            
            domain = forms.TextField(label='Domínio', help_text="O domínio refere-se ao site que você\ndeseja salvar a senha. Exemplo: Youtube")

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

            username = forms.TextField(label="Usuário", help_text="O usuário refere-se login no domínio\nespecificado.", opcional=True)
            
            break

        # Password Field
        while True:
            self.header()
            if self.errors:
                Console.Write(self.errors, fg='lightred_ex')

            password = forms.PasswordField( label="Senha", help_text="Senha do seu domínio especificado.", error_msg="Senha muito curta.")

            if password.value == "":
                self.errors = password.empty_value
                continue
            
            if len(password.value) < 4:
                self.errors = password.error_msg
                continue

            self.errors = None
            break

        # Key Field
        while True:
            self.header()
            if self.errors:
                Console.Write(self.errors, fg='lightred_ex')

            key = forms.SecretKeyField(label="Chave", help_text="Para finalizar, informe a sua Chave.", error_msg="Chave inválida, Tente novamente.")

            if key.value == "":
                self.errors = key.empty_value
                continue

            if key.value != Cryptography.signature():
                self.errors = key.error_msg
                continue
            
            self.errors = None
            break

        crypt = Cryptography(key.value)
        
        objects = Passwords(
           domain=domain.value,
           username=username.value,
           password=crypt.encrypt(password.value)
        )

        objects.save()
        Console.Write("Senha criptografada com sucesso.", fg='green')
        Console.ReadLine("← Voltar ")

    def show_password(self):
        self.check_db
        self.header()

        if not self.check_key:
            Console.Write("Você ainda não gerou sua chave.", fg='lightred_ex')
            Console.ReadLine("← Voltar ")
            return
        
        Console.Write(f"Para ver uma senha, você precisa\nprimeiro acessar: db > {self.db_path},\ncopiar a senha que deseja descriptografar\ne informar-la no campo Senha.", fg='yellow')
        Console.Write("Logo após, você precisa fornecer sua Chave.\nAssim você irá conseguir recuperar a sua senha.", fg='yellow')
        Console.ReadLine("Vamos lá ")

        # Password Field
        while True:
            self.header()
            if self.errors:
                Console.Write(self.errors, fg='lightred_ex')

            password = forms.PasswordField(label="Senha", help_text="Senha criptografada.")

            if password.value == "":
                self.errors = password.empty_value
                continue
            
            self.errors = None
            break

        # Key Field
        while True:
            self.header()
            if self.errors:
                Console.Write(self.errors, fg='lightred_ex')

            key = forms.SecretKeyField(label="Chave", help_text="Para finalizar, informe a sua Chave.", error_msg="Chave inválida, Tente novamente.")

            if key.value == "":
                self.errors = key.empty_value
                continue

            if key.value != Cryptography.signature():
                self.errors = key.error_msg
                continue

            self.errors = None
            break

        try:
            crypt = Cryptography(key.value)
            descrypted = crypt.decrypt(password.value)
        except InvalidToken:
            Console.Write("Senha inválida ou criptografia não foi feita com esta chave.", fg='red')
            Console.ReadLine("← Voltar ")
            return
        
        data = self.views_details(password.value)
        data.insert(2, descrypted.decode())
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

                            length = forms.TextField(label="Tamanho", help_text="mínimo 4 e máximo 6.", error_msg="Tamnho inválido.")

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

                            alnum = forms.TextField(label="Tamanho", help_text="mínimo 8 e máximo 23.", error_msg="Tamanho inválido.")

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