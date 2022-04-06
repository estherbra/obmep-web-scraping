<div style="font-size:20px">
  <h1>Web Scraping and sending do S3 with Apache Airflow</h1>
</div>

# Sobre o Projeto

<br/>

## 🌐 Overview
Esse projeto foi feito com a linguagem de programação Python, utilizando as bibliotecas Pandas, Requests e BeautifulSoup. 
Objetivando arquiteturar solução utilizando o orquestrador de fluxos Apache Airflow para coletar dados da 16º OBMEP, foi criada uma DAG que importa dois módulos e os 
incorpora ao fluxo de envio para o Bucket "1sti-bucket" no Amazon S3, esses módulos são "scraper.py" e "local_to_s3.py".

<br/>

## Passo a passo
1. A primeira etapa consiste em ajustar algumas permissões do bucket, como a inclusão da action "s3:PutObject" na política, 
para que seja possível realizar a ingestão dos arquivos no Bucket da Amazon s3 através da DAG. Na primeira etapa foi criado o web scraper "scraper.py", que faz
a raspagem do site da 16º premiação da OBMEP utilizando as bibliotecas Requests e BeautifulSoup, mais especificamente coletando dados dos medalhistas de ouro, prata, bronze e menções honrosas 
das escolas públicas e privadas, concatenando todas as tabelas e convertendo em um arquivo do tipo Parquet comprimido em GZIP ("df_obmep.parquet.gzip") a partir de um Pandas Dataframe.
Já o script "local_to_s3.py", utiliza o s3Hook para permitir acesso ao serviço externo s3 e criar uma função que envia o arquivo para o bucket especificado. Os dois scripts Python
estão disponíveis na pasta "Passo 1" deste repositório.

![politica](https://i.imgur.com/RCBF1ju.png)


2. Na segunda etapa é criada a DAG "s3_ingestion_DAG.py", a qual apresenta dois Dummy Operators para representar o início e o fim do fluxo e dois Python Operators, que executam
as funções importadas dos dois módulos python citados no passo 1.

![dag](https://i.imgur.com/ZCmCXhB.png)

![dag](https://i.imgur.com/HkbUyys.png)

![s3](https://i.imgur.com/liQAeDS.png)


# Configurando o ambiente

### Requerimentos

- Python version 3.9
- Apache Airflow version 2.2.3
- Pandas version 1.1.3


 <br/>

### Instalando as dependencias

```
pip install beautifulsoup4
pip install requests
pip install pandas
```

<br/>
