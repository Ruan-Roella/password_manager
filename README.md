Gerenciador de Senhas
=====================

A proposta do projeto é um sistema que gerência senhas pelo `Console`, criptografando, descriptografando, Salvando e fazendo amostragem dos dados.

<p align="center" width="100%">
    <img width="45%" src="https://github.com/Ruan-Roella/password_manager/blob/main/image/console_image.png">
</p>

<p align="center" width="100%">
    <img width="10%" style="padding: 5px" src="https://img.shields.io/badge/Versão-2.0.0-blue">
    <img width="10%" style="padding: 5px" src="https://img.shields.io/badge/Download-blue">
</p>


### Gerar minha Chave
- Cria uma chave em em um diretório `key` com arquivo `key.key` onde ficará armazenada a Chave que irá usar para **Salvar** e __Ver__ suas senhas.

### Salvar uma Senha
- É necessário preencher 3(três) campos.
    - __Domínio__: *É referente ao site e/ou aplicativo a qual você deseja salvar a senha criptografada, podendo ser apenas o nome.*
        > Exemplo: Domínio: `GitHub` ou `https://github.com/`
    - __Usuário__: Seu username e/ou email do mesmo, caso queria salvar-lo também. Porém não é criptografado. **Campo Opcional**
    - __Senha__: A senha que irá ser criptografada e salva em um arquivo `passwords.yml` em um diretório `db`.
    - __Chave__: E por fim a chave que foi gerada, você irá copiar e colar aqui. Se tudo estiver correto, você receberá uma mensagem de sucesso no terminal.

### Ver minhas Senhas
- Nesta parte você precisará copiar e colar a senha criptografada dentro de __db > passwords.yml__, logo após fazer o mesmo processo com sua chave. Após tudo ocorrer corretamente, irá retornar um detalhe monstrando tudo no terminal.
> [!CAUTION]
> Não perca sua Chave pois a criptografia é única.<br/>A chave é obrigatória para a descriptografia da senha.



