import sys
import os
from flask import Flask, jsonify, request, redirect, url_for
from dominate import document
from dominate.tags import *

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from shared.database import get_db_connection

app = Flask(__name__, static_folder='../assets')

def create_admin_base(title):
    doc = document(title=title)
    with doc.head:
        meta(charset="UTF-8")
        link(href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css", rel="stylesheet")
        link(href=url_for('static', filename='css/styles.css'), rel="stylesheet")
    return doc

def render_inventory_management():
    doc = create_admin_base("Admin - Inventory Management")
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, name, stock, price FROM products ORDER BY id")
    products = cursor.fetchall()
    cursor.close()
    conn.close()

    with doc.body(cls="bg-gray-100 p-8"):
        with div(cls="max-w-4xl mx-auto bg-white p-6 rounded-lg shadow"):
            img(src=url_for('static', filename='images/pup_logo.png'), cls="h-16 mx-auto mb-4")
            h1("INVENTORY MANAGEMENT", cls="text-3xl font-bold text-center text-pup-maroon mb-6 border-b-2 pb-2 border-pup-maroon")

            with form(action="/add", method="POST", cls="grid grid-cols-1 md:grid-cols-2 gap-4 mb-8"):
                div(label("Item Name:", cls="block font-bold"), input_(type="text", name="name", required=True, cls="mt-1 block w-full border-gray-300 rounded-md shadow-sm"))
                div(label("Quantity:", cls="block font-bold"), input_(type="number", name="quantity", required=True, cls="mt-1 block w-full border-gray-300 rounded-md shadow-sm"))
                div(label("Price (₱):", cls="block font-bold"), input_(type="text", name="price", required=True, cls="mt-1 block w-full border-gray-300 rounded-md shadow-sm"))
                div(label("Image URL:", cls="block font-bold"), input_(type="text", name="image_url", placeholder="/static/images/...", required=True, cls="mt-1 block w-full border-gray-300 rounded-md shadow-sm"))
                
                with div(cls="md:col-span-2 flex justify-end space-x-2 mt-4"):
                    button("Add Item", type="submit", cls="bg-green-600 text-white font-bold py-2 px-4 rounded")
                    # Update/Delete buttons would require JS to populate form fields
            
            # Inventory Table
            with table(cls="min-w-full divide-y divide-gray-200 mt-4"):
                with thead(cls="bg-gray-50"):
                    with tr():
                        th("ID", cls="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider")
                        th("Name", cls="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider")
                        th("Quantity", cls="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider")
                        th("Price", cls="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider")
                        th("Actions", cls="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider")
                with tbody(cls="bg-white divide-y divide-gray-200"):
                    for p in products:
                        with tr():
                            td(p['id'], cls="px-6 py-4 whitespace-nowrap")
                            td(p['name'], cls="px-6 py-4 whitespace-nowrap")
                            td(p['stock'], cls="px-6 py-4 whitespace-nowrap")
                            td(f"₱{p['price']:.2f}", cls="px-6 py-4 whitespace-nowrap")
                            td(a("Delete", href=f"/delete/{p['id']}", cls="text-red-600 hover:text-red-900"), cls="px-6 py-4 whitespace-nowrap")
    return doc.render()

@app.route('/')
def admin_home():
    return render_inventory_management()

@app.route('/add', methods=['POST'])
def add_item():
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "INSERT INTO products (name, stock, price, image_url) VALUES (%s, %s, %s, %s)"
    data = (request.form['name'], request.form['quantity'], request.form['price'], request.form['image_url'])
    cursor.execute(query, data)
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('admin_home'))

@app.route('/delete/<int:item_id>')
def delete_item(item_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM products WHERE id = %s", (item_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('admin_home'))