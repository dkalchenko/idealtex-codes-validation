import openpyxl
from io import BytesIO, StringIO

import re

class CodeValidation:
  regex = r"^\d\d\d\d-\d\d\d[B,C,M]A?$"
  
  def __init__(self, file: BytesIO):
    self.file = file

  def ValidateProducts(self) -> BytesIO:
    productsTables = openpyxl.load_workbook(filename=self.file)
    productsSheet = productsTables.active
    if(productsSheet is None):
        raise Exception("Таблиці нема в файле, давай інший файл!")
    response = ""
    response += self.ValidationCondition()
    for row in productsSheet.iter_rows(min_row=2, max_col=1):
        for cell in row:
          response += self.CheckCode(cell)
    
    return BytesIO(response.encode())
  def ValidationCondition(self) -> str:
     return "Таблиця була перевірина на наступні умови \n Код повинен бути 0000-000(B/C/M - це велика середня чи маленька, повинні бути англиські букви)(A - акційни това чи ні) \n Приклад вірного коду 1234-123В або 1234-123СА \n"

  def CheckCode(self, cell) -> str:
       errMessage = "\n Рядок " + str(cell.row) + " "
       match = re.fullmatch(self.regex, cell.value)
       if(match is None):
          return errMessage + "код " + str(cell.value) + " має невірну структуру."