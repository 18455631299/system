from app import app

# Vercel会使用这个变量
application = app

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
