import sys
import os
from flask import Flask, jsonify, render_template_string, request, redirect, url_for
from dominate import document
from dominate.tags import *

# Adjust path to import from shared module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from shared.database import get_db_connection

# --- Flask App Initialization ---
# The static_folder path is relative to the location of this script
app = Flask(__name__, static_folder='../assets')


# --- dominate HTML Page Generation ---

def create_base_template(title="PUP E-Commerce"):
    """Creates the base HTML structure with head and body."""
    doc = document(title=title)
    with doc.head:
        meta(charset="UTF-8")
        meta(name="viewport", content="width=device-width, initial-scale=1.0")
        link(href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css", rel="stylesheet")
        # Link to our custom CSS for the font
        link(href=url_for('static', filename='css/styles.css'), rel="stylesheet")
        style("""
            .pup-maroon { color: #7b2120; }
            .bg-pup-maroon { background-color: #7b2120; }
            .border-pup-maroon { border-color: #7b2120; }
            .bg-pup-gold { background-color: #f2c202; }
            .text-pup-gold { color: #f2c202; }
        """)
    return doc

def render_login_page():
    """Generates the Login/Registration page (Image 1)."""
    doc = create_base_template("Login or Register")
    with doc.body(cls="bg-gray-100 flex items-center justify-center min-h-screen"):
        with div(cls="w-full max-w-sm p-8 space-y-8 bg-white rounded-lg shadow-md"):
            with div(cls="text-center"):
                img(src=url_for('static', filename='images/pup_logo.png'), cls="w-24 h-24 mx-auto mb-4")
                h1("Mula sayo para", cls="text-3xl font-bold text-pup-maroon")
                h1("sa bayan", cls="text-3xl font-bold text-pup-maroon")

            with form(cls="mt-8 space-y-6", action="/register", method="POST"):
                # Registration fields
                div(label("Name:", _for="name", cls="block text-sm font-medium text-gray-700"), cls="mb-2")
                input_(type="text", id="name", name="name", required=True, cls="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-pup-maroon focus:border-pup-maroon")
                
                div(label("Email Address:", _for="email", cls="block text-sm font-medium text-gray-700"), cls="mb-2")
                input_(type="email", id="email", name="email", required=True, cls="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-pup-maroon focus:border-pup-maroon")

                div(label("Password:", _for="password", cls="block text-sm font-medium text-gray-700"), cls="mb-2")
                input_(type="password", id="password", name="password", required=True, cls="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-pup-maroon focus:border-pup-maroon")

                div(label("Confirm Password:", _for="confirm_password", cls="block text-sm font-medium text-gray-700"), cls="mb-2")
                input_(type="password", id="confirm_password", name="confirm_password", required=True, cls="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-pup-maroon focus:border-pup-maroon")

                div(cls="space-y-2 pt-4")
                a("Back to LOGIN", href="/login", cls="block w-full text-center px-4 py-2 text-sm font-medium text-white bg-cyan-500 rounded-md hover:bg-cyan-600")
                button("REGISTER", type="submit", cls="w-full px-4 py-2 text-sm font-medium text-white bg-cyan-600 rounded-md hover:bg-cyan-700")
            
            a("?", href="/contact", cls="fixed bottom-4 right-4 bg-black text-white w-10 h-10 rounded-full flex items-center justify-center text-lg font-bold shadow-lg")
    
    return doc.render()


def render_homepage():
    """Generates the Homepage with product listings."""
    doc = create_base_template("PUP Shop - Home")
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, name, price, image_url FROM products")
    products = cursor.fetchall()
    cursor.close()
    conn.close()

    with doc.body(cls="bg-gray-50"):
        # Header
        with header(cls="sticky top-0 bg-white shadow-md z-10"):
            with div(cls="container mx-auto px-4 py-3 flex justify-between items-center"):
                img(src=url_for('static', filename='images/pup_logo.png'), cls="h-10")
                h1("StudywithStyle", cls="text-2xl font-bold text-pup-maroon")
                with div(cls="flex items-center space-x-4"):
                    a(i(cls="fas fa-shopping-cart"), href="/cart", cls="text-xl text-gray-600") # Use FontAwesome if you add it
                    a(i(cls="fas fa-user"), href="/profile", cls="text-xl text-gray-600")
        
        # Main Content
        with main(cls="container mx-auto p-4"):
            # Banner
            with div(cls="relative bg-pup-maroon text-white p-8 rounded-lg mb-8 text-center"):
                img(src=url_for('static', filename='images/pup_logo.png'), cls="absolute top-2 left-2 h-8 opacity-20")
                h2("POLYTECHNIC UNIVERSITY OF THE PHILIPPINES", cls="text-xl font-bold")
                p("Mula sayo para sa bayan", cls="text-pup-gold")

            # Product Grid
            with div(cls="grid grid-cols-2 gap-4"):
                for product in products:
                    with a(href=f"/product/{product['id']}", cls="block bg-white rounded-lg shadow hover:shadow-lg transition-shadow"):
                        img(src=product['image_url'], cls="w-full h-48 object-cover rounded-t-lg")
                        with div(cls="p-4"):
                            h3(product['name'], cls="font-bold text-gray-800 truncate")
                            p(f"₱{product['price']:.2f}", cls="text-lg font-bold text-pup-maroon mt-1")
        
        # Bottom Navigation
        with nav(cls="fixed bottom-0 left-0 right-0 bg-white border-t-2 border-pup-maroon p-2 flex justify-around"):
             a("Home", href="/", cls="text-pup-maroon")
             a("Cart", href="/cart", cls="text-pup-maroon")
             a("Profile", href="/profile", cls="text-pup-maroon")

    return doc.render()

# --- Flask Routes ---

@app.route('/')
def home():
    """Route for the homepage."""
    return render_homepage()

@app.route('/login')
@app.route('/register')
def login_register():
    """Route for the combined login/register page."""
    return render_login_page()

@app.route('/splash/<int:page_num>')
def splash(page_num):
    """Route for splash screens."""
    doc = create_base_template(f"Welcome - {page_num}")
    with doc.body(cls="bg-pup-maroon text-white flex flex-col items-center justify-center h-screen p-8 text-center"):
        img(src=url_for('static', filename='images/pup_logo.png'), cls="w-32 h-32 mb-8")
        if page_num == 1:
            h1("Welcome to the PUP E-Commerce App", cls="text-3xl font-bold text-pup-gold")
            p("Your one-stop shop for official university merchandise.", cls="mt-4 text-lg")
            a("NEXT >", href="/splash/2", cls="mt-8 bg-pup-gold text-pup-maroon font-bold py-2 px-6 rounded-full")
        elif page_num == 2:
            h1("STUDY WITH PASSION", cls="text-3xl font-bold text-pup-gold")
            p("Find everything you need, from lanyards to tote bags.", cls="mt-4 text-lg")
            a("NEXT >", href="/splash/3", cls="mt-8 bg-pup-gold text-pup-maroon font-bold py-2 px-6 rounded-full")
        elif page_num == 3:
            h1("Mula Sayo, Para sa Bayan", cls="text-3xl font-bold text-pup-gold")
            p("Every purchase supports our beloved university.", cls="mt-4 text-lg")
            a("GET STARTED", href="/", cls="mt-8 bg-pup-gold text-pup-maroon font-bold py-2 px-6 rounded-full")
        else:
            return redirect(url_for('home'))

    return doc.render()


# Add routes for /cart, /profile, /product/<id>, /contact etc. as needed
# For brevity, only the key requested pages are implemented here.
# You would follow the same pattern: create a render function and a route.