from flask import Flask, render_template, flash, request, session,send_file
from flask import render_template, redirect, url_for, request
import datetime
import mysql.connector
import sys
app = Flask(__name__)
app.config['DEBUG']
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

@app.route("/")
def homepage():
    import os, shutil
    folder = 'static/plott'
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

    return render_template('index.html')


@app.route("/ViewData")
def ViewData():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1Medicalddb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM salestb ")
    data = cur.fetchall()

    return render_template('ViewData.html',data=data)


@app.route("/excelpost", methods=['GET', 'POST'])
def uploadassign():
    if request.method == 'POST':

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1Medicalddb')
        cursor = conn.cursor()
        cursor.execute("truncate table salestb ")
        conn.commit()
        conn.close()




        file = request.files['fileupload']
        file_extension = file.filename.split('.')[1]
        print(file_extension)
        #file.save("static/upload/" + secure_filename(file.filename))

        import pandas as pd
        import matplotlib.pyplot as plt
        df = ''
        if file_extension == 'xlsx':
            df = pd.read_excel(file.read(), engine='openpyxl')
        elif file_extension == 'xls':
            df = pd.read_excel(file.read())
        elif file_extension == 'csv':
            df = pd.read_csv(file)

        print(df)


        print("Preprocessing Completed")
        print(df)
        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1Medicalddb')
        cursor = conn.cursor()

        for row in df.itertuples():
            cursor.execute(" INSERT INTO salestb VALUES ('"+ row.Month +"','"+ row.Customer+"','"+ row.Period +"','"+row.Product +"','"+ row.Location +"','"+ row.SalesRep +"','"+ row.Supplier+"','"+ row.WarehouseLocations +"','"+ str(row.Actual) + "','"+str(row.CSales)+"','"+ str(row.InventoryStock)+"','"+ str(row.LSales)+"','"+ str(row.MSales) +"','"+str(row.NumberofRecords) + "','"+str(row.ReceivedInventory) +"','"+ str(row.RepSales) +"','"+str(row.Target) +"' )")
        conn.commit()
        conn.close()

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1Medicalddb')
        cur = conn.cursor()
        cur.execute("SELECT * FROM salestb ")
        data = cur.fetchall()




        return render_template('ViewData.html', data=data)
@app.route("/Customer")
def Customer():

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1Medicalddb')
    # cursor = conn.cursor()
    cur = conn.cursor()
    cur.execute(
        "SELECT  distinct Customer  FROM salestb ")
    customer = cur.fetchall()
    #print(coorname)

    return render_template('Customer.html', customer=customer)



@app.route("/csearch", methods=['GET', 'POST'])
def csearch():
    if request.method == 'POST':
        cname = request.form['Customer']

        import matplotlib.pyplot as plt
        import matplotlib
        matplotlib.use('Agg')

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1Medicalddb')

        mycursor = conn.cursor()

        # Fecthing Data From mysql to my python progame
        mycursor.execute("select Month, sum(CSales) as CSales from salestb where Customer='"+ cname +"' group by Month")
        result = mycursor.fetchall

        Month = []
        CSales = []
        Month.clear()
        CSales.clear()

        for i in mycursor:
            Month.append(i[0])
            CSales.append(i[1])

        print("Month = ", Month)
        print("Total Sales = ", CSales)

        # Visulizing Data using Matplotlib
        plt.figure(figsize=(12, 10))
        plt.bar(Month, CSales, color=['black', 'red', 'green', 'blue', 'cyan'])
        #plt.ylim(0, 5)

        ax = plt.gca()
        plt.draw()

        ax.tick_params(axis='x', rotation=70)
        plt.xlabel("Month",fontsize=5)
        plt.ylabel("Total Sales")
        plt.title("Customer Sales")



        import random

        n = random.randint(1111, 9999)

        plt.savefig('static/plott/' + str(n) + '.jpg')

        iimg = 'static/plott/' +str(n)+ '.jpg'





        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1Medicalddb')
        cur = conn.cursor()
        cur.execute("SELECT * FROM salestb where Customer='"+ cname +"' ")
        data = cur.fetchall()

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1Medicalddb')
        # cursor = conn.cursor()
        cur = conn.cursor()
        cur.execute(
            "SELECT  distinct Customer  FROM salestb ")
        customer = cur.fetchall()





        return render_template('Customer.html', data=data,dataimg=iimg,customer=customer)

@app.route("/Location")
def Location():

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1Medicalddb')
    # cursor = conn.cursor()
    cur = conn.cursor()
    cur.execute(
        "SELECT  distinct Location  FROM salestb ")
    location = cur.fetchall()
    #print(coorname)

    return render_template('Location.html', locat=location)





@app.route("/lsearch", methods=['GET', 'POST'])
def lsearch():
    if request.method == 'POST':




        lllocation = request.form['loc']

        import matplotlib.pyplot as plt
        import matplotlib
        matplotlib.use('Agg')

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1Medicalddb')

        mycursor = conn.cursor()
        mycursor.execute("select Month, sum(MSales) as MSales from salestb where Location='"+ lllocation +"' group by Month")
        result = mycursor.fetchall

        Month = []
        MSales = []
        Month.clear()
        MSales.clear()

        for i in mycursor:
            Month.append(i[0])
            MSales.append(i[1])

        print("Month = ", Month)
        print("Total Sales = ", MSales)




        # Visulizing Data using Matplotlib
        plt.figure(figsize=(12, 10))
        plt.bar(Month, MSales, color=['yellow', 'red', 'green', 'blue', 'cyan'])
        #plt.ylim(0, 5)

        ax = plt.gca()
        plt.draw()

        ax.tick_params(axis='x', rotation=70)

        plt.xlabel("Month")
        plt.ylabel("Total Sales")
        plt.title("Sales By Location")
        import random

        n = random.randint(1111, 9999)

        plt.savefig('static/plott/'+str(n)+'.jpg')


        iimg = 'static/plott/'+str(n)+'.jpg'




        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1Medicalddb')
        cur = conn.cursor()
        cur.execute("SELECT * FROM salestb where Location='"+ lllocation +"' ")
        data = cur.fetchall()



        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1Medicalddb')
        # cursor = conn.cursor()
        cur = conn.cursor()
        cur.execute(
            "SELECT  distinct location  FROM salestb ")
        locati = cur.fetchall()





        return render_template('Location.html', data=data, dataimg=iimg, locat=locati)
@app.route("/Sales")
def Sales():

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1Medicalddb')
    # cursor = conn.cursor()
    cur = conn.cursor()
    cur.execute(
        "SELECT  distinct Month  FROM salestb ")
    location = cur.fetchall()
    #print(coorname)

    return render_template('Sales.html', mon=location)


@app.route("/salsearch", methods=['GET', 'POST'])
def salsearch():
    if request.method == 'POST':




        month = request.form['loc']

        import matplotlib.pyplot as plt
        import matplotlib
        matplotlib.use('Agg')

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1Medicalddb')

        mycursor = conn.cursor()
        mycursor.execute("select Product, sum(RepSales) as MSales from salestb group by Product")
        result = mycursor.fetchall

        Month = []
        MSales = []
        Month.clear()
        MSales.clear()

        for i in mycursor:
            Month.append(i[0])
            MSales.append(i[1])

        print("Month = ", Month)
        print("Total Sales = ", MSales)




        # Visulizing Data using Matplotlib
        plt.figure(figsize=(12, 10))
        plt.bar(Month, MSales, color=['yellow', 'red', 'green', 'blue', 'cyan'])
        #plt.ylim(0, 5)

        ax = plt.gca()
        plt.draw()

        ax.tick_params(axis='x', rotation=70)
        plt.xlabel("Product")
        plt.ylabel("Total Sales")
        plt.title("Sales By Product")
        import random

        n = random.randint(1111, 9999)

        plt.savefig('static/plott/'+str(n)+'.jpg')


        iimg = 'static/plott/'+str(n)+'.jpg'




        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1Medicalddb')
        cur = conn.cursor()
        cur.execute("SELECT * FROM salestb where Month='"+ month +"' ")
        data = cur.fetchall()



        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1Medicalddb')
        # cursor = conn.cursor()
        cur = conn.cursor()
        cur.execute(
            "SELECT  distinct Month  FROM salestb ")
        locati = cur.fetchall()





        return render_template('Sales.html', data=data, dataimg=iimg, mon=locati)

@app.route("/SupplierInventory")
def SupplierInventory():

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1Medicalddb')
    # cursor = conn.cursor()
    cur = conn.cursor()
    cur.execute(
        "SELECT  distinct Supplier  FROM salestb ")
    customer = cur.fetchall()
    #print(coorname)

    return render_template('SupplierInventory.html', sup=customer)



@app.route("/supsearch", methods=['GET', 'POST'])
def supsearch():
    if request.method == 'POST':
        cname = request.form['sup']

        import matplotlib.pyplot as plt
        import matplotlib
        matplotlib.use('Agg')

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1Medicalddb')

        mycursor = conn.cursor()

        # Fecthing Data From mysql to my python progame
        mycursor.execute("select Month, sum(InventoryStock) as InventoryStock from salestb where Supplier='"+ cname +"' group by Month")
        result = mycursor.fetchall

        Month = []
        CSales = []
        Month.clear()
        CSales.clear()

        for i in mycursor:
            Month.append(i[0])
            CSales.append(i[1])

        print("Month = ", Month)
        print("Total Sales = ", CSales)

        # Visulizing Data using Matplotlib
        plt.figure(figsize=(12, 10))
        plt.bar(Month, CSales, color=['black', 'red', 'green', 'blue', 'cyan'])
        #plt.ylim(0, 5)

        ax = plt.gca()
        plt.draw()

        ax.tick_params(axis='x', rotation=70)
        plt.xlabel("Month")
        plt.ylabel("Inventory Stock")
        plt.title("Inventory")

        import random

        n = random.randint(1111, 9999)

        plt.savefig('static/plott/' + str(n) + '.jpg')

        iimg = 'static/plott/' +str(n)+ '.jpg'





        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1Medicalddb')
        cur = conn.cursor()
        cur.execute("SELECT * FROM salestb where Supplier='"+ cname +"' ")
        data = cur.fetchall()

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1Medicalddb')
        # cursor = conn.cursor()
        cur = conn.cursor()
        cur.execute(
            "SELECT  distinct Supplier  FROM salestb ")
        customer = cur.fetchall()





        return render_template('SupplierInventory.html', data=data,dataimg=iimg,sup=customer)



@app.route("/Inventory")
def Inventory():

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1Medicalddb')
    # cursor = conn.cursor()
    cur = conn.cursor()
    cur.execute(
        "SELECT  distinct Month  FROM salestb ")
    location = cur.fetchall()
    #print(coorname)

    return render_template('Inventory.html', mon=location)


@app.route("/insearch", methods=['GET', 'POST'])
def insearch():
    if request.method == 'POST':




        month = request.form['loc']

        import matplotlib.pyplot as plt
        import matplotlib
        matplotlib.use('Agg')

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1Medicalddb')

        mycursor = conn.cursor()
        mycursor.execute("select Product, sum(InventoryStock) as InventoryStock from salestb where Month='"+ month +"' group by Product")
        result = mycursor.fetchall

        Month = []
        MSales = []
        Month.clear()
        MSales.clear()

        for i in mycursor:
            Month.append(i[0])
            MSales.append(i[1])

        print("Month = ", Month)
        print("Total Sales = ", MSales)




        # Visulizing Data using Matplotlib
        plt.figure(figsize=(12, 10))
        plt.bar(Month, MSales, color=['yellow', 'red', 'green', 'blue', 'cyan'])
        #plt.ylim(0, 5)

        ax = plt.gca()
        plt.draw()

        ax.tick_params(axis='x', rotation=70)
        plt.xlabel("Product")
        plt.ylabel("Inventory Stock")
        plt.title(" Inventory")
        import random

        n = random.randint(1111, 9999)

        plt.savefig('static/plott/'+str(n)+'.jpg')


        iimg = 'static/plott/'+str(n)+'.jpg'




        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1Medicalddb')
        cur = conn.cursor()
        cur.execute("SELECT * FROM salestb where Month='"+ month +"' ")
        data = cur.fetchall()



        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1Medicalddb')
        # cursor = conn.cursor()
        cur = conn.cursor()
        cur.execute(
            "SELECT  distinct Month  FROM salestb ")
        locati = cur.fetchall()



        return render_template('Inventory.html', data=data, dataimg=iimg, mon=locati)


@app.route("/SalesTrend")
def SalesTrend():

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1Medicalddb')
    # cursor = conn.cursor()
    cur = conn.cursor()
    cur.execute(
        "SELECT  distinct Month  FROM salestb ")
    location = cur.fetchall()
    #print(coorname)

    return render_template('SalesTrend.html', mon=location)


@app.route("/stsearch", methods=['GET', 'POST'])
def stsearch():
    if request.method == 'POST':




        month = request.form['loc']

        import matplotlib.pyplot as plt
        import matplotlib
        matplotlib.use('Agg')

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1Medicalddb')

        mycursor = conn.cursor()
        mycursor.execute("select Product, sum(Actual) as Actual from salestb where Month='"+ month +"' group by Product order by Actual  DESC")
        result = mycursor.fetchall

        Month = []
        MSales = []
        Month.clear()
        MSales.clear()

        for i in mycursor:
            Month.append(i[0])
            MSales.append(i[1])

        print("Month = ", Month)
        print("Total Sales = ", MSales)




        # Visulizing Data using Matplotlib
        plt.figure(figsize=(12, 10))
        plt.bar(Month, MSales, color=['yellow', 'red', 'green', 'blue', 'cyan'])
        #plt.ylim(0, 5)

        ax = plt.gca()
        plt.draw()

        ax.tick_params(axis='x', rotation=70)
        plt.xlabel("Product")
        plt.ylabel("Total Sales")
        plt.title("Sales Trend")
        import random

        n = random.randint(1111, 9999)

        plt.savefig('static/plott/'+str(n)+'.jpg')


        iimg = 'static/plott/'+str(n)+'.jpg'




        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1Medicalddb')
        cur = conn.cursor()
        cur.execute("SELECT * FROM salestb where Month='"+ month +"' ")
        data = cur.fetchall()



        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1Medicalddb')
        # cursor = conn.cursor()
        cur = conn.cursor()
        cur.execute(
            "SELECT  distinct Month  FROM salestb ")
        locati = cur.fetchall()





        return render_template('SalesTrend.html', data=data, dataimg=iimg, mon=locati)


@app.route("/MonthlySales")
def MonthlySales():

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1Medicalddb')
    # cursor = conn.cursor()
    cur = conn.cursor()
    cur.execute(
        "SELECT  distinct Month  FROM salestb ")
    location = cur.fetchall()
    #print(coorname)

    return render_template('MonthlySales.html', mon=location)


@app.route("/msearch", methods=['GET', 'POST'])
def msearch():
    if request.method == 'POST':




        month = request.form['loc']

        import matplotlib.pyplot as plt
        import matplotlib
        matplotlib.use('Agg')

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1Medicalddb')

        mycursor = conn.cursor()
        mycursor.execute("select Product, sum(MSales) as MSales from salestb where Month='"+ month +"' group by Product ")
        result = mycursor.fetchall

        Month = []
        MSales = []
        Month.clear()
        MSales.clear()

        for i in mycursor:
            Month.append(i[0])
            MSales.append(i[1])

        print("Month = ", Month)
        print("Total Sales = ", MSales)




        # Visulizing Data using Matplotlib
        plt.figure(figsize=(12, 10))
        plt.bar(Month, MSales, color=['yellow', 'red', 'green', 'blue', 'cyan'])
        #plt.ylim(0, 5)

        ax = plt.gca()
        plt.draw()

        ax.tick_params(axis='x', rotation=70)
        plt.xlabel("Product")
        plt.ylabel("Total Sales")
        plt.title("Monthly Sales")
        import random

        n = random.randint(1111, 9999)

        plt.savefig('static/plott/'+str(n)+'.jpg')


        iimg = 'static/plott/'+str(n)+'.jpg'




        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1Medicalddb')
        cur = conn.cursor()
        cur.execute("SELECT * FROM salestb where Month='"+ month +"' ")
        data = cur.fetchall()



        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1Medicalddb')
        # cursor = conn.cursor()
        cur = conn.cursor()
        cur.execute(
            "SELECT  distinct Month  FROM salestb ")
        locati = cur.fetchall()





        return render_template('MonthlySales.html', data=data, dataimg=iimg, mon=locati)



@app.route("/InventorybyMonth")
def InventorybyMonth():

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1Medicalddb')
    # cursor = conn.cursor()
    cur = conn.cursor()
    cur.execute(
        "SELECT  distinct Month  FROM salestb ")
    location = cur.fetchall()
    #print(coorname)

    return render_template('InventorybyMonth.html', mon=location)


@app.route("/insalsearch", methods=['GET', 'POST'])
def insalsearch():
    if request.method == 'POST':




        month = request.form['loc']

        import matplotlib.pyplot as plt
        import matplotlib
        import  numpy as np
        matplotlib.use('Agg')

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1Medicalddb')

        mycursor = conn.cursor()
        mycursor.execute("select Product, sum(Actual) as Actual, sum(ReceivedInventory) as ReceivedInventory from salestb where Month='"+ month +"' group by Product ")
        result = mycursor.fetchall

        Month = []
        Actual = []
        inven = []
        Month.clear()
        Actual.clear()
        inven.clear()

        for i in mycursor:
            Month.append(i[0])
            Actual.append(i[1])
            inven.append(i[2])

            # Visulizing Data using Matplotlib



        #labels = ['G1', 'G2', 'G3', 'G4', 'G5']
        #men_means = [20, 34, 30, 35, 27]
        #women_means = [25, 32, 34, 20, 25]
        plt.figure(figsize=(12, 10))



        x = np.arange(len(Month))  # the label locations
        width = 0.35  # the width of the bars

        fig, ax = plt.subplots()
        rects1 = ax.bar(x - width / 2, Actual, width, label='Actual')
        rects2 = ax.bar(x + width / 2, inven, width, label='inven')

        # Add some text for labels, title and custom x-axis tick labels, etc.


        ax.set_ylabel('Count')
        ax.set_title(' Actual and Received Inventory by Month')
        ax.set_xticks(x, Month,fontsize=8)
        ax.tick_params(axis='x', rotation=70)
        ax.legend()



        ax.bar_label(rects1, padding=3)
        ax.bar_label(rects2, padding=3)

        fig.tight_layout()





        #@plt.show()







        import random

        n = random.randint(1111, 9999)

        plt.savefig('static/plott/'+str(n)+'.jpg')


        iimg = 'static/plott/'+str(n)+'.jpg'




        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1Medicalddb')
        cur = conn.cursor()
        cur.execute("SELECT * FROM salestb where Month='"+ month +"' ")
        data = cur.fetchall()



        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1Medicalddb')
        # cursor = conn.cursor()
        cur = conn.cursor()
        cur.execute(
            "SELECT  distinct Month  FROM salestb ")
        locati = cur.fetchall()





        return render_template('InventorybyMonth.html', data=data, dataimg=iimg, mon=locati)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)