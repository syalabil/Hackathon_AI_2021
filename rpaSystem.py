import pandas as pd
import rpa as r

def addEquipmentExcel(excel):
    df = pd.read_excel(excel, dtype="str")  
    r.init()
    r.url('http://127.0.0.1:5000/')
    r.wait(10)
    r.type('//*[@name="username"]', 'admin')
    r.type('//*[@name="password"]', 'password123[enter]')
    r.click('//*[@name="equipment"]')
    for i,row in df.iterrows():
        r.click('//*[@name="addequipment"]')
        r.type('//*[@name="name"]', f"{row['Equipment Name']}")
        r.type('//*[@name="price"]', f"{row['Price']}")
        r.type('//*[@name="qty"]', f"{row['Quantity']}"+"[enter]")

    r.close()

def printReciept(product,price):
    r.init(visual_automation = True, chrome_browser = False)
    r.keyboard('[win][e]')
    r.keyboard('[ctrl][l]')
    r.keyboard('C:/Hackathon_2021_AI/Receipt.docx[enter]')
    r.wait()
    r.dclick('ReceiptProduct.PNG')
    r.keyboard(product)
    r.dclick('ReceiptPrice.PNG')
    r.keyboard(price)
    r.keyboard('[f12]')
    r.keyboard('newreciept[enter][enter]')
    r.close()