from flask import Flask, render_template, request, redirect
import sqlite3
import pandas as pd
import os

global data

database_path = r"C:\Users\elija\OneDrive\Desktop\INFO2000\info2000assignments-TheAntiBreacher\Database.sqlite"
database = os.path.abspath(database_path)

# Connect to the SQLite database using Flask
with sqlite3.connect(database, check_same_thread=False) as SQ:
    app = Flask(__name__)

    @app.route('/')
    def home():
        return render_template('Home.html')

    @app.route('/enterproduct', methods=['GET', 'POST'])
    def enterproduct():
        if request.method == 'POST':
            # Retrieve product information from the form
            prod_cat = request.form.get("ProdCat")
            prod_des = request.form.get("ProdDes")
            price = request.form.get("Price")
            prod_code = request.form.get("ProdCode")

            if prod_cat and prod_des and price and prod_code:
                # Create a DataFrame with the entered product information
                data = pd.DataFrame({'Product Category': [prod_cat], 'Product Description': [prod_des], 'Price': [price],'Product Code': [prod_code]})
                try:
                    # Creates the Users table if it doesn't exist
                    SQ.execute("CREATE TABLE IF NOT EXISTS Users (\
                                'Product Category' TEXT,\
                                'Product Description' TEXT,\
                                'Price' TEXT,\
                                'Product Code' TEXT)")
                    # Where the new data is written
                    data.to_sql(name="Users", con=SQ, if_exists='append', index=False)
                except Exception as e:
                    print(f"Error: {e}")
                return redirect('/')  # Brings you back to the home page
        return render_template("EnterProduct.html")

    @app.route('/retrieval', methods=['GET', 'POST'])
    def retrieval():
        if request.method == 'POST':
            # Retrieve the appropriate category for from user input
            request_cat = request.form.get("CategoryRetrieve")
            if request_cat:
                # Depending on what categoroy the user inputs in, the function retrieves all information relating to that category
                query = "SELECT * FROM Users WHERE `Product Category` = ?"
                result = pd.read_sql_query(query, SQ, params=(request_cat,))
                print(result)
                to_send = result.to_records()
            else:
                # If no category is specified, retrieves all products available in the database
                query = "SELECT * FROM Users"
                result = pd.read_sql_query(query, SQ)
                print(result)
                to_send = result.to_records()

            return render_template('Retrieval.html', df=to_send)
        return render_template('Retrieval.html')

    @app.route('/delete', methods=['POST'])
    def delete():
        if request.method == 'POST':
            # Finds the product code to be deleted
            product_code = request.form.get("ProductCodeToDelete")

            if product_code:
                # Delete the product with the specified product code
                query1 = "DELETE FROM Users WHERE `Product Code` = ?"
                SQ.execute(query1, (product_code,))
                SQ.commit()

        return redirect('/retrieval')  # Redirect to the retrieval page after deleting item

if __name__ == '__main__':
    app.run(debug=True)

