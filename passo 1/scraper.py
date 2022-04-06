# Import libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd

def scraping_function():
    url = 'http://premiacao.obmep.org.br/16aobmep/verRelatorioPremiadosGeral-AC.1.do.htm'

    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'lxml')
    tables = soup.find_all("table", {"class": "list"})
    headers = []
    for i in tables[0].select('tr:nth-of-type(2)')[0].find_all('th'):
      headers.append(i.text)

    all_data = []

    estados = ['AL', 'AC', 'AM', 'AP', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MG', 'MS', 'MT', 'PA', 'PB', 'PE', 'PI', 'PR', 'RJ', 'RN', 'RO', 'RR', 'RS', 'SC', 'SE', 'SP', 'TO']
    escolas = ['', '.privada']
    niveis = ['1', '2', '3']


    for estado in estados: 
      for escola in escolas: 
        for nivel in niveis: 
          # Create an URL object
          url = 'http://premiacao.obmep.org.br/16aobmep/verRelatorioPremiadosGeral-'+ estado +'.'+ nivel + escola + '.do.htm'
          # Create object page
          page = requests.get(url)

          # parser-lxml = Change html to Python friendly format
          # Obtain page's information
          soup = BeautifulSoup(page.text, 'lxml')

          # Obtain information from tag <table>
          tables = soup.find_all("table", {"class": "list"})


          data_rows = []
          for table in tables:
            for row in table.find_all("tr"):
              data_rows.append(row)
              
          for row in data_rows:
            row_data = []
            for data in row.find_all("td"):
              row_data.append(data.text)
            if(row_data != []):
              all_data.append(row_data)


    # Create a dataframe
    df_obmep = pd.DataFrame([headers] + all_data)
    # with pd.option_context('display.max_rows', None, 'display.max_columns', None, 'display.width', 7):  # more options can be specified also
    df_obmep.columns = df_obmep.columns.astype(str)

    # Converts to Parquet format
    df_obmep.to_parquet('df_obmep.parquet.gzip', compression='gzip')
    pd.read_parquet('df_obmep.parquet.gzip')
