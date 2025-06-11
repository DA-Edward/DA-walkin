# Customer Management System

A streamlit-based customer management system optimized for iPad with a public form and password-protected backend.

## Features

- **Public Customer Form**: Customers can submit their information (name, phone, date, time, notes)
- **Live Queue Management**: Real-time queue with ability to assign customers
- **Customer Database**: Complete customer management system
- **iPad Optimized**: Responsive design optimized for iPad use
- **Navy Blue Theme**: Professional navy blue color scheme
- **Logo Support**: Display your custom logo (1453x905 recommended)

## Setup Instructions

### 1. Local Development

1. Clone this repository:
```bash
git clone <your-repo-url>
cd customer-management-system
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Add your logo:
   - Place your logo file as `logo.jpg` in the root directory
   - Recommended size: 1453x905 pixels

4. Run the application:
```bash
streamlit run main.py
```

### 2. Streamlit Cloud Deployment

1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Deploy the app

### 3. Configuration

- **Backend Password**: Default is `admin123` (change in `main.py` line 191)
- **Logo**: Place your logo as `logo.jpg` in the root directory
- **Data Storage**: Uses JSON files (`live_queue.json`, `customers.json`)

## Usage

### Public Form
- Customers access the main page to submit their information
- Form includes: Name, Phone, Date, Time, Notes
- Automatically adds to both live queue and customer database

### Backend Access
- Click the 🔧 button on the public form
- Enter password (default: `admin123`)
- Access live queue and customer management

### Live Queue
- View waiting customers
- Assign customers (removes from queue)
- See estimated wait times
- Clear queue option

### Customer Management
- View all customers
- Search functionality
- Export to CSV
- Clear database option

## File Structure

```
customer-management-system/
├── main.py              # Main Streamlit application
├── requirements.txt     # Python dependencies
├── README.md           # This file
├── logo.jpg            # Your logo (add this)
├── live_queue.json     # Live queue data (auto-generated)
└── customers.json      # Customer database (auto-generated)
```

## Customization

### Colors
The app uses a navy blue theme. To change colors, modify the CSS in the `st.markdown()` section in `main.py`.

### Password
Change the backend password in `main.py` line 191:
```python
if password == "your_new_password":
```

### Logo
Replace `logo.jpg` with your logo file. The app will automatically display it.

## iPad Optimization

The app is specifically optimized for iPad use with:
- Touch-friendly button sizes
- Responsive layout
- Proper font sizes for mobile viewing
- Optimized form inputs

## Data Storage

- **Live Queue**: `live_queue.json` - Stores current queue
- **Customers**: `customers.json` - Stores all customer data
- **Format**: JSON with automatic timestamping and ID generation

## Security Notes

- Change the default password before deployment
- Consider implementing proper authentication for production use
- Data is stored in JSON files - consider database integration for large-scale use

## Support

For issues or questions, please create an issue in the GitHub repository.