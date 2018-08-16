import openpyxl
from pymongo import MongoClient
import pymongo


def hard_labor(Collection_name,file_name):
    client = MongoClient()
    DB = client.Mobile_revenue
    Collection = DB[Collection_name]


    file = openpyxl.load_workbook(file_name)
    sheet = file.get_sheet_by_name('Sheet')
    result = Collection.find({'date':{'$exists':True}})
    result = result.sort('date', pymongo.ASCENDING)


    sheet['A1'] = 'Date'
    sheet['B1'] = 'DAU'
    sheet['C1'] = 'DNU'
    sheet['D1'] = 'Revenu'
    sheet['E1'] = 'Paied_players'
    sheet['F1'] = 'New_paid_players'
    sheet['G1'] = 'DOU'
    
    i=2
    for item in result:
        sheet['A'+str(i)]=item['date']
        sheet['B'+str(i)]=item['dau']
        sheet['C'+str(i)]=item['dnu']
        sheet['D'+str(i)]=item['revenue']
        sheet['E'+str(i)]=item['paid_players']
        sheet['F'+str(i)]=item['new_paid_players']
        sheet['G'+str(i)]=item['dou']
        i +=1

    file.save(file_name)

hard_labor('EZ_PZ_RPG','EZ_PZ_RPG.xlsx')
hard_labor('EZ_PZ_RPG_3D','EZ_PZ_RPG_3D.xlsx')
hard_labor('EZ_PZ_RPG_3D_RU','EZ_PZ_RPG_3D_RU.xlsx')
