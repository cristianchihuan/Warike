# Peruvian Warike Restaurant Website

A modern, mobile-first restaurant website for **Peruvian Warike** featuring authentic Peruvian cuisine. Built with Flask and styled with a beautiful light blue color theme inspired by the restaurant's Facebook branding.

## 🌟 Features

- **Mobile-First Design**: Responsive layout optimized for mobile devices
- **Light Blue Theme**: Beautiful color scheme matching Peruvian Warike's branding
- **Server-Side Logic**: All functionality handled in Python/Flask (no JavaScript dependencies)
- **User Authentication**: Sign up, login, and session management
- **Menu System**: Complete menu with categories and pricing
- **Order Management**: Place orders, track status, and reorder functionality
- **Admin Panel**: Order management and analytics for restaurant staff
- **Database Integration**: MySQL database with PyMySQL for Windows compatibility

## 🎨 Design Features

- **Hero Section**: Eye-catching landing area with call-to-action buttons
- **Menu Preview**: Featured dishes with high-quality food images
- **Light Blue Color Palette**: 
  - Primary: `#4A90E2` (Light Blue)
  - Secondary: `#357ABD` (Darker Blue)
  - Accent: `#E3F2FD` (Light Blue Background)
- **Modern UI Elements**: Cards, gradients, shadows, and smooth animations
- **Peruvian Cuisine Focus**: Authentic dishes like Pollo a la Brasa, Lomo Saltado, and Ceviche

## 🛠️ Technology Stack

- **Backend**: Flask (Python)
- **Database**: MySQL with PyMySQL
- **Frontend**: HTML5, CSS3, Minimal JavaScript
- **Styling**: Custom CSS with Poppins font
- **Icons**: Font Awesome 6
- **Images**: Unsplash high-quality food photography

## 📱 Mobile-First Features

- Responsive navigation with hamburger menu
- Touch-friendly buttons and forms
- Optimized layouts for all screen sizes
- Fast loading and smooth interactions

## 🚀 Quick Start

### Prerequisites

- Python 3.7+
- MySQL Server
- pip (Python package manager)

### Installation

1. **Clone or download the project files**

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up MySQL database**:
   - Create a new MySQL database named `peruvian_warike_db`
   - Update database credentials in `app.py` if needed

4. **Initialize the database**:
   ```bash
   python app.py
   ```
   Then visit `http://localhost:5000/api/init-db` in your browser to create tables

5. **Run the application**:
   ```bash
   python app.py
   ```

6. **Access the website**:
   Open your browser and go to `http://localhost:5000`

## 📋 Database Setup

The application uses PyMySQL for better Windows compatibility. The database includes:

- **Users table**: Customer accounts and authentication
- **Menu items table**: Restaurant menu with categories and pricing
- **Orders table**: Order tracking and management

Sample menu items are automatically added during initialization.

## 🍽️ Menu Categories

- **Platos Principales**: Main dishes (Pollo a la Brasa, Lomo Saltado)
- **Entradas**: Appetizers (Ceviche)
- **Bebidas**: Beverages (Chicha Morada)
- **Postres**: Desserts (Tres Leches)

## 🔧 Configuration

### Database Configuration
Edit the `config` dictionary in `app.py`:
```python
config = {
    'host': 'localhost',
    'port': 3306,
    'user': 'your_username',
    'password': 'your_password',
    'database': 'peruvian_warike_db',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}
```

### Restaurant Information
Update restaurant details in `app.py`:
```python
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
```

## 📁 Project Structure

```
peruvian-warike/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── static/
│   └── styles.css        # Main stylesheet with light blue theme
└── templates/
    ├── index.html        # Homepage with hero section
    ├── menu.html         # Full menu page
    ├── quick_order.html  # Quick order form
    └── signup.html       # User registration
```

## 🎯 Key Features

### For Customers
- Browse complete menu with photos and descriptions
- Create account and manage orders
- Place quick orders for popular items
- Track order status
- Reorder previous meals
- View restaurant hours and contact information

### For Restaurant Staff
- Admin panel for order management
- Real-time order status updates
- Daily order analytics
- Customer order history

## 🌐 Routes

- `/` - Homepage with hero section and featured dishes
- `/menu` - Complete menu with all categories
- `/quick-order` - Quick order form for popular items
- `/signup` - User registration
- `/admin` - Admin panel (requires login)
- `/login` - User authentication
- `/logout` - Session termination

## 🎨 Color Scheme

The website uses a cohesive light blue color palette:

- **Primary Blue**: `#4A90E2` - Main brand color
- **Dark Blue**: `#357ABD` - Secondary color for gradients
- **Light Blue Background**: `#E3F2FD` - Subtle backgrounds
- **White**: `#FFFFFF` - Clean backgrounds
- **Dark Text**: `#333333` - Readable text
- **Gray Text**: `#666666` - Secondary text

## 📱 Responsive Breakpoints

- **Mobile**: < 768px (default)
- **Tablet**: 768px - 1024px
- **Desktop**: > 1024px

## 🔒 Security Features

- Password hashing with Werkzeug
- Session management
- SQL injection prevention
- Input validation and sanitization

## 🚀 Deployment

The application is ready for deployment on:
- Heroku
- DigitalOcean
- AWS
- Any Python hosting platform

## 📞 Support

For technical support or questions about the Peruvian Warike website, contact the development team.

---

**Peruvian Warike** - Auténtica Cocina Peruana en Lynchburg, VA
*Authentic Peruvian Cuisine in the Heart of Lynchburg* 