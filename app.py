from flask import Flask, render_template, request, redirect, url_for, session
from models import db, Book

app = Flask(__name__)
app.secret_key = "bookstore_secret_123"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SECRET_KEY'] = 'your-secret-key'  # Needed for session
db.init_app(app)

# Home page: show available books
@app.route('/')
def home():
    books = Book.query.filter_by(sold=False).all()
    return render_template('home.html', books=books)
@app.route("/debug")
def debug():
    books = Book.query.all()
    return str([(b.id, b.title) for b in books])

# Add to cart
@app.route('/add_to_cart/<int:book_id>')
def add_to_cart(book_id):
    print("ADD TO CART CLICKED:", book_id)

    cart = session.get('cart', [])
    print("Before:", cart)

    if book_id not in cart:
        cart.append(book_id)

    session['cart'] = cart
    session.modified = True

    print("After:", session['cart'])

    return redirect(url_for('home'))


# Cart page
@app.route('/cart')
def cart():
    cart_items = session.get('cart', [])
    books_in_cart = Book.query.filter(Book.id.in_(cart_items)).all() if cart_items else []
    total = sum(book.price for book in books_in_cart)
    return render_template('cart.html', books=books_in_cart, total=total)

# Remove from cart
@app.route('/remove_from_cart/<int:book_id>')
def remove_from_cart(book_id):
    cart = session.get('cart', [])
    if book_id in cart:
        cart.remove(book_id)
    session['cart'] = cart
    return redirect(url_for('cart'))
@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    if request.method == "POST":
        cart = session.get("cart", [])

        for book_id in cart:
            book = Book.query.get(book_id)
            if book:
                book.sold = True   # mark purchased

        db.session.commit()
        session["cart"] = []   # empty cart

        return render_template("success.html")

    return render_template("checkout.html")

@app.route("/add-sample-books")
def add_sample_books():
    Book.query.delete()   # clear old data

    books = [
        Book(title="Python for Beginners", price=499, description="Learn Python from scratch", image="book1.jpg"),
        Book(title="Flask Web Development", price=699, description="Build web apps using Flask", image="book2.jpg"),
        Book(title="Mastering Django", price=799, description="Advanced Django guide", image="book3.jpg"),
        Book(title="Data Science with Python", price=899, description="Data analysis and ML", image="book4.jpg"),
        Book(title="JavaScript Essentials", price=599, description="Frontend fundamentals", image="book5.jpg"),
        Book(title="React JS in Action", price=799, description="Build UI with React", image="book6.jpg"),
        Book(title="SQL & Databases", price=549, description="Learn SQL and DB design", image="book7.jpg"),
        Book(title="DevOps Basics", price=649, description="CI/CD, Docker & Cloud", image="book8.jpg"),
        Book(title="AI & Machine Learning", price=999, description="AI concepts and projects", image="book9.jpg"),
        Book(title="System Design Interview", price=899, description="Crack backend interviews", image="book10.jpg")
    ]

    db.session.add_all(books)
    db.session.commit()

    return "10 Books added successfully!"

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Ensure DB is created
    app.run(debug=True)
