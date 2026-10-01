# import openpyxl
import os
# from openpyxl.styles import Font
import pandas as pd


def create_Excel_file(data):
    if not data:
        print("No stock data available.")
        return None
    
    current_directory = os.path.dirname(__file__)

    output_path = os.path.join(
        current_directory,
        "..",
        "output",
        "large_cap_stocks.xlsx"
    )
    df = pd.DataFrame(data)
    df.to_excel(output_path, index=False)
    
    return output_path




# workbook=openpyxl.Workbook()

# sheet=workbook.active
# sheet.title="Large_cap_stocks"


# def create_Excel_file(data):
#     if not data:
#         print("No stock data available.")
#         return None
    
#     first_file=True
#     for stock in data:
#         if first_file:
#             headers=list(stock.keys())
#             print(headers)
#             sheet.append(headers)
#             for cell in sheet[1]:
#              cell.font = Font(bold=True)
            
#         sheet.append(list(stock.values()))
#         first_file=False    
    
#     Excel_file= os.path.join('..', 'output', 'large_cap_stocks.xlsx')
#     workbook.save(Excel_file)

#     return Excel_file