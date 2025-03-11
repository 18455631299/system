from app import app

# 这是Vercel的入口点
# Vercel expects a Flask application instance here
application = app

# 这是用于本地开发的部分，Vercel不会使用这部分
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)