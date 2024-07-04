# Projeto APKAnalyzer

A ferramenta APKAnalyzer foi desenvolvida com um motor de classificação para arquivos APK com *multi-view* na composição dos vetores de características e seleção de característica com otimização multiobjetivo.


## Requisitos
Para instalar e executar este projeto, é necessário ter Python 3.10 e Docker instalados na máquina. Os pacotes Python necessários estão listados no arquivo `requirements.txt`.

### Instalação dos Requisitos
1. Clone o repositório para sua máquina local:
    ```sh
    git clone <URL do repositório>
    cd APKAnalyzer
    ```

2. Crie um ambiente virtual e ative-o:
    ```sh
    python -m venv venv
    source venv/bin/activate  # Linux/macOS
    venv\Scripts\activate  # Windows
    ```

3. Instale os pacotes Python necessários:
    ```sh
    pip install -r requirements.txt
    ```
### Instalando o Docker
1. Siga as instruções para instalar o Docker na sua máquina a partir do [site oficial do Docker](https://docs.docker.com/get-docker/).

2. Adicione seu usuário ao grupo Docker para evitar a necessidade de permissões root:
    ```sh
    sudo usermod -aG docker $USER
    ```

3. Faça logout e login novamente, ou reinicie o sistema, para que as alterações tenham efeito.

4. Verifique a instalação do Docker com o comando:
    ```sh
    docker --version
    ```

5. Baixe a imagem `alexmyg/andropytool:latest` necessária para a análise:
    ```sh
    docker pull alexmyg/andropytool:latest
    ```
### Outras dependências

Para o correto funcionando dessa ferramenta, arquivos de configuração devem estar presentes no diretório raiz da aplicação:

#### ./dumps/
- **Função:** Este diretório contém os arquivos de modelo e escala utilizados para normalização e previsão das features extraídas.
- **Arquivos:**
  - `apicalls-dt-pca-las.pkl`
  - `apicalls-knn-pca-las.pkl`
  - `apicalls_minMaxScaler.pkl`
  - `apicalls_pca.pkl`
  - `apicalls-rf-pca-las.pkl`
  - `feature-selection-dt.pkl`
  - `feature-selection-knn.pkl`
  - `feature-selection-rf.pkl`
  - `opcodes-dt-pca-las.pkl`
  - `opcodes-knn-pca-las.pkl`
  - `opcodes_minMaxScaler.pkl`
  - `opcodes_pca.pkl`
  - `opcodes-rf-pca-las.pkl`
  - `perm-dt-pca-las.pkl`
  - `perm-knn-pca-las.pkl`
  - `perm_minMaxScaler.pkl`
  - `perm_pca.pkl`
  - `perm-rf-pca-las.pkl`



#### ./schemas/
- **Função:** Diretório contendo arquivos de esquema para as features. Estes arquivos são utilizados para gerar dicionários de features durante o processo de extração e análise.
- **Arquivos:**
  - `apicall-features.txt`
  - `opcodes-features.txt`
  - `perm-features.txt`

### Estrutura de diretórios:

#### ./apks/
- **Função:** Diretório onde os arquivos APK a serem analisados são armazenados. Este diretório é utilizado pelo script principal durante o processo de análise.
  
#### ./dumps/
- **Função:** Este diretório contém os arquivos de modelo e escala utilizados para normalização e previsão das features extraídas.

#### ./para-processar/
- **Função:** Arquivos APK de exemplo para testar a aplicação.

#### ./schemas/
- **Função:** Diretório contendo arquivos de esquema para as features. Estes arquivos são utilizados para gerar dicionários de features durante o processo de extração e análise.

#### ./src/
- **Função:** Diretório com todos os arquivos fontes.

## Executando a Aplicação
A execução da aplicação pode ser feita de duas maneiras: informando um arquivo específico ou um diretório. Por exemplo, consideremos o diretório `./para-processar` e o arquivos `./para-processar/6BE157CDE54CBD4B7D4866312AF8C0E099CE83AD9F449FF3539CF6FCA40BB82D.apk`.

Acesso o diretório `./src` e execute o comando:

```sh
# para processar apenas o arquivo 6BE157CDE54CBD4B7D4866312AF8C0E099CE83AD9F449FF3539CF6FCA40BB82D.apk
python APKAnalyzer.py ./para-processar/6BE157CDE54CBD4B7D4866312AF8C0E099CE83AD9F449FF3539CF6FCA40BB82D.apk 
```
```sh
# para processar todos os arquivos no diretório ./para-processar
python APKAnalyzer.py ./para-processar 
```


Na primeira execução da ferramenta, as dependências serão verificadas. Caso ocorra um erro, a ferramenta será abortada. Para corrigir as dependências veja os  [requisitos](#requisitos).

Os dados informados a partir do argumento da aplicação são copiados para `./apks`. Caso a ferramenta seja executada com privilégios, ao final do processamento, os arquivos e diretórios em `./apks` serão limpos.
