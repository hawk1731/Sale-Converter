
import streamlit as st
import pandas as pd
# from datetime import datetime
import os
from PIL import Image
import re 
#from streamlit_ace import st_ace

       

def Amazon_salesreturn_B2B():
    file_path = st.session_state['file_path']
    output_folder = st.session_state['output_folder']

    sales_return_data = pd.read_csv(file_path)
    sales_return_data = sales_return_data[~sales_return_data['Transaction Type'].isin(
        ['Cancel', 'Shipment', 'EInvoiceCancel'])]
    
    
    sales_return_data['Mrp'] = 0
    for index, row in sales_return_data.iterrows():
        TotalTax = (-row['Invoice Amount'])/(-row['Quantity'])
        sales_return_data.at[index, 'Mrp'] = TotalTax
        new_data = pd.DataFrame(sales_return_data['Mrp'])
        new_data.reset_index(drop=True, inplace=True)
    
    sales_return_data['Rate']=0
    for index, row in sales_return_data.iterrows():
        TotalTax=(-row['Tax Exclusive Gross'])/(-row['Quantity'])
        sales_return_data.at[index, 'Rate'] = TotalTax
        new_data = pd.DataFrame(sales_return_data['Rate'])
        new_data.reset_index(drop=True, inplace=True)

    Amazon_Data = sales_return_data.rename(columns={'Sku':'ItemEAN','Warehouse Id':'StoreNo','Mrp':'Mrp','Invoice Number': 'ReceiptNo', 'Credit Note No': 'TransactionNo', 'Seller Gstin': 'SellerGST', 'Invoice Amount': 'Bill Amount', 'Order Id': 'Order Number', 'Credit Note Date': 'Date', 'Rate': 'Rate', 'Quantity': 'Quantity', 'Cgst Rate': 'CGST%',
                                           'Sgst Rate': 'SGST%', 'Igst Rate': 'IGST%', 'Cgst Tax': 'CGSTAmount', 'Sgst Tax': 'SGSTAmount', 'Igst Tax': 'IGSTAmount', 'Item Description': 'ProductName', 'Ship To State': 'State', 'Ship To Postal Code': 'PartyPincode', 'Transaction Type': 'Transaction Type', 'Customer Bill To Gstid': 'GSTIN'})

    column_Data = Amazon_Data['ReceiptNo']
    column = pd.DataFrame(column_Data)

    column_Data = Amazon_Data['TransactionNo']
    column['TransactionNo'] = pd.DataFrame(column_Data)
    
    column_Data = Amazon_Data['StoreNo']
    column['StoreNo'] = pd.DataFrame(column_Data)

    column_Data = Amazon_Data['SellerGST']
    column['SellerGST'] = pd.DataFrame(column_Data)
    column['CustomerName'] = 'Cash'

    column_Data = Amazon_Data['Order Number']
    column['Order Number'] = pd.DataFrame(column_Data)
    column['POSTerminalNo'] = 'Amazon seller services Private Limited'
    column['StaffID'] = ''

    column_Data=Amazon_Data['Date']
    column['Date']=pd.DataFrame(column_Data)
    # column['Date'] = pd.to_datetime(column['Date'], format='%y/%m/%d %H:%M')
    # column['Date'] = column['Date'].dt.strftime('%y/%m/%d')
    
    column['LotNo']='Adhoc'

    column_Data = Amazon_Data['Mrp']
    remove_minus=column_Data/(-1)
    column['Mrp'] = pd.DataFrame(remove_minus)


    column_Data = Amazon_Data['Rate']
    remove_minus=column_Data/(-1)
    column['Rate'] = pd.DataFrame(remove_minus)

    old_column_name = 'Rate'
    old_column_data = column[old_column_name]

    new_column_name = 'BillingRate'
    column[new_column_name] = old_column_data

    column_Data = Amazon_Data['Quantity']
    column['Quantity'] = pd.DataFrame(column_Data)

    column_Data = Amazon_Data['CGST%']
    column_Data = column_Data.replace({0.09: 9, 0.06: 6})
    column['CGST%'] = pd.DataFrame(column_Data)

    column_Data = Amazon_Data['SGST%']
    column_Data = column_Data.replace({0.09: 9, 0.06: 6})
    column['SGST%'] = pd.DataFrame(column_Data)

    column_Data = Amazon_Data['IGST%']
    column_Data = column_Data.replace({0.12: 12, 0.18: 18})
    column['IGST%'] = pd.DataFrame(column_Data)
    column['LINE_SHIPPING_AMT_INCL_TAX'] = ''

    
    column['Amount'] = 0
    for index, row in column.iterrows():
        CGST = row['BillingRate'] * row['Quantity']
        column.at[index, 'Amount'] = CGST
        new_data = pd.DataFrame(column['Amount'])

    column['CGSTAmount'] = 0
    for index, row in column.iterrows():
        CGST = row['BillingRate'] * row['CGST%'] / 100
        column.at[index, 'CGSTAmount'] = CGST
        new_data = pd.DataFrame(column['CGSTAmount'])
        #new_data.reset_index(drop=True, inplace=True)

    column['SGSTAmount'] = 0
    for index, row in column.iterrows():
        CGST = row['BillingRate'] * row['SGST%'] / 100
        column.at[index, 'SGSTAmount'] = CGST
        new_data = pd.DataFrame(column['SGSTAmount'])
        #new_data.reset_index(drop=True, inplace=True)

    column['IGSTAmount'] = 0
    for index, row in column.iterrows():
        CGST = row['BillingRate'] * row['IGST%'] / 100
        column.at[index, 'IGSTAmount'] = CGST
        new_data = pd.DataFrame(column['IGSTAmount'])
        #new_data.reset_index(drop=True, inplace=True)

    column['TotalTax%'] = 0
    for index, row in column.iterrows():
        TotalTax = row['CGST%']+row['SGST%']+row['IGST%']
        column.at[index, 'TotalTax%'] = TotalTax
        new_data = pd.DataFrame(column['TotalTax%'])
        new_data.reset_index(drop=True, inplace=True)

    column['TotalTax'] = 0
    for index, row in column.iterrows():
        TotalTax = row['CGSTAmount']+row['SGSTAmount']+row['IGSTAmount']
        column.at[index, 'TotalTax'] = TotalTax
        new_data = pd.DataFrame(column['TotalTax'])
        new_data.reset_index(drop=True, inplace=True)

    column['LineAmount'] = 0
    for index, row in column.iterrows():
        TotalTax = row['Amount']+row['TotalTax']
        column.at[index, 'LineAmount'] = TotalTax
        new_data = pd.DataFrame(column['LineAmount'])
        new_data.reset_index(drop=True, inplace=True)

    column['LineAmtWithShipping'] = 0
    for index, row in column.iterrows():
        TotalTax = row['Mrp']*row['Quantity']
        column.at[index, 'LineAmtWithShipping'] = TotalTax
        new_data = pd.DataFrame(column['LineAmtWithShipping'])
        new_data.reset_index(drop=True, inplace=True)

    column['LINE_ITEM_DISCAMT_INCL_TAX'] = 0
    for index, row in column.iterrows():
        TotalTax = row['Mrp']*row['Quantity']
        column.at[index, 'LINE_ITEM_DISCAMT_INCL_TAX'] = TotalTax
        new_data = pd.DataFrame(column['LINE_ITEM_DISCAMT_INCL_TAX'])
        new_data.reset_index(drop=True, inplace=True)

    column_Data = Amazon_Data['ProductName']
    column['ProductName'] = pd.DataFrame(column_Data)

    column_Data = Amazon_Data['State']
    column['State'] = pd.DataFrame(column_Data)
    column['Payment Method'] = 'Prepaid'
    column['Shipping Provider Name'] = 'Selfship'

    old_column_name = 'State'
    old_column_data = column[old_column_name]

    new_column_name = 'PartyAddress'
    column[new_column_name] = old_column_data

    column_Data = Amazon_Data['PartyPincode']
    column['PartyPincode'] = pd.DataFrame(column_Data)

    column_Data = Amazon_Data['GSTIN']
    column['GSTIN'] = pd.DataFrame(column_Data)
    column['BillType'] = 'B2B'
    column['Discount'] = 0
    column['DiscountAmount'] = 0
    column['WholeSalesBill'] = 0
    column['Transaction Type'] = 'Sales Return'
    column_Data = Amazon_Data['ItemEAN']
    column['ItemEAN'] = pd.DataFrame(column_Data)
    column['DOCUMENT']=''
    

    output_file_path = f"{output_folder}/Amazon_B2B_Salesreturn.csv"
    
    
    if os.path.exists(output_file_path):
            # File with the same name already exists, add indexing
            index = 1
            while True:
                new_output_file_path = f"{output_folder}/Amazon_B2B_Salesreturn({index}).csv"
                if not os.path.exists(new_output_file_path):
                    output_file_path = new_output_file_path
                    break
                index += 1
    column.to_csv(output_file_path, index=False)

    # Rest of the code...

    column.to_csv(output_file_path, index=False)
    st.success("File processed and saved successfully.")



def Amazon_sales_B2B():
    
    file_path = st.session_state['file_path']
    output_folder = st.session_state['output_folder']

    sales_data = pd.read_csv(file_path)
    
    sales_data = sales_data[~sales_data['Transaction Type'].isin(
            ['Cancel', 'Refund', 'EInvoiceCancel'])]
    
    

    sales_data['Rate']=0
    for index, row in sales_data.iterrows():
        TotalTax=(row['Tax Exclusive Gross'])/(row['Quantity'])
        sales_data.at[index, 'Rate'] = TotalTax
        new_data = pd.DataFrame(sales_data['Rate'])
        new_data.reset_index(drop=True, inplace=True)

    

    Amazon_Data = sales_data.rename(columns={'Sku':'ItemEAN','Warehouse Id':'StoreNo','Invoice Number': 'ReceiptNo', 'Seller Gstin': 'SellerGST', 'Invoice Amount': 'Bill Amount', 'Order Id': 'Order Number', 'Shipment Date': 'Date', 'Rate': 'Rate', 'Quantity': 'Quantity', 'Cgst Rate': 'CGST%',
                                        'Sgst Rate': 'SGST%', 'Igst Rate': 'IGST%', 'Cgst Tax': 'CGSTAmount', 'Sgst Tax': 'SGSTAmount', 'Igst Tax': 'IGSTAmount', 'Item Description': 'ProductName', 'Ship To State': 'State', 'Ship To Postal Code': 'PartyPincode', 'Transaction Type': 'Transaction Type','Customer Bill To Gstid':'GSTIN'})

    column_Data = Amazon_Data['ReceiptNo']
    column = pd.DataFrame(column_Data)

    old_column_name = 'ReceiptNo'
    old_column_data = column[old_column_name]

    new_column_name = 'TransactionNo'
    column[new_column_name] = old_column_data
    column_Data = Amazon_Data['StoreNo']
    column['StoreNo'] = pd.DataFrame(column_Data)

    column_Data = Amazon_Data['SellerGST']
    column['SellerGST'] = pd.DataFrame(column_Data)
    column['CustomerName'] = 'Cash'

    column_Data = Amazon_Data['Bill Amount']
    column['Bill Amount'] = pd.DataFrame(column_Data)

    column_Data = Amazon_Data['Order Number']
    column['Order Number'] = pd.DataFrame(column_Data)
    column['POSTerminalNo'] = 'Amazon seller services Pvt Ltd'
    column['StaffID'] = ' '

    column_Data = Amazon_Data['Date']
    column['Date'] = pd.DataFrame(column_Data)
    

        
    
    column['LotNo'] = 'Adhoc'

    old_column_name = 'Bill Amount'
    old_column_data = column[old_column_name]

    new_column_name = 'MRP'
    column[new_column_name] = old_column_data

    column_Data = Amazon_Data['Rate']
    column['Rate'] = pd.DataFrame(column_Data)

    old_column_name = 'Rate'
    old_column_data = column[old_column_name]

    new_column_name = 'BillingRate'
    column[new_column_name] = old_column_data

    column_Data = Amazon_Data['Quantity']
    column['Quantity'] = pd.DataFrame(column_Data)

    column_Data = pd.Series(Amazon_Data['CGST%'])
    column_Data = column_Data.replace({0.09: 9, 0.06: 6})
    column['CGST%'] = pd.DataFrame(column_Data)

    column_Data = pd.Series(Amazon_Data['SGST%'])
    column_Data = column_Data.replace({0.09: 9, 0.06: 6})
    #column_Data= Amazon_Data['SGST%']
    column['SGST%'] = pd.DataFrame(column_Data)

    column_Data = Amazon_Data['IGST%']
    column_Data = column_Data.replace({0.18: 18, 0.12: 12})
    column['IGST%'] = pd.DataFrame(column_Data)
    column["LINE_SHIPPING_AMT_INCL_TAX"] = 0

    column['Amount'] = 0
    for index, row in column.iterrows():
        CGST = row['BillingRate'] * row['Quantity']
        column.at[index, 'Amount'] = CGST
        new_data = pd.DataFrame(column['Amount'])

    column['CGSTAmount'] = 0
    for index, row in column.iterrows():
        CGST = row['Amount'] * row['CGST%'] / 100
        column.at[index, 'CGSTAmount'] = CGST
        new_data = pd.DataFrame(column['CGSTAmount'])
        #new_data.reset_index(drop=True, inplace=True)

    column['SGSTAmount'] = 0
    for index, row in column.iterrows():
        CGST = row['Amount'] * row['SGST%'] / 100
        column.at[index, 'SGSTAmount'] = CGST
        new_data = pd.DataFrame(column['SGSTAmount'])
        #new_data.reset_index(drop=True, inplace=True)

    column['IGSTAmount'] = 0
    for index, row in column.iterrows():
        CGST = row['Amount'] * row['IGST%'] / 100
        column.at[index, 'IGSTAmount'] = CGST
        new_data = pd.DataFrame(column['IGSTAmount'])
        new_data.reset_index(drop=True, inplace=True)

    column['TotalTax%'] = 0
    for index, row in column.iterrows():
        TotalTax = row['CGST%']+row['SGST%']+row['IGST%']
        column.at[index, 'TotalTax%'] = TotalTax
        new_data = pd.DataFrame(column['TotalTax%'])
        new_data.reset_index(drop=True, inplace=True)

    column['TotalTax'] = 0
    for index, row in column.iterrows():
        TotalTax = row['CGSTAmount']+row['SGSTAmount']+row['IGSTAmount']
        column.at[index, 'TotalTax'] = TotalTax
        new_data = pd.DataFrame(column['TotalTax'])
        new_data.reset_index(drop=True, inplace=True)

    column['LineAmount'] = 0
    for index, row in column.iterrows():
        TotalTax = row['Amount']+row['TotalTax']
        column.at[index, 'LineAmount'] = TotalTax
        new_data = pd.DataFrame(column['LineAmount'])
        new_data.reset_index(drop=True, inplace=True)

    

    old_column_name = 'LineAmount'
    old_column_data = column[old_column_name]

    new_column_name = 'LineAmtWithShipping'
    column[new_column_name] = old_column_data

    old_column_name = 'LineAmtWithShipping'
    old_column_data = column[old_column_name]

    new_column_name = 'LINE_ITEM_INCL_TAX'
    column[new_column_name] = old_column_data

    column_Data = Amazon_Data['ProductName']
    column['ProductName'] = pd.DataFrame(column_Data)

    column_Data = Amazon_Data['State']
    column['State'] = pd.DataFrame(column_Data)

    column['Payment Method'] = 'Credit'
    column['Shipping Provider Name'] = 'Selfship'

    column_Data = Amazon_Data['ItemEAN']
    column['ItemEAN'] = pd.DataFrame(column_Data)
    column['DOCUMENT_EASYCOM_INVOICE']=''

    old_column_name = 'State'
    old_column_data = column[old_column_name]

    new_column_name = 'PartyAddress'
    column[new_column_name] = old_column_data

    column_Data = Amazon_Data['PartyPincode']
    column['PartyPincode'] = pd.DataFrame(column_Data)

    column_Data = Amazon_Data['GSTIN']
    column['GSTIN'] = pd.DataFrame(column_Data)
    column['BillType'] = 'B2B'
    
    column['DiscountAmount'] = 0
    column['WholeSaleBill'] = 1
    

    
        # Save the modified DataFrame as a new CSV file

    output_file_path = f"{output_folder}/Amazon_B2B_Sales.csv"

    if os.path.exists(output_file_path):
        # File with the same name already exists, add indexing
        index = 1
        while True:
            new_output_file_path = f"{output_folder}/Amazon_B2B_Sales({index}).csv"
            if not os.path.exists(new_output_file_path):
                output_file_path = new_output_file_path
                break
            index += 1

   



   

    column.to_csv(output_file_path, index=False)
    st.success("File processed and saved successfully.")



def Amazon_sales_B2C():
    file_path = st.session_state['file_path']
    output_folder = st.session_state['output_folder']

    sales_B2C = pd.read_csv(file_path)
    sales_B2C = sales_B2C[~sales_B2C['Quantity'].isin([0])]

    
    sales_B2C['Rate']=0
    for index, row in sales_B2C.iterrows():
        TotalTax=(row['Tax Exclusive Gross'])/(row['Quantity'])
        sales_B2C.at[index, 'Rate'] = TotalTax
        new_data = pd.DataFrame(sales_B2C['Rate'])
        new_data.reset_index(drop=True, inplace=True)

  

    sales_B2C = sales_B2C[~sales_B2C['Transaction Type'].isin(['Cancel', 'Refund', 'FreeReplacement'])]
    Amazon_Data = sales_B2C.rename(columns={'Sku':'ItemEAN','Warehouse Id':'StoreNo','Invoice Number': 'ReceiptNo', 'Seller Gstin': 'SellerGST', 'Invoice Amount': 'Bill Amount', 'Order Id': 'Order Number', 'Shipment Date': 'Date', 'Rate': 'Rate', 'Quantity': 'Quantity', 'Cgst Rate': 'CGST%',
                                        'Sgst Rate': 'SGST%', 'Igst Rate': 'IGST%', 'Cgst Tax': 'CGSTAmount', 'Sgst Tax': 'SGSTAmount', 'Igst Tax': 'IGSTAmount', 'Item Description': 'ProductName', 'Ship To State': 'State', 'Ship To Postal Code': 'PartyPincode', 'Transaction Type': 'Transaction Type'})
    
    column_Data = Amazon_Data['ReceiptNo']
    column = pd.DataFrame(column_Data)

    
    old_column_name = 'ReceiptNo'
    old_column_data = column[old_column_name]

    new_column_name = 'TransactionNo'
    column[new_column_name] = old_column_data



    column_Data = Amazon_Data['StoreNo']
    column['StoreNo'] = pd.DataFrame(column_Data)

    column_Data = Amazon_Data['SellerGST']
    column['SellerGST'] = pd.DataFrame(column_Data)
    column['CustomerName'] = 'Cash'

    column_Data = Amazon_Data['Bill Amount']
    column['Bill Amount'] = pd.DataFrame(column_Data)

    column_Data = Amazon_Data['Order Number']
    column['Order Number'] = pd.DataFrame(column_Data)
    column['POSTerminalNo'] = 'Amazon seller services Pvt Ltd'
    column['StaffID'] = ' '

    column_Data = Amazon_Data['Date']
    column['Date'] = pd.DataFrame(column_Data)
    column['LotNo'] = 'adhoc'

    old_column_name = 'Bill Amount'
    old_column_data = column[old_column_name]

    new_column_name = 'MRP'
    column[new_column_name] = old_column_data

    
    column_Data = Amazon_Data['Rate']
    column['Rate'] = pd.DataFrame(column_Data)
    

    old_column_name = 'Rate'
    old_column_data = column[old_column_name]

    new_column_name = 'BillingRate'
    column[new_column_name] = old_column_data

    column_Data = Amazon_Data['Quantity']
    column['Quantity'] = pd.DataFrame(column_Data)

    column_Data = pd.Series(Amazon_Data['CGST%'])
    column_Data = column_Data.replace({0.09: 9, 0.06: 6})
    column['CGST%'] = pd.DataFrame(column_Data)

    column_Data = pd.Series(Amazon_Data['SGST%'])
    column_Data = column_Data.replace({0.09: 9, 0.06: 6})
    column['SGST%'] = pd.DataFrame(column_Data)

    column_Data = Amazon_Data['IGST%']
    column_Data = column_Data.replace({0.18: 18, 0.12: 12})
    column['IGST%'] = pd.DataFrame(column_Data)
    column["LINE_SHIPPING_AMT_INCL_TAX"] = ''

    column['Amount']=0
    for index, row in column.iterrows():
        TotalTax=row['BillingRate']*row['Quantity']
        column.at[index, 'Amount'] = TotalTax
        new_data = pd.DataFrame(column['Amount'])
        new_data.reset_index(drop=True, inplace=True)

    column['CGSTAmount'] = 0
    for index, row in column.iterrows():
        CGST = row['Amount'] * row['CGST%'] / 100
        column.at[index, 'CGSTAmount'] = CGST
        new_data = pd.DataFrame(column['CGSTAmount'])

    column['SGSTAmount'] = 0
    for index, row in column.iterrows():
        CGST = row['Amount'] * row['SGST%'] / 100
        column.at[index, 'SGSTAmount'] = CGST
        new_data = pd.DataFrame(column['SGSTAmount'])

    
    column['IGSTAmount'] = 0
    for index, row in column.iterrows():
        CGST = row['Amount'] * row['IGST%'] / 100
        column.at[index, 'IGSTAmount'] = CGST
        new_data = pd.DataFrame(column['IGSTAmount'])

    column['TotalTax%'] = 0
    for index, row in column.iterrows():
        TotalTax = row['CGST%']+row['SGST%']+row['IGST%']
        column.at[index, 'TotalTax%'] = TotalTax
        new_data = pd.DataFrame(column['TotalTax%'])

    column['TotalTax'] = 0
    for index, row in column.iterrows():
        TotalTax = row['CGSTAmount']+row['SGSTAmount']+row['IGSTAmount']
        column.at[index, 'TotalTax'] = TotalTax
        new_data = pd.DataFrame(column['TotalTax'])
        #new_data.reset_index(drop=True, inplace=True)

    column['LineAmount'] = 0
    for index, row in column.iterrows():
        TotalTax = row['Amount']+row['TotalTax']
        column.at[index, 'LineAmount'] = TotalTax
        new_data = pd.DataFrame(column['LineAmount'])
        new_data.reset_index(drop=True, inplace=True)

    old_column_name = 'LineAmount'
    old_column_data = column[old_column_name]

    new_column_name = 'LineAmtWithShipping'
    column[new_column_name] = old_column_data

    old_column_name = 'LineAmtWithShipping'
    old_column_data = column[old_column_name]

    new_column_name = 'LINE_ITEM_INCL_TAX'
    column[new_column_name] = old_column_data

    column_Data = Amazon_Data['ProductName']
    column['ProductName'] = pd.DataFrame(column_Data)

    column_Data = Amazon_Data['State']
    column['State'] = pd.DataFrame(column_Data)
    column['Payment Method'] = 'PrePaid'
    column['Shipping Provider Name'] = 'Selfship'
    
    column_Data = Amazon_Data['ItemEAN']
    column['ItemEAN'] = pd.DataFrame(column_Data)
    column['DOCUMENT']=''

    # sales_return_B2C = sales_B2C[~sales_B2C['Transaction Type'].isin(['Cancel', 'Shipment', 'FreeReplacement'])]
    # sales_return_B2C = sales_B2C[~sales_B2C['Quantity'].isin([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20])]
    # Amazon_Data1 = sales_return_B2C.rename(columns={'Total Tax Amount':'TotalTax','Credit Note Date':'Date','Invoice Amount':'Bill Amount','Credit Note No':'ReceiptNo','Sku':'ItemEAN','Warehouse Id':'StoreNo','Invoice Number': 'TransactionNo', 'Seller Gstin': 'SellerGST', 'Invoice Amount': 'Bill Amount', 'Order Id': 'Order Number',  'Tax Exclusive Gross': 'Rate', 'Quantity': 'Quantity', 'Cgst Rate': 'CGST%',
    #                                     'Sgst Rate': 'SGST%', 'Igst Rate': 'IGST%', 'Shipping Cgst Tax': 'CGSTAmount', 'Shipping Sgst Tax': 'SGSTAmount', 'Shipping Igst Tax': 'IGSTAmount', 'Item Description': 'ProductName', 'Ship To State': 'State', 'Ship To Postal Code': 'PartyPincode', 'Transaction Type': 'Transaction Type'})
    
    # Amazon=Amazon_Data1['Transaction Type'].replace('Refund','Shipment')
    # column_Data = Amazon_Data1['ReceiptNo']
    # column1 = pd.DataFrame(column_Data)

    # column_Data = Amazon_Data1['TransactionNo']
    # column1['TransactionNo'] = pd.DataFrame(column_Data)

    # column_Data = Amazon_Data1['StoreNo']
    # column1['StoreNo'] = pd.DataFrame(column_Data)

    # column_Data = Amazon_Data['SellerGST']
    # column1['SellerGST'] = pd.DataFrame(column_Data)
    # column1['CustomerName']='Cash'

    # column_Data = Amazon_Data['Bill Amount']
    # column1['Bill Amount'] = pd.DataFrame(column_Data)
    # column_Data = Amazon_Data['Order Number']
    # column1['Order Number'] = pd.DataFrame(column_Data)
    # column1['POSTerminalNo']='Amazon seller services Pvt Ltd'
    # column1['StaffID']=''

    # column_Data = Amazon_Data['Date']
    # column1['Date'] = pd.DataFrame(column_Data)
    # column1['LotNo']='adhoc'
    # column1['Mrp']=''

    # column_Data = Amazon_Data['Rate']
    # column1['Rate'] = pd.DataFrame(column_Data)

    # old_column_name = 'Rate'
    # old_column_data = column1[old_column_name]
    
    # new_column_name = 'BillingRate'
    # column1[new_column_name] = old_column_data


    # column_Data = Amazon_Data['Quantity']
    # column1['Quantity'] = pd.DataFrame(column_Data)
    # column1['CGST%']=0
    # column1['SGST%']=0
    # column1['IGST%']=0
    # column1['LINE_SHIPPING_AMT_INCL_TAX']=0

    # old_column_name = 'BillingRate'
    # old_column_data = column1[old_column_name]
    
    # new_column_name = 'Amount'
    # column1[new_column_name] = old_column_data

    # column_Data = Amazon_Data['CGSTAmount']
    # column1['CGSTAmount'] = pd.DataFrame(column_Data)

    # column_Data = Amazon_Data['SGSTAmount']
    # column1['SGSTAmount'] = pd.DataFrame(column_Data)


    # column_Data = Amazon_Data['IGSTAmount']
    # column1['IGSTAmount'] = pd.DataFrame(column_Data)
    # column1['TotalTax%']='0'


    # column_Data = Amazon_Data['TotalTax']
    # column1['TotalTax'] = pd.DataFrame(column_Data)


    # old_column_name = 'Bill Amount'
    # old_column_data = column1[old_column_name]
    
    # new_column_name = 'LineAmount'
    # column1[new_column_name] = old_column_data

    # old_column_name = 'LineAmount'
    # old_column_data = column1[old_column_name]
    
    # new_column_name = 'LineAmtWithShipping'
    # column1[new_column_name] = old_column_data

    # old_column_name = 'LineAmtWithShipping'
    # old_column_data = column1[old_column_name]
    
    # new_column_name = 'LINE_ITEM_INCL_TAX'
    # column1[new_column_name] = old_column_data

    # column_Data = Amazon_Data['ProductName']
    # column1['ProductName'] = pd.DataFrame(column_Data)

    # column_Data = Amazon_Data['State']
    # column1['State'] = pd.DataFrame(column_Data)
    # column1['Payment Method']='PrePaid'
    # column1['Shipping Provider Name']='Selfship'

    # column_Data = Amazon_Data['ItemEAN']
    # column1['ItemEAN'] = pd.DataFrame(column_Data)
    # column1['DOCUMENT']=''

    # merged_df=pd.concat([column,column1],axis=0)



    output_file_path = f"{output_folder}/Amazon_B2C_Sales.csv"
    if os.path.exists(output_file_path):
        # File with the same name already exists, add indexing
        index = 1
        while True:
            new_output_file_path = f"{output_folder}/Amazon_B2C_Sales({index}).csv"
            if not os.path.exists(new_output_file_path):
                output_file_path = new_output_file_path
                break
            index += 1
    
    column.to_csv(output_file_path, index=False)
    st.success("File processed and saved successfully.")

def Amazon_salesreturn_B2C():
    file_path = st.session_state['file_path']
    output_folder = st.session_state['output_folder']

    sales_return_B2C = pd.read_csv(file_path)
    sales_return_B2C = sales_return_B2C[~sales_return_B2C['Quantity'].isin([0])]

    sales_return_B2C['Rate']=0
    for index, row in sales_return_B2C.iterrows():
        TotalTax=(row['Tax Exclusive Gross'])/(row['Quantity'])
        sales_return_B2C.at[index, 'Rate'] = TotalTax
        new_data = pd.DataFrame(sales_return_B2C['Rate'])
        new_data.reset_index(drop=True, inplace=True)

    sales_return_B2C = sales_return_B2C[~sales_return_B2C['Transaction Type'].isin(['Cancel', 'Shipment', 'FreeReplacement'])]
    Amazon_Data = sales_return_B2C.rename(columns={'Warehouse Id':'StoreNo','Sku':'ItemEAN','Rate':'Rate','Credit Note No': 'ReceiptNo','Order Id':'TransactionNo','Seller Gstin': 'SellerGST', 'Invoice Amount': 'Mrp', 'Shipment Date': 'Date','Quantity': 'Quantity', 'Cgst Rate': 'CGST%',
                                        'Sgst Rate': 'SGST%', 'Igst Rate': 'IGST%', 'Cgst Tax': 'CGSTAmount', 'Sgst Tax': 'SGSTAmount', 'Igst Tax': 'IGSTAmount', 'Item Description': 'ProductName', 'Ship To State': 'State', 'Ship To Postal Code': 'PartyPincode', 'Transaction Type': 'Transaction Type'})
    
    column_Data = Amazon_Data['ReceiptNo']
    column = pd.DataFrame(column_Data)

    column_Data=Amazon_Data['TransactionNo']
    column['TransactionNo']=pd.DataFrame(column_Data)
    
    
    column_Data = Amazon_Data['StoreNo']
    column['StoreNo'] = pd.DataFrame(column_Data)
    

    column_Data=Amazon_Data['SellerGST']
    column['SellerGST']=pd.DataFrame(column_Data)
    column['CustomerName']='CASH'

    old_column_name = 'TransactionNo'
    old_column_data = column[old_column_name]
    new_column_name = 'Order Number'
    column[new_column_name] = old_column_data
    column['POSTerminalNo']='AMAZON SELLER SERVICES PRIVATE LIMITED'
    column['StaffID']=''

    
    column_Data=Amazon_Data['Date']
    column['Date']=pd.DataFrame(column_Data)
    # column['Date'] = pd.to_datetime(column['Date'], format='%y/%m/%d %H:%M')
    # column['Date'] = column['Date'].dt.strftime('%y/%m/%d')
    
    column['LotNo']='adhoc'

    column_Data = Amazon_Data['Mrp']
    remove_minus=column_Data/(-1)
    column['Mrp'] = pd.DataFrame(remove_minus)

    column_Data=Amazon_Data['Rate']
    remove_minus=column_Data/(-1)
    column['Rate']=pd.DataFrame(remove_minus)

    old_column_name = 'Rate'
    old_column_data = column[old_column_name]
    new_column_name = 'BillingRate'
    column[new_column_name] = old_column_data

    column_Data=Amazon_Data['Quantity']
    column['Quantity']=pd.DataFrame(column_Data)

    column_Data=Amazon_Data['CGST%']
    column_Data = column_Data.replace({0.09: 9,0.06: 6})
    column['CGST%']=pd.DataFrame(column_Data)

    column_Data=Amazon_Data['SGST%']
    column_Data = column_Data.replace({0.09: 9,0.06: 6})
    column['SGST%']=pd.DataFrame(column_Data)

    column_Data=Amazon_Data['IGST%']
    column_Data = column_Data.replace({0.12: 12,0.18: 18})
    column['IGST%']=pd.DataFrame(column_Data)
    column['LINE_SHIPPING_AMT_INCL_TAX']=''

    column['Amount']=0
    for index, row in column.iterrows():
        TotalTax=(-row['BillingRate'])*(-row['Quantity'])
        column.at[index, 'Amount'] = TotalTax
        new_data = pd.DataFrame(column['Amount'])
        new_data.reset_index(drop=True, inplace=True)

    column['CGSTAmount'] = 0 
    for index, row in column.iterrows():
        CGST = row['BillingRate'] * row['CGST%'] / 100
        column.at[index, 'CGSTAmount'] = CGST
        new_data = pd.DataFrame(column['CGSTAmount'])
        #new_data.reset_index(drop=True, inplace=True)

    column['SGSTAmount'] = 0 
    for index, row in column.iterrows():
        CGST = row['BillingRate'] * row['SGST%'] / 100
        column.at[index, 'SGSTAmount'] = CGST
        new_data = pd.DataFrame(column['SGSTAmount'])
        #new_data.reset_index(drop=True, inplace=True)

    column['IGSTAmount'] = 0 
    for index, row in column.iterrows():
        CGST = row['BillingRate'] * row['IGST%'] / 100
        column.at[index, 'IGSTAmount'] = CGST
        new_data = pd.DataFrame(column['IGSTAmount'])
        #new_data.reset_index(drop=True, inplace=True)

    column['TotalTax%']=0
    for index, row in column.iterrows():
        TotalTax=row['CGST%']+row['SGST%']+row['IGST%']
        column.at[index, 'TotalTax%'] = TotalTax
        new_data = pd.DataFrame(column['TotalTax%'])
        new_data.reset_index(drop=True, inplace=True)   
        
    column['TotalTax']=0
    for index, row in column.iterrows():
        TotalTax=row['CGSTAmount']+row['SGSTAmount']+row['IGSTAmount']
        column.at[index, 'TotalTax'] = TotalTax
        new_data = pd.DataFrame(column['TotalTax'])
        new_data.reset_index(drop=True, inplace=True) 

    column['LineAmount']=0
    for index, row in column.iterrows():
        TotalTax=row['Amount']+row['TotalTax']
        column.at[index, 'LineAmount'] = TotalTax
        new_data = pd.DataFrame(column['LineAmount'])
        new_data.reset_index(drop=True, inplace=True)

    column['LineAmtWithShipping']=0
    for index, row in column.iterrows():
        TotalTax=row['Amount']+row['TotalTax']
        column.at[index, 'LineAmtWithShipping'] = TotalTax
        new_data = pd.DataFrame(column['LineAmtWithShipping'])
        new_data.reset_index(drop=True, inplace=True)

    
    column['LINE_ITEM_DISCAMT_INCL_TAX']=0
    for index, row in column.iterrows():
        TotalTax=row['Amount']+row['TotalTax']
        column.at[index, 'LINE_ITEM_DISCAMT_INCL_TAX'] = TotalTax
        new_data = pd.DataFrame(column['LINE_ITEM_DISCAMT_INCL_TAX'])
        new_data.reset_index(drop=True, inplace=True)

    column_Data=Amazon_Data['ProductName']
    column['ProductName']=pd.DataFrame(column_Data)

    column_Data=Amazon_Data['State']
    column['State']=pd.DataFrame(column_Data)
    column['Payment Mode']='PrePaid'
    column['Shipping Provide Name']='SelfShip'
    
    column_Data = Amazon_Data['ItemEAN']
    column['ItemEAN'] = pd.DataFrame(column_Data)
    column['DOCUMENT']=''

    output_file_path = f"{output_folder}/Amazon_sales_return_B2C.csv"
    
    if os.path.exists(output_file_path):
        # File with the same name already exists, add indexing
        index = 1
        while True:
            new_output_file_path = f"{output_folder}/Amazon_salesreturn_B2C({index}).csv"
            if not os.path.exists(new_output_file_path):
                output_file_path = new_output_file_path
                break
            index += 1
    column.to_csv(output_file_path, index=False)
    st.success("File processed and saved successfully.")


def flipkart_sale():
    file_path = st.session_state['file_path']
    output_folder = st.session_state['output_folder']

    sales = pd.read_excel(file_path,sheet_name='Sales Report')
    sales = sales[~sales['Event Sub Type'].isin(['Cancellation','Return'])]

    sales['Event Sub Type']=sales['Event Sub Type'].replace('Return Cancellation', 'Sale')
    import re

    def remove_special_characters(text):
        pattern = r'[^a-zA-Z0-9\s]'
        cleaned_text = re.sub(pattern, '', text)
        return cleaned_text
    sales['Product Title/Description']=sales['Product Title/Description'].apply(remove_special_characters)


    sales['Rate'] = 0
    for index, row in sales.iterrows():
        TotalRate = (row['Taxable Value (Final Invoice Amount -Taxes)'])/(row['Item Quantity'])
        sales.at[index, 'Rate'] = TotalRate
        new_data = pd.DataFrame(sales['Rate'])
        new_data.reset_index(drop=True, inplace=True)

    sales['TotalTax%'] = 0
    for index, row in sales.iterrows():
        TotalRate = (row['CGST Rate']+row['SGST Rate (or UTGST as applicable)']+row['IGST Rate'])
        sales.at[index, 'TotalTax%'] = TotalRate
        new_data = pd.DataFrame(sales['TotalTax%'])
        new_data.reset_index(drop=True, inplace=True)

    sales['TotalTax'] = 0
    for index, row in sales.iterrows():
        TotalRate = (row['Taxable Value (Final Invoice Amount -Taxes)']*row['TotalTax%'])/100
        sales.at[index, 'TotalTax'] = TotalRate
        new_data = pd.DataFrame(sales['TotalTax'])
        new_data.reset_index(drop=True, inplace=True)

    sales['mrp'] = 0
    for index, row in sales.iterrows():
        TotalRate = row['Taxable Value (Final Invoice Amount -Taxes)']+row['TotalTax']
        sales.at[index, 'mrp'] = TotalRate
        new_data = pd.DataFrame(sales['mrp'])
        new_data.reset_index(drop=True, inplace=True)

    flipkart_Data = sales.rename(columns={'Buyer Invoice ID':'ReceiptNo','Seller GSTIN':'SellerGST','Order ID':'Order Number','Buyer Invoice Date':'Date','Rate':'Rate','Item Quantity':'Quantity','CGST Rate':'CGST%','SGST Rate (or UTGST as applicable)':'SGST%','IGST Rate':'IGST%','Product Title/Description':'ProductName',"Customer's Billing State":"State",'mrp':'Billing Amount','Order Shipped From (State)':'StoreNo','SKU':'ItemEAN'})

    column_Data = flipkart_Data['ReceiptNo']
    column = pd.DataFrame(column_Data)

    old_column_name = 'ReceiptNo'
    old_column_data = column[old_column_name]
    
    new_column_name = 'TransactionNo'
    column[new_column_name] = old_column_data
    
    column_Data = flipkart_Data['StoreNo']
    column['StoreNo'] = pd.DataFrame(column_Data)
    

    column_Data = flipkart_Data['SellerGST']
    column['SellerGST'] = pd.DataFrame(column_Data)
    column['CustomerName']='Cash'
    column_Data = flipkart_Data['Billing Amount']
    column['Billing Amount'] = pd.DataFrame(column_Data)

    column_Data = flipkart_Data['Order Number']
    column['Order Number'] = pd.DataFrame(column_Data)
    column['PostTerminal']='Flipkart Seller Pvt Ltd'
    column['StaffID']=''

    column_Data = flipkart_Data['Date']
    column['Date'] = pd.DataFrame(column_Data)
    
    column['LotNo']="Adhoc"
    
    old_column_name = 'Billing Amount'
    old_column_data = column[old_column_name]
    
    new_column_name = 'Mrp'
    column[new_column_name] = old_column_data

    column_Data = flipkart_Data['Rate']
    column['Rate'] = pd.DataFrame(column_Data)

    old_column_name = 'Rate'
    old_column_data = column[old_column_name]
    
    new_column_name = 'BillingRate'
    column[new_column_name] = old_column_data

    column_Data = flipkart_Data['Quantity']
    column['Quantity'] = pd.DataFrame(column_Data)

    column_Data = flipkart_Data['CGST%']
    column['CGST%'] = pd.DataFrame(column_Data)

    column_Data = flipkart_Data['SGST%']
    column['SGST%'] = pd.DataFrame(column_Data)

    column_Data = flipkart_Data['IGST%']
    column['IGST%'] = pd.DataFrame(column_Data)
    column['LINE_SHIPPING_AMT_INCL_TAX']=''

    column['Amount'] = 0
    for index, row in column.iterrows():
        CGST = row['BillingRate'] * row['Quantity']
        column.at[index, 'Amount'] = CGST
        new_data = pd.DataFrame(column['Amount'])

    column['CGSTAmount'] = 0
    for index, row in column.iterrows():
        CGST = row['Amount'] * row['CGST%'] / 100
        column.at[index, 'CGSTAmount'] = CGST
        new_data = pd.DataFrame(column['CGSTAmount'])

    column['SGSTAmount'] = 0
    for index, row in column.iterrows():
        CGST = row['Amount'] * row['SGST%'] / 100
        column.at[index, 'SGSTAmount'] = CGST
        new_data = pd.DataFrame(column['SGSTAmount'])

    column['IGSTAmount'] = 0
    for index, row in column.iterrows():
        CGST = row['Amount'] * row['IGST%'] / 100
        column.at[index, 'IGSTAmount'] = CGST
        new_data = pd.DataFrame(column['IGSTAmount'])

    column['TotalTax%'] = 0
    for index, row in column.iterrows():
        TotalTax = row['CGST%']+row['SGST%']+row['IGST%']
        column.at[index, 'TotalTax%'] = TotalTax
        new_data = pd.DataFrame(column['TotalTax%'])

    column['TotalTax'] = 0
    for index, row in column.iterrows():
        TotalTax = row['CGSTAmount']+row['SGSTAmount']+row['IGSTAmount']
        column.at[index, 'TotalTax'] = TotalTax
        new_data = pd.DataFrame(column['TotalTax'])

    column['LineAmount'] = 0
    for index, row in column.iterrows():
        TotalTax = row['Amount']+row['TotalTax']
        column.at[index, 'LineAmount'] = TotalTax
        new_data = pd.DataFrame(column['LineAmount'])
        new_data.reset_index(drop=True, inplace=True)

    column['LineAmtWithShipping'] = 0
    for index, row in column.iterrows():
        TotalTax = row['Amount']+row['TotalTax']
        column.at[index, 'LineAmtWithShipping'] = TotalTax
        new_data = pd.DataFrame(column['LineAmtWithShipping'])
        new_data.reset_index(drop=True, inplace=True)

    column['LINE_ITEM_AMT_INCL_TAX'] = 0
    for index, row in column.iterrows():
        TotalTax = row['Amount']+row['TotalTax']
        column.at[index, 'LINE_ITEM_AMT_INCL_TAX'] = TotalTax
        new_data = pd.DataFrame(column['LINE_ITEM_AMT_INCL_TAX'])
        new_data.reset_index(drop=True, inplace=True)

    column['LINE_ITEM_DISCAMT_INCL_TAX'] = 0
    for index, row in column.iterrows():
        TotalTax = row['Amount']+row['TotalTax']
        column.at[index, 'LINE_ITEM_DISCAMT_INCL_TAX'] = TotalTax
        new_data = pd.DataFrame(column['LINE_ITEM_DISCAMT_INCL_TAX'])
        new_data.reset_index(drop=True, inplace=True)

    column_Data = flipkart_Data['ProductName']
    column['ProductName'] = pd.DataFrame(column_Data)

    column_Data = flipkart_Data['State']
    column['State'] = pd.DataFrame(column_Data)
    column['Payment Method']='Prepaid'
    column['Shipping Provider Name']='Selfship'

    column_Data = flipkart_Data['ItemEAN']
    column['ItemEAN'] = pd.DataFrame(column_Data)

    
    def extract_sku(text):
        pattern = r'\bSKU:([\w\s]+)\b'
        match = re.search(pattern, text)
        if match:
            return match.group(1)
        else:
            return ''
    column['ItemEAN'] = column['ItemEAN'].apply(extract_sku)
    column['DOCUMENT']=''

    output_file_path = f"{output_folder}/flipkart_sales.csv"

    if os.path.exists(output_file_path):
        # File with the same name already exists, add indexing
        index = 1
        while True:
            new_output_file_path = f"{output_folder}/flipkart_sales({index}).csv"
            if not os.path.exists(new_output_file_path):
                output_file_path = new_output_file_path
                break
            index += 1
    column.to_csv(output_file_path, index=False)
    st.success("File processed and saved successfully.")


def flipkart_salesreturn():
    file_path = st.session_state['file_path']
    output_folder = st.session_state['output_folder']

    sales_return = pd.read_excel(file_path,sheet_name='Sales Report')
    sales_return = sales_return[~sales_return['Event Sub Type'].isin(['Cancellation','Return Cancellation','Sale'])]
    def remove_special_characters(text):
        pattern = r'[^a-zA-Z0-9\s]'
        cleaned_text = re.sub(pattern, '', text)
        return cleaned_text
    sales_return['Product Title/Description']=sales_return['Product Title/Description'].apply(remove_special_characters)

    sales_return['Rate'] = 0
    for index, row in sales_return.iterrows():
        TotalRate = (row['Taxable Value (Final Invoice Amount -Taxes)'])/(row['Item Quantity'])
        sales_return.at[index, 'Rate'] = TotalRate
        new_data = pd.DataFrame(sales_return['Rate'])
        new_data.reset_index(drop=True, inplace=True)
    
    sales_return['TotalTax%'] = 0
    for index, row in sales_return.iterrows():
        TotalRate = (row['CGST Rate']+row['SGST Rate (or UTGST as applicable)']+row['IGST Rate'])
        sales_return.at[index, 'TotalTax%'] = TotalRate
        new_data = pd.DataFrame(sales_return['TotalTax%'])
        new_data.reset_index(drop=True, inplace=True)

    sales_return['TotalTax'] = 0
    for index, row in sales_return.iterrows():
        TotalRate = (row['Taxable Value (Final Invoice Amount -Taxes)']*row['TotalTax%'])/100
        sales_return.at[index, 'TotalTax'] = TotalRate
        new_data = pd.DataFrame(sales_return['TotalTax'])
        new_data.reset_index(drop=True, inplace=True)

    sales_return['mrp'] = 0
    for index, row in sales_return.iterrows():
        TotalRate = row['Taxable Value (Final Invoice Amount -Taxes)']+row['TotalTax']
        sales_return.at[index, 'mrp'] = TotalRate
        new_data = pd.DataFrame(sales_return['mrp'])
        new_data.reset_index(drop=True, inplace=True)

    flipkart_Data = sales_return.rename(columns={'SKU':'ItemEAN','Order Shipped From (State)':'StoreNo','Buyer Invoice ID':'ReceiptNo','Seller GSTIN':'SellerGST','Order ID':'Order Number','Buyer Invoice Date':'Date','Rate':'Rate','Item Quantity':'Quantity','CGST Rate':'CGST%','SGST Rate (or UTGST as applicable)':'SGST%','IGST Rate':'IGST%','Product Title/Description':'ProductName',"Customer's Billing State":"State",'BillingAmount':'Billing Amount','mrp':'Mrp'})

    column_Data = flipkart_Data['ReceiptNo']
    column = pd.DataFrame(column_Data)

    old_column_name = 'ReceiptNo'
    old_column_data = column[old_column_name]
    
    new_column_name = 'TransactionNo'
    column[new_column_name] = old_column_data
    column_Data = flipkart_Data['StoreNo']
    column['StoreNo'] = pd.DataFrame(column_Data)
    

    column_Data = flipkart_Data['SellerGST']
    column['SellerGST'] = pd.DataFrame(column_Data)
    column['CustomerName']='Cash'

    column['Billing Amount'] = 0
    for index, row in flipkart_Data.iterrows():
        TotalRate = row['Rate']*(-row['Quantity'])
        column.at[index, 'Billing Amount'] = TotalRate
        new_data = pd.DataFrame(column['Billing Amount'])
        new_data.reset_index(drop=True, inplace=True)

    column_Data = flipkart_Data['Order Number']
    column['Order Number'] = pd.DataFrame(column_Data)
    column['PostTerminal']='Flipkart Seller Pvt Ltd'
    column['StaffID']=''

    column_Data = flipkart_Data['Date']
    column['Date'] = pd.DataFrame(column_Data)
    column['LotNo']="Adhoc"
    
    column_Data = flipkart_Data['Mrp']
    remove_minus= column_Data/(-1)
    column['Mrp'] = pd.DataFrame(remove_minus)

    column_Data = flipkart_Data['Rate']
    remove_minus=column_Data/(-1)
    column['Rate'] = pd.DataFrame(remove_minus)

    old_column_name = 'Rate'
    old_column_data = column[old_column_name]
    
    new_column_name = 'BillingRate'
    column[new_column_name] = old_column_data

    column_Data = flipkart_Data['Quantity']
    column['Quantity'] = pd.DataFrame(column_Data)

    column_Data = flipkart_Data['CGST%']
    column['CGST%'] = pd.DataFrame(column_Data)

    column_Data = flipkart_Data['SGST%']
    column['SGST%'] = pd.DataFrame(column_Data)

    column_Data = flipkart_Data['IGST%']
    column['IGST%'] = pd.DataFrame(column_Data)
    column['LINE_SHIPPING_AMT_INCL_TAX']=''

    column['Amount'] = 0
    for index, row in column.iterrows():
        CGST = row['BillingRate'] * row['Quantity']
        column.at[index, 'Amount'] = CGST
        new_data = pd.DataFrame(column['Amount'])

    column['CGSTAmount'] = 0
    for index, row in column.iterrows():
        CGST = row['Amount'] * row['CGST%'] / 100
        column.at[index, 'CGSTAmount'] = CGST
        new_data = pd.DataFrame(column['CGSTAmount'])

    column['SGSTAmount'] = 0
    for index, row in column.iterrows():
        CGST = row['Amount'] * row['SGST%'] / 100
        column.at[index, 'SGSTAmount'] = CGST
        new_data = pd.DataFrame(column['SGSTAmount'])

    column['IGSTAmount'] = 0
    for index, row in column.iterrows():
        CGST = row['Amount'] * row['IGST%'] / 100
        column.at[index, 'IGSTAmount'] = CGST
        new_data = pd.DataFrame(column['IGSTAmount'])

    column['TotalTax%'] = 0
    for index, row in column.iterrows():
        TotalTax = row['CGST%']+row['SGST%']+row['IGST%']
        column.at[index, 'TotalTax%'] = TotalTax
        new_data = pd.DataFrame(column['TotalTax%'])

    column['TotalTax'] = 0
    for index, row in column.iterrows():
        TotalTax = row['CGSTAmount']+row['SGSTAmount']+row['IGSTAmount']
        column.at[index, 'TotalTax'] = TotalTax
        new_data = pd.DataFrame(column['TotalTax'])

    column['LineAmount'] = 0
    for index, row in column.iterrows():
        TotalTax = row['Amount']+row['TotalTax']
        column.at[index, 'LineAmount'] = TotalTax
        new_data = pd.DataFrame(column['LineAmount'])
        new_data.reset_index(drop=True, inplace=True)

    column['LineAmtWithShipping'] = 0
    for index, row in column.iterrows():
        TotalTax = row['Amount']+row['TotalTax']
        column.at[index, 'LineAmtWithShipping'] = TotalTax
        new_data = pd.DataFrame(column['LineAmtWithShipping'])
        new_data.reset_index(drop=True, inplace=True)

    column['LINE_ITEM_AMT_INCL_TAX'] = 0
    for index, row in column.iterrows():
        TotalTax = row['Amount']+row['TotalTax']
        column.at[index, 'LINE_ITEM_AMT_INCL_TAX'] = TotalTax
        new_data = pd.DataFrame(column['LINE_ITEM_AMT_INCL_TAX'])
        new_data.reset_index(drop=True, inplace=True)

    column['LINE_ITEM_DISCAMT_INCL_TAX'] = 0
    for index, row in column.iterrows():
        TotalTax = row['Amount']+row['TotalTax']
        column.at[index, 'LINE_ITEM_DISCAMT_INCL_TAX'] = TotalTax
        new_data = pd.DataFrame(column['LINE_ITEM_DISCAMT_INCL_TAX'])
        new_data.reset_index(drop=True, inplace=True)

    column_Data = flipkart_Data['ProductName']
    column['ProductName'] = pd.DataFrame(column_Data)

    column_Data = flipkart_Data['State']
    column['State'] = pd.DataFrame(column_Data)
    column['Payment Method']='Prepaid'
    column['Shipping Provider Name']='Selfship'

    column_Data = flipkart_Data['ItemEAN']
    column['ItemEAN'] = pd.DataFrame(column_Data)

    
    
    def extract_sku(text):
        pattern = r'\bSKU:([\w\s]+)\b'
        match = re.search(pattern, text)
        if match:
            return match.group(1)
        else:
            return ''
    column['ItemEAN'] = column['ItemEAN'].apply(extract_sku)
    column['DOCUMENT']=''

    output_file_path = f"{output_folder}/Flipkart_salesreturn.csv"

    if os.path.exists(output_file_path):
        index = 1
        while True:
            new_output_file_path = f"{output_folder}/Flipkart_salesreturn({index}).csv"
            if not os.path.exists(new_output_file_path):
                output_file_path = new_output_file_path
                break
            index += 1
    column.to_csv(output_file_path, index=False)
    st.success("File processed and saved successfully.")














    


options=[" ","Amazon_sales_B2B","Amazon_salesreturn_B2B","Amazon_sales_B2C","Amazon_salesreturn_B2C","Flipkart_Sale","Flipkart_Salesreturn"]

def Seller():
    import streamlit as st
    st.title("Sale Converter :office: :bar_chart:")
   

    emoji_image = Image.open(r"C:\Users\GHSL\Desktop\GENERATOR DATA\logo\Guardian.jpg")
    st.image(emoji_image,width=100)

   

    # Add a dropdown list to the sidebar
    option = st.sidebar.selectbox("Select an option", options)

    # Display the selected option in the main content area
    st.write("Selected:", option)


    # Initialize session state variables
    if 'file_path' not in st.session_state:
        st.session_state['file_path'] = None
    if 'output_folder' not in st.session_state:
        st.session_state['output_folder'] = None

    #File selection
    file_path = st.file_uploader("Select a file")
    if file_path is not None:
        st.session_state['file_path'] = file_path
        st.success("File uploaded successfully.")
   

    # Output folder selection
    
    output_path = os.path.join(os.getcwd())
    
    output_folder = st.text_input("Enter output folder path",value=output_path)
   
    if output_folder != "":
        st.session_state['output_folder'] = output_folder

    # Process file button
    selected_option = st.button("Process File")
    if selected_option:
        if st.session_state['file_path'] is None:
            st.error("Please upload a file.")
        elif st.session_state['output_folder'] is None:
            st.error("Please enter an output folder path.")
        else:
            try:
                if option== "Amazon_sales_B2B":
                    Amazon_sales_B2B()

                elif option== "Amazon_salesreturn_B2B":
                    Amazon_salesreturn_B2B()
                
                elif option== "Amazon_sales_B2C":
                    Amazon_sales_B2C()

                elif option== "Amazon_salesreturn_B2C":
                    Amazon_salesreturn_B2C()

                elif option== "Flipkart_Sale":
                    flipkart_sale()

                elif option== "Flipkart_Salesreturn":
                    flipkart_salesreturn()

                else:
                    st.error("Not selected any function!")
                # st.success("File processed successfully.")
            except Exception as e:
                st.error(f"An error occurred during file processing: {str(e)}")



# def Dashboard():
#     st.title("Reconcillation Dashboard :bar_chart:")
#     emoji_image = Image.open(r"C:\Users\GHSL\Documents\gnc-guardian-logo.png")
#     st.image(emoji_image,width=200)
#     st.write("     ")

#     option=("","Amazon B2B","Amazon B2C","Flipkart")
#     Select= st.sidebar.selectbox("Select an option",option)
#     st.write("", Select)

#     file_path = st.sidebar.file_uploader("Upload CSV Data",type="csv")
    
#     if file_path is not None:
#         st.success("File uploaded successfully.")
#         df = pd.read_csv(file_path)
#         st.write("File Data:")
#         st.dataframe(df)
        
        
    # Data=pd.read_csv("file_path")
    # st.write(Data)
    

# navigation = st.sidebar.radio("Navigation", ("Seller", "Dashboard"))

# if navigation == "Seller":
#     Seller()
# else:
#     Dashboard()
if __name__ == "__main__":
    Seller()







