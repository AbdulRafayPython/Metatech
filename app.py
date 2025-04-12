from flask import Flask, render_template, request, redirect, url_for, flash, session, g
import pymysql
import re
import os
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'metaltech_engineering_secret_key'

# Database Configuration
DB_HOST = '77.37.35.55'
DB_USER = 'u971630016_QUWvm'
DB_PASSWORD = 'bin@ncE_#21'
DB_NAME = 'u971630016_koxO0'

def get_db():
    if 'db' not in g:
        g.db = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            cursorclass=pymysql.cursors.DictCursor
        )
    return g.db

@app.teardown_appcontext
def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

# Database initialization script
def init_db():
    with app.app_context():
        db = get_db()
        with db.cursor() as cursor:
            # Create tables
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS mt_services (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    category VARCHAR(255) NOT NULL,
                    name VARCHAR(255) NOT NULL,
                    description TEXT,
                    image_url VARCHAR(255)
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS mt_testimonials (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    client_name VARCHAR(255) NOT NULL,
                    company VARCHAR(255),
                    content TEXT NOT NULL,
                    rating INT,
                    date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS mt_quotes (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    email VARCHAR(255) NOT NULL,
                    phone VARCHAR(20),
                    service VARCHAR(255),
                    message TEXT,
                    date_submitted TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS mt_blog_posts (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    title VARCHAR(255) NOT NULL,
                    content TEXT NOT NULL,
                    author VARCHAR(255),
                    image_url VARCHAR(255),
                    date_posted TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Insert sample data for services
            service_categories = [
                "Warehouse Equipments", "Pharmaceutical Fixtures", 
                "Display Stands for Showrooms", "Solar Panel Framing",
                "Premises Security", "General Fabrication"
            ]
            
            warehouse_equipments = [
                "Light Duty Racks", "Heavy Duty Racks", "Material handling Trolleys",
                "MS Pallets", "GI Pallets", "Column Guards", "Anti-Collision MS Barriers",
                "High Rise Pallet Racking"
            ]
            
            pharmaceutical_fixtures = [
                "SS Trays in 304 & 316 L Grade", "SS Pressure Vessels",
                "SS Ladders", "SS Lockers & Cabinets", 
                "SS containers/Buckets/Bins in 316 and 304 Grade",
                "SS Cross Over Benches, & Stands", "SS Pallets,Tables, Stools Etc",
                "Anti Vibration Tables"
            ]
            
            display_stands = [
                "Wall Mounted Display Stands", "Pedestal Stands with Marble Base",
                "Spinners Racks", "Aclyric Display", "Counter Top Stands"
            ]
            
            solar_panel = ["Solar Panel Framing"]
            
            premises_security = [
                "Barbed Wire", "Razors Wires", "Chain Link",
                "Watch Towers", "Security Cabin", "MS Barriers"
            ]
            
            general_fabrication = [
                "Laser Cut Doors", "Production Shades", "Parking Shades",
                "Main Gates", "Pargolas", "Staircases & Rallyings"
            ]
            
            # Check if services table is empty
            cursor.execute("SELECT COUNT(*) as count FROM mt_services")
            count = cursor.fetchone()['count']
            
            if count == 0:
                # Insert Warehouse Equipments
                for item in warehouse_equipments:
                    cursor.execute(
                        "INSERT INTO mt_services (category, name, description, image_url) VALUES (%s, %s, %s, %s)",
                        ("Warehouse Equipments", item, f"Professional {item} designed for industrial use", f"static/images/services/{item.lower().replace(' ', '_')}.jpg")
                    )
                
                # Insert Pharmaceutical Fixtures
                for item in pharmaceutical_fixtures:
                    cursor.execute(
                        "INSERT INTO mt_services (category, name, description, image_url) VALUES (%s, %s, %s, %s)",
                        ("Pharmaceutical Fixtures", item, f"High-quality {item} for pharmaceutical industry", f"static/images/services/{item.lower().replace(' ', '_')}.jpg")
                    )
                
                # Insert Display Stands
                for item in display_stands:
                    cursor.execute(
                        "INSERT INTO mt_services (category, name, description, image_url) VALUES (%s, %s, %s, %s)",
                        ("Display Stands for Showrooms", item, f"Custom-designed {item} for retail displays", f"static/images/services/{item.lower().replace(' ', '_')}.jpg")
                    )
                
                # Insert Solar Panel Framing
                for item in solar_panel:
                    cursor.execute(
                        "INSERT INTO mt_services (category, name, description, image_url) VALUES (%s, %s, %s, %s)",
                        ("Solar Panel Framing", item, "Durable frames for solar panel installations", "static/images/services/solar_panel_framing.jpg")
                    )
                
                # Insert Premises Security
                for item in premises_security:
                    cursor.execute(
                        "INSERT INTO mt_services (category, name, description, image_url) VALUES (%s, %s, %s, %s)",
                        ("Premises Security", item, f"Robust {item} for complete security solutions", f"static/images/services/{item.lower().replace(' ', '_')}.jpg")
                    )
                
                # Insert General Fabrication
                for item in general_fabrication:
                    cursor.execute(
                        "INSERT INTO mt_services (category, name, description, image_url) VALUES (%s, %s, %s, %s)",
                        ("General Fabrication", item, f"Custom {item} fabricated to your specifications", f"static/images/services/{item.lower().replace(' ', '_')}.jpg")
                    )
            
            # Insert sample testimonials if empty
            cursor.execute("SELECT COUNT(*) as count FROM mt_testimonials")
            count = cursor.fetchone()['count']
            
            if count == 0:
                sample_testimonials = [
                    ("John Smith", "ABC Manufacturing", "Metaltech Engineering provided excellent warehouse equipment solutions for our facility. The quality of their work is outstanding.", 5),
                    ("Sarah Johnson", "PharmaCorp", "The pharmaceutical fixtures we ordered were delivered on time and matched our exact specifications. Highly recommended!", 5),
                    ("Michael Brown", "Retail Displays Inc", "Their display stands have transformed our showroom. Professional service from start to finish.", 4),
                    ("Emily Davis", "Green Energy Solutions", "The solar panel framing was exactly what we needed for our large installation project. Durable and well-designed.", 5),
                    ("Robert Wilson", "Security First", "Metaltech's security solutions have significantly improved our premises protection. Quality craftsmanship!", 4)
                ]
                
                for testimonial in sample_testimonials:
                    cursor.execute(
                        "INSERT INTO mt_testimonials (client_name, company, content, rating) VALUES (%s, %s, %s, %s)",
                        testimonial
                    )
            
            # Insert sample blog posts if empty
            cursor.execute("SELECT COUNT(*) as count FROM mt_blog_posts")
            count = cursor.fetchone()['count']
            
            if count == 0:
                sample_posts = [
                    ("Innovation in Warehouse Equipment Design", "Modern warehouse operations demand innovative equipment solutions. At Metaltech Engineering, we're constantly pushing the boundaries of design and functionality to create warehouse equipment that enhances efficiency and safety. Our latest developments include...", "Engineering Team", "static/images/blog/warehouse_innovation.jpg"),
                    ("Advancements in Pharmaceutical Fixture Materials", "The pharmaceutical industry requires fixtures that meet rigorous standards for cleanliness and durability. Our research into advanced materials has led to significant improvements in our product offerings...", "R&D Department", "static/images/blog/pharma_fixtures.jpg"),
                    ("Custom Display Solutions for Retail", "Creating the perfect retail display requires a balance of aesthetics and functionality. Our team recently completed a project for a high-end boutique that showcases how custom metalwork can transform a shopping experience...", "Design Team", "static/images/blog/retail_displays.jpg"),
                    ("Sustainable Practices in Metal Fabrication", "At Metaltech Engineering, we're committed to reducing our environmental footprint. Our new processes for metal fabrication minimize waste and energy consumption while maintaining the highest quality standards...", "Sustainability Officer", "static/images/blog/sustainable_fabrication.jpg"),
                    ("Security Solutions for Industrial Facilities", "Industrial security presents unique challenges that require specialized solutions. Our integrated approach combines physical barriers with modern security features to create comprehensive protection systems...", "Security Division", "static/images/blog/industrial_security.jpg")
                ]
                
                for post in sample_posts:
                    cursor.execute(
                        "INSERT INTO mt_blog_posts (title, content, author, image_url) VALUES (%s, %s, %s, %s)",
                        post
                    )
        
        db.commit()

# Define a context processor to add 'now' globally to all templates
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# Routes
@app.route('/')
def home():
    db = get_db()
    with db.cursor() as cursor:
        # Get service categories
        cursor.execute("SELECT DISTINCT category FROM mt_services")
        categories = cursor.fetchall()
        
        # Get one testimonial for homepage
        cursor.execute("SELECT * FROM mt_testimonials ORDER BY rating DESC LIMIT 1")
        featured_testimonial = cursor.fetchone()
        
        # Get quote for homepage
        quote = "Precision Engineering for Tomorrow's World"
        
    return render_template('index.html', 
                          categories=categories, 
                          featured_testimonial=featured_testimonial,
                          quote=quote)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/services')
def services():
    category = request.args.get('category', None)
    db = get_db()
    with db.cursor() as cursor:
        if category:
            cursor.execute("SELECT * FROM mt_services WHERE category = %s", (category,))
            services = cursor.fetchall()
            
            cursor.execute("SELECT DISTINCT category FROM mt_services")
            categories = cursor.fetchall()
            
            return render_template('services.html', services=services, categories=categories, selected_category=category)
        else:
            cursor.execute("SELECT DISTINCT category FROM mt_services")
            categories = cursor.fetchall()
            
            cursor.execute("SELECT * FROM mt_services")
            all_services = cursor.fetchall()
            
            return render_template('services.html', services=all_services, categories=categories)

@app.route('/testimonials')
def testimonials():
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute("SELECT * FROM mt_testimonials ORDER BY date_added DESC")
        all_testimonials = cursor.fetchall()
    
    return render_template('testimonials.html', testimonials=all_testimonials)

@app.route('/blog')
def blog():
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute("SELECT * FROM mt_blog_posts ORDER BY date_posted DESC")
        posts = cursor.fetchall()
    
    return render_template('blog.html', posts=posts)

@app.route('/blog/<int:post_id>')
def blog_post(post_id):
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute("SELECT * FROM mt_blog_posts WHERE id = %s", (post_id,))
        post = cursor.fetchone()
        
        if not post:
            flash('Blog post not found')
            return redirect(url_for('blog'))
        
        # Get related posts
        cursor.execute("SELECT * FROM mt_blog_posts WHERE id != %s ORDER BY date_posted DESC LIMIT 3", (post_id,))
        related_posts = cursor.fetchall()
    
    return render_template('blog_post.html', post=post, related_posts=related_posts)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')
        
        db = get_db()
        with db.cursor() as cursor:
            cursor.execute(
                "INSERT INTO mt_quotes (name, email, phone, message) VALUES (%s, %s, %s, %s)",
                (name, email, phone, message)
            )
        db.commit()
        
        flash('Your message has been sent. We will contact you shortly!')
        return redirect(url_for('contact'))
    
    return render_template('contact.html')

@app.route('/request_quote', methods=['GET', 'POST'])
def request_quote():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        service = request.form.get('service')
        message = request.form.get('message')
        
        db = get_db()
        with db.cursor() as cursor:
            cursor.execute(
                "INSERT INTO mt_quotes (name, email, phone, service, message) VALUES (%s, %s, %s, %s, %s)",
                (name, email, phone, service, message)
            )
        db.commit()
        
        flash('Your quote request has been submitted. Our team will reach out to you soon!')
        return redirect(url_for('home'))
    
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute("SELECT DISTINCT category FROM mt_services")
        categories = cursor.fetchall()
    
    return render_template('request_quote.html', categories=categories)

if __name__ == '__main__':
    with app.app_context():
        init_db()
    app.run(debug=True)