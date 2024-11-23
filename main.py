from source.app import Application


if __name__ == "__main__":
    app = Application()

    while app.running:
        app.clean_prompt
        app.header()

        opt = app.menu_option(
            'Gerar minha Chave',
            'Salvar uma Senha',
            'Ver minhas Senhas',
            "Criar uma senha segura",
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
                app.generate_password()
                continue
            case 5:
                app.clean_prompt
                app.running = False