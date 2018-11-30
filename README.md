# PSE

## Instalação & Execução
### Ubuntu
- Instale o gerenciador de pacotes PIP:

  ```
  $ sudo apt update
  $ sudo apt install python3-pip
  ```

- Baixe o repositório zipado ou clone utilizando o git (o caminho padrão, quando omitido, é ./pse-pid):
  
  ```
  $ sudo apt update
  $ sudo apt install git
  $ git clone https://github.com/GeovaneF55/pse-pid.git [caminho/para/repositorio]
  ``` 
  
- Navegue até a pasta raíz do projeto e instale as dependências necessárias para a execução do programa:

  ```
  $ cd caminho/para/repositório/
  $ sudo pip3 install -e .
  ```
 
- Uma vez dentro da pasta raíz do projeto, o execute:

  ```
  $ python3 pse
  ```
  
- OBS: Em caso de erros relacionados a biblioteca tkinter, proceda da seguinte forma:

  ```
  $ sudo apt install python3-tk
  ```
  
### Windows 10
- Instale o gerenciador de pacotes Chocolatey. Para isso, siga as instruções do link: https://chocolatey.org/install

- Baixe o repositório zipado ou, pelo CMD ou Powershell (ambos como administrador), clone o projeto utilizando o git (o caminho padrão, quando omitido, é .\pse-pid):

  ```
  $ choco install git
  $ git clone https://github.com/GeovaneF55/pse-pid.git [caminho/para/repositorio]
  ```
  
- Instale a versão 3 do Python:

  ```
  $ choco install python
  ```

- Feche e reabra o CMD/Powershell (como administrador) para garantir que as variáveis de ambiente estejam atualizadas

- Atualize o gerenciador de pacotes PIP:

  ```
  $ python -m pip install pip --upgrade
  ```
  
- Navegue até a pasta raíz do projeto e instale as dependências necessárias para a execução do programa:

  ```
  $ cd caminho\para\repositório\
  $ pip install -e .
  ```
  
- Uma vez dentro da pasta raíz do projeto, o execute:

  ```
  $ python .\pse
  
## Manual do Usuário
[Vídeo de Demonstração](https://youtu.be/Pze5D69Sipw)  
[manual do usuário](doc/MANUAL.md)

## Documentação
[PSE](doc/PSE.md)
