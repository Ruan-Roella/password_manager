from source.views import Application

# TODO: Opção de criptogravar várias senhas.
# TODO: Criar o método de descriptografar.

if __name__ == "__main__":
    app = Application()

    while app.running:
        app.clean_prompt
        app.header()

        opt = app.menu_option(
            'Gerar minha Chave',
            'Salvar uma Senha',
            'Ver minhas Senhas',
            'Sair'
        )

        match opt:
            case 1:
                app.generate_key()
                continue
            case 2:
                app.save_password()
                continue
            case 3:
                app.show_password()
                continue
            case 4:
                app.clean_prompt
                app.running = False