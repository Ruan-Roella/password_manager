from .backend import Console, Backend, Cryptography, InvalidToken
from .backend import emojis
from .constants import *
from .models import Passwords

import time, os

class Application(Backend):
    def __init__(self):
        super().__init__()
        self.running = True
        self.text_eror = []
    
    @property
    def clean_prompt(self):
        return os.system('cls')

    def header(self):
        Console.Write("=="*18, fg='white')
        Console.Write('\t', "Gerenciador de Senhas", fg='blue', weight='bright')
        Console.Write("=="*18, fg='white')

    def menu_option(self, *options: object):
        if not self.check_key:
            Console.Write("Bem-Vindo, por favor gere sua chave\nantes de começar. Obrigado!", fg='lightcyan_ex', weight='bright')
        
        menu ={ k: v for k,v in enumerate(options, start=1) }
        Console.Write("Escolha umas da opções abaixo para começar.")
        
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
            self.clean_prompt
            self.header()
            Console.Write("Você já tem uma chave. Use para\ncriptografar suas senhas na opção\n\"Salvar uma senha\".", fg='yellow')
            Console.ReadLine("← Voltar ")
            return
        
        self.clean_prompt
        self.header()
        token = Cryptography.generate_key()
        
        Console.Write("Gerando...", fg='magenta')
        self.save(token)
        time.sleep(1)

        Console.Write("Parabéns, sua Chave foi criada com sucesso.")
        Console.Write(f"{emojis(KEY)} Chave: {token.decode()}")
        Console.Write(f'Sua chave foi salva no diretório abaixo ↓:')
        Console.Write(self.key_path, fg='lightmagenta_ex')
        Console.ReadLine()

    def save_password(self):
        self.check_db
        self.clean_prompt
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
            self.clean_prompt
            self.header()
            if self.text_eror:
                Console.Write(self.text_eror, fg='red')
            
            Console.Write("O domínio refere-se ao site que você\ndeseja salvar a senha. Exemplo: Youtube", fg='black')
            domain = Console.ReadLine("Domínio: ")

            if domain == "":
                self.text_eror = 'O domínio é obrigatório.'
                continue
            break

        # Username Field
        while True:
            self.clean_prompt
            self.header()

            Console.Write("O usuário refere-se login no domínio\nespecificado.", fg='black')
            Console.Write("Campo Opcional", fg='lightmagenta_ex')
            username = Console.ReadLine("Usuário: ")
            break

        # Password Field
        while True:
            self.clean_prompt
            self.header()
            if self.text_eror:
                Console.Write(self.text_eror, fg='red')
            
            Console.Write("Senha do seu domínio especificado.", fg='black')
            password = Console.ReadLine("Senha: ", password=True)

            if password == "":
                self.text_eror = "Senha é um campo obrigatório."
                continue
            break

        # Key Field
        while True:
            self.clean_prompt
            self.header()
            
            Console.Write("Para finalizar, informe a sua Chave.", fg='blue')
            key = Console.ReadLine(f"Chave: ", password=True)

            if key != Cryptography.signature():
                self.text_eror = "Chave inválida, Tente novamente."
                continue
#
            if key == "":
                self.text_eror = "A chave é obrigatória."
                continue
            break

        
        crypt = Cryptography(key)
        
        objects = Passwords(
           domain=domain.strip(),
           username=username.strip(),
           password=crypt.encrypt(password.strip())
        )
        objects.save()
        
        Console.Write("Senha criptografada com sucesso.", fg='green')
        Console.ReadLine("← Voltar ")

    def show_password(self):
        self.check_db
        self.clean_prompt
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
            self.clean_prompt
            self.header()
            if self.text_eror:
                Console.Write(self.text_eror, fg='red')
            
            Console.Write("Senha criptografada.", fg='black')
            password = Console.ReadLine("Senha: ", password=True)

            if password == "":
                self.text_eror = "Senha é um campo obrigatório."
                continue
            break

        # Key Field
        while True:
            self.clean_prompt
            self.header()
            if self.text_eror:
                Console.Write(self.text_eror, fg='red')
            
            Console.Write("Para finalizar, informe a sua Chave.", fg='blue')
            key = Console.ReadLine(f"Chave: ", password=True)

            if key != Cryptography.signature():
                self.text_eror = "Chave inválida, Tente novamente."
                continue
#
            if key == "":
                self.text_eror = "A chave é obrigatória."
                continue
            break

        try:
            crypt = Cryptography(key)
            descrypted = crypt.decrypt(password.strip())
        except InvalidToken:
            Console.Write("Senha inválida ou criptografia não foi feita com esta chave.", fg='red')
            Console.ReadLine("← Voltar ")
            return
        
        data = self.views_details(password.strip())
        data.insert(2, descrypted.decode())
        texts = ('Domínio', 'Usuário', 'Senha', 'Data de Registro')
        Console.Write("Resultado: ")
        for label, value in zip(texts, data):
            Console.Write(f"{label}: {value}", fg='green', weight='bright')
        Console.ReadLine("← Voltar ")