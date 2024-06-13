import xlrd


def readExcel(filepath, sheet):
    Ptm_Mutations = xlrd.open_workbook(filepath)  # filepath:PTM_mutation.xlsx
    sheet = Ptm_Mutations.sheet_by_name(sheet)  # 工作表Sheet1
    rows = sheet.nrows  # 10721条数据
    cols = sheet.ncols  # 22个数据类型

    return sheet, rows, cols


