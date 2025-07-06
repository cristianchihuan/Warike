from flask import Flask, render_template, request, redirect, url_for, jsonify, session, flash, abort, make_response
import pymysql
from pymysql import Error
from werkzeug.security import generate_password_hash, check_password_hash
import os
import json
from datetime import datetime, timedelta

"""
Peruvian Warike Restaurant Management System
Flask web server that handles restaurant operations, orders, and user management.
All logic is handled server-side without JavaScript dependencies.
"""

app = Flask(__name__)
app.secret_key = 'peruvian-warike-secret-key-2025'
app.config['SESSION_PERMANENT'] = False
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=24)

# Database configuration
config = {
    'host': 'localhost',  # Change to your database host
    'port': 3306,
    'user': 'root',       # Change to your database user
    'password': '',       # Change to your database password
    'database': 'peruvian_warike_db',  # Change to your database name
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

# Restaurant configuration - Updated to match Peruvian Warike branding
RESTAURANT_INFO = {
    'name': 'Peruvian Warike',
    'phone': '(434) 845 - 0070',
    'email': 'info@peruvianwarike.com',
    'address': '1213 Greenview Dr, Lynchburg, VA 24502',
    'hours': {
        'mon_thu': '11:00 AM - 9:00 PM',
        'fri_sat': '11:00 AM - 9:30 PM',
        'sun': '11:00 AM - 8:00 PM'
    }
}

"""
Main route - serves the restaurant website
"""
@app.route('/')
def index():
    recent_orders = []
    if 'user_id' in session:
        try:
            conn = pymysql.connect(**config)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT o.*, u.username 
                FROM orders o 
                JOIN users u ON o.user_id = u.id 
                WHERE o.user_id = %s 
                ORDER BY o.created_at DESC
                LIMIT 3
            """, (session['user_id'],))
            
            orders = cursor.fetchall()
            for order in orders:
                order['items'] = json.loads(order['items'])
            recent_orders = orders
            
            cursor.close()
            conn.close()
        except Error as e:
            print(f"Error loading recent orders: {e}")
    
    return render_template('index.html', restaurant=RESTAURANT_INFO, recent_orders=recent_orders)

"""
User Authentication Routes
"""

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not email or not password:
            flash('Por favor completa todos los campos', 'error')
            return redirect(url_for('index') + '#signin')
        
        try:
            conn = pymysql.connect(**config)
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()
            cursor.close()
            conn.close()
            
            if user and check_password_hash(user['password'], password):
                session['user_id'] = user['id']
                session['username'] = user['username']
                session['email'] = user['email']
                flash('Inicio de sesión exitoso!', 'success')
                return redirect(url_for('index'))
            else:
                flash('Credenciales inválidas', 'error')
                return redirect(url_for('index') + '#signin')
                
        except Error as e:
            flash('Error de conexión', 'error')
            return redirect(url_for('index') + '#signin')
    
    return redirect(url_for('index') + '#signin')

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    flash('Sesión cerrada exitosamente', 'info')
    return redirect(url_for('index'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        phone = request.form.get('phone', '')
        address = request.form.get('address', '')
        
        if not username or not email or not password:
            flash('Por favor completa todos los campos requeridos', 'error')
            return redirect(url_for('signup'))
        
        try:
            conn = pymysql.connect(**config)
            cursor = conn.cursor()
            
            # Check if user already exists
            cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
            if cursor.fetchone():
                flash('El usuario ya existe', 'error')
                return redirect(url_for('signup'))
            
            # Hash password
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
            
            # Insert new user
            cursor.execute("""
                INSERT INTO users (username, email, password, phone, address)
                VALUES (%s, %s, %s, %s, %s)
            """, (username, email, hashed_password, phone, address))
            
            conn.commit()
            cursor.close()
            conn.close()
            
            flash('Cuenta creada exitosamente! Por favor inicia sesión.', 'success')
            return redirect(url_for('index') + '#signin')
            
        except Error as e:
            flash('Error al crear la cuenta', 'error')
            return redirect(url_for('signup'))
    
    return render_template('signup.html', restaurant=RESTAURANT_INFO)

"""
Menu and Order Routes
"""

@app.route('/menu')
def menu():
    try:
        conn = pymysql.connect(**config)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM menu_items 
            WHERE active = 1 
            ORDER BY category, name
        """)
        
        menu_items = cursor.fetchall()
        cursor.close()
        conn.close()
        
        # Group items by category
        menu_by_category = {}
        for item in menu_items:
            category = item['category']
            if category not in menu_by_category:
                menu_by_category[category] = []
            menu_by_category[category].append(item)
        
        return render_template('menu.html', restaurant=RESTAURANT_INFO, menu=menu_by_category)
        
    except Error as e:
        flash('Error al cargar el menú', 'error')
        return redirect(url_for('index'))

@app.route('/quick-order', methods=['GET', 'POST'])
def quick_order():
    if request.method == 'POST':
        if 'user_id' not in session:
            flash('Debes iniciar sesión para ordenar', 'error')
            return redirect(url_for('login'))
        
        # Get form data
        items = []
        total = 0
        
        for key, value in request.form.items():
            if key.startswith('item_') and value and int(value) > 0:
                item_id = key.replace('item_', '')
                quantity = int(value)
                
                # Get item details from database
                try:
                    conn = pymysql.connect(**config)
                    cursor = conn.cursor()
                    cursor.execute("SELECT * FROM menu_items WHERE id = %s", (item_id,))
                    item = cursor.fetchone()
                    cursor.close()
                    conn.close()
                    
                    if item:
                        items.append({
                            'id': item['id'],
                            'name': item['name'],
                            'price': float(item['price']),
                            'quantity': quantity
                        })
                        total += float(item['price']) * quantity
                except Error as e:
                    flash('Error al procesar el pedido', 'error')
                    return redirect(url_for('quick_order'))
        
        if not items:
            flash('El carrito está vacío', 'error')
            return redirect(url_for('quick_order'))
        
        # Create order
        try:
            conn = pymysql.connect(**config)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO orders (user_id, items, total_amount, status, delivery_address, phone)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                session['user_id'],
                json.dumps(items),
                total,
                'pending',
                request.form.get('delivery_address', ''),
                request.form.get('phone', '')
            ))
            
            conn.commit()
            cursor.close()
            conn.close()
            
            flash('¡Orden creada exitosamente!', 'success')
            return redirect(url_for('index'))
            
        except Error as e:
            flash('Error al crear la orden', 'error')
            return redirect(url_for('quick_order'))
    
    # GET request - show quick order form
    try:
        conn = pymysql.connect(**config)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM menu_items 
            WHERE active = 1 
            ORDER BY category, name
        """)
        
        menu_items = cursor.fetchall()
        cursor.close()
        conn.close()
        
        # Group items by category
        menu_by_category = {}
        for item in menu_items:
            category = item['category']
            if category not in menu_by_category:
                menu_by_category[category] = []
            menu_by_category[category].append(item)
        
        return render_template('quick_order.html', restaurant=RESTAURANT_INFO, menu=menu_by_category)
        
    except Error as e:
        flash('Error al cargar el menú', 'error')
        return redirect(url_for('index'))

@app.route('/reorder/<int:order_id>', methods=['POST'])
def reorder(order_id):
    if 'user_id' not in session:
        flash('Debes iniciar sesión para reordenar', 'error')
        return redirect(url_for('login'))
    
    try:
        conn = pymysql.connect(**config)
        cursor = conn.cursor()
        
        # Get original order
        cursor.execute("""
            SELECT * FROM orders 
            WHERE id = %s AND user_id = %s
        """, (order_id, session['user_id']))
        
        original_order = cursor.fetchone()
        if not original_order:
            flash('Orden no encontrada', 'error')
            return redirect(url_for('index'))
        
        # Create new order with same items
        cursor.execute("""
            INSERT INTO orders (user_id, items, total_amount, status, delivery_address, phone)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            session['user_id'],
            original_order['items'],
            original_order['total_amount'],
            'pending',
            original_order['delivery_address'],
            original_order['phone']
        ))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        flash('¡Reordenado exitosamente!', 'success')
        return redirect(url_for('index'))
        
    except Error as e:
        flash('Error al reordenar', 'error')
        return redirect(url_for('index'))

"""
Admin Routes
"""

@app.route('/admin')
def admin():
    if 'user_id' not in session:
        flash('Debes iniciar sesión para acceder al panel de administración', 'error')
        return redirect(url_for('login'))
    
    try:
        conn = pymysql.connect(**config)
        cursor = conn.cursor()
        
        # Get today's orders
        cursor.execute("""
            SELECT o.*, u.username 
            FROM orders o 
            JOIN users u ON o.user_id = u.id 
            WHERE DATE(o.created_at) = CURDATE()
            ORDER BY o.created_at DESC
        """)
        today_orders = cursor.fetchall()
        
        # Get analytics
        cursor.execute("""
            SELECT COUNT(*) as total_orders, SUM(total_amount) as total_revenue
            FROM orders 
            WHERE DATE(created_at) = CURDATE()
        """)
        today_stats = cursor.fetchone()
        
        cursor.execute("""
            SELECT status, COUNT(*) as count
            FROM orders 
            WHERE DATE(created_at) = CURDATE()
            GROUP BY status
        """)
        status_stats = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return render_template('admin.html', 
                             restaurant=RESTAURANT_INFO,
                             orders=today_orders,
                             stats=today_stats,
                             status_stats=status_stats)
        
    except Error as e:
        flash('Error al cargar datos de administración', 'error')
        return redirect(url_for('index'))

@app.route('/admin/order/<int:order_id>/status', methods=['POST'])
def update_order_status(order_id):
    if 'user_id' not in session:
        flash('No autorizado', 'error')
        return redirect(url_for('login'))
    
    new_status = request.form.get('status')
    if not new_status:
        flash('Estado requerido', 'error')
        return redirect(url_for('admin'))
    
    try:
        conn = pymysql.connect(**config)
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE orders 
            SET status = %s, updated_at = NOW() 
            WHERE id = %s
        """, (new_status, order_id))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        flash(f'Estado de orden actualizado a {new_status}', 'success')
        return redirect(url_for('admin'))
        
    except Error as e:
        flash('Error al actualizar estado', 'error')
        return redirect(url_for('admin'))

"""
Static Pages
"""

@app.route('/privacy')
def privacy():
    return render_template('privacy.html', restaurant=RESTAURANT_INFO)

@app.route('/terms')
def terms():
    return render_template('terms.html', restaurant=RESTAURANT_INFO)

"""
Database initialization route
"""
@app.route('/api/init-db', methods=['POST'])
def initialize_database():
    """Initialize database tables (run once for setup)"""
    try:
        conn = pymysql.connect(**config)
        cursor = conn.cursor()
        
        # Create users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(100) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                phone VARCHAR(20),
                address TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            )
        """)
        
        # Create menu_items table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS menu_items (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                description TEXT,
                price DECIMAL(10,2) NOT NULL,
                category VARCHAR(50) NOT NULL,
                image_url VARCHAR(255),
                active BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create orders table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT,
                items JSON NOT NULL,
                total_amount DECIMAL(10,2) NOT NULL,
                status ENUM('pending', 'confirmed', 'preparing', 'ready', 'delivered', 'cancelled') DEFAULT 'pending',
                delivery_address TEXT,
                phone VARCHAR(20),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)
        
        # Insert sample menu items with actual Peruvian Warike dishes
        sample_items = [
            ('Ceviche Peruano', 'Pescado fresco marinado en limón con cebolla y cilantro', 16.99, 'Platos Principales', '/static/images/menu/ceviche_peruano.jpg'),
            ('Seco de Pollo', 'Pollo guisado en salsa de cilantro con arroz y frijoles', 14.99, 'Platos Principales', '/static/images/menu/seco_de_pollo.jpg'),
            ('Hamburguesa Warike', 'Hamburguesa especial con sabores peruanos únicos', 13.99, 'Platos Principales', '/static/images/menu/hamburguesa_warike.jpg'),
            ('Leche de Tigre', 'Sopa de pescado con leche de tigre y mariscos', 18.99, 'Sopas', '/static/images/menu/leche_de_tigre.jpg'),
            ('Aeropuerto', 'Plato especial con arroz, papas fritas y carne', 15.99, 'Platos Principales', '/static/images/menu/aeropuerto.jpg'),
            ('Pescado a lo Macho', 'Pescado frito con salsa criolla y papas', 17.99, 'Platos Principales', '/static/images/menu/pescado_a_lo_macho.jpg'),
            ('Escabeche de Pollo', 'Pollo en escabeche con cebolla y vinagre', 13.99, 'Platos Principales', '/static/images/menu/escabeche_de_pollo.jpg')
        ]
        
        for item in sample_items:
            cursor.execute("""
                INSERT IGNORE INTO menu_items (name, description, price, category, image_url)
                VALUES (%s, %s, %s, %s, %s)
            """, item)
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({
            'success': True, 
            'message': 'Database initialized successfully with Peruvian Warike menu items'
        })
        
    except Error as e:
        return jsonify({'success': False, 'error': str(e)}), 500

"""
Error handlers
"""
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', restaurant=RESTAURANT_INFO), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html', restaurant=RESTAURANT_INFO), 500

"""
Health check route
"""
@app.route('/health')
def health_check():
    """Check if the application and database are running"""
    try:
        conn = pymysql.connect(**config)
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        cursor.fetchone()
        cursor.close()
        conn.close()
        
        return jsonify({
            'status': 'healthy',
            'database': 'connected',
            'timestamp': datetime.now().isoformat()
        })
    except Error as e:
        return jsonify({
            'status': 'unhealthy',
            'database': 'disconnected',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

if __name__ == '__main__':
    # Create templates and static directories if they don't exist
    if not os.path.exists('templates'):
        os.makedirs('templates')
    if not os.path.exists('static'):
        os.makedirs('static')
    
    # Move HTML file to templates directory
    if os.path.exists('index.html') and not os.path.exists('templates/index.html'):
        import shutil
        shutil.move('index.html', 'templates/index.html')
    
    # Move CSS file to static directory
    if os.path.exists('styles.css') and not os.path.exists('static/styles.css'):
        import shutil
        shutil.move('styles.css', 'static/styles.css')
    
    print("Peruvian Warike Restaurant Server")
    print("Starting Flask application...")
    print("Database config:", config)
    print("Access the website at: http://localhost:5000")
    print("All logic is handled server-side - no JavaScript required!")
    print("Using authentic Peruvian Warike images from menu folder!")
    
    app.run(debug=True, host='0.0.0.0', port=5000) 