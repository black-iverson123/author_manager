# 📚 Author Manager API

**Author Manager API** is a backend service built with **Python (Flask)** that allows you to create, manage, and retrieve author profiles and their written works or publications.  
It’s designed with a clean, scalable structure suitable for real-world applications, with support for **MySQL** (development), **SQLite** (testing), and ready deployment to platforms like **Render** or **Heroku**.

---

## 🚀 Features

- 🧑‍💻 **Author Management** – Create, read, update, and delete author profiles.  
- 📚 **Book Linking** – Associate books and content with authors.  
- 🔐 **JWT Authentication** – Secure endpoints and protect sensitive data.  
- 🗄️ **Database Ready** – Works with MySQL (development) and SQLite (testing).  
- 📜 **Auto-Generated Docs** – Swagger/OpenAPI documentation support.  
- ☁️ **Deployment-Ready** – Easily deployable to Render, Heroku, or Docker.

---

## 🏗️ Project Structure

```
author_manager/
├── src/
│   ├── api/           # Flask blueprints and API routes
│   ├── docs/          # Swagger/OpenAPI documentation
│   ├── images/        # Static assets (optional)
│   ├── migrations/    # Database migration files
│   ├── main.py        # App factory / entry point
│   └── run.py         # Development server script
├── requirements.txt   # Python dependencies
├── Procfile           # Deployment config
├── .gitignore         # Git ignore rules
└── README.md          # Project documentation
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the repository

```bash
git clone https://github.com/black-iverson123/author_manager.git
cd author_manager
```

### 2️⃣ Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🛠️ Configuration

Create a `.env` file in the project root with the following variables:

```env
FLASK_ENV=development
SECRET_KEY=your_secret_key
DATABASE_URL=mysql+pymysql://user:password@localhost/author_manager_db
TEST_DATABASE_URL=sqlite:///test.db
JWT_SECRET_KEY=your_jwt_secret
```

---

## ▶️ Running the Application

### Development Server
```bash
python src/run.py
```

or using Flask CLI:

```bash
flask --app src/main.py run
```

The server will start on:  
`http://127.0.0.1:5000`

---

## 🧪 Running Tests

```bash
pytest
```

Make sure your `TEST_DATABASE_URL` points to a SQLite database for isolated test runs.

---

## 🗃️ Database Migrations

```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

---

## 📜 API Documentation

Swagger docs will be available at:

```
http://127.0.0.1:5000/docs
```

---

## ☁️ Deployment

### Deploying to Render or Heroku

- Ensure you have a `Procfile`:

```
web: gunicorn src.main:app
```

- Commit and push your code:

```bash
git add .
git commit -m "Deploy: initial version"
git push heroku master
```

- Set environment variables in the hosting dashboard (like `DATABASE_URL`, `JWT_SECRET_KEY`, etc.)

---

## 🧰 Tech Stack

- **Backend:** Python, Flask  
- **Database:** MySQL (development), SQLite (testing)  
- **ORM:** SQLAlchemy  
- **Authentication:** JWT  
- **Serialization:** Marshmallow  
- **Documentation:** Swagger/OpenAPI  

---

## 🤝 Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request to improve features, fix bugs, or enhance documentation.

---

## 📄 License

This project is licensed under the **MIT License**. See [LICENSE](LICENSE) for more information.

---

## 👨‍💻 Author

**Adebowale Obalanlege**  
- 💼 Backend Developer | Data Enthusiast  
- 📧 maxwelladebowale6@gmail.com  
- 🌐 [GitHub](https://github.com/black-iverson123) | [Project Repo](https://github.com/black-iverson123/author_manager)

---

### ⭐️ If you find this project helpful, give it a star on GitHub to support future development!
