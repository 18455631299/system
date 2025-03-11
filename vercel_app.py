import os
import datetime
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
import urllib.parse

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# 创建Flask应用
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "vehicle_scheduling_system_secret_key")

# 获取数据库URL
database_url = os.environ.get("DATABASE_URL")

# 修复Heroku和Vercel上的postgres://格式
if database_url and database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

# 配置PostgreSQL数据库
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# 初始化数据库
db.init_app(app)

# 模型定义
class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.String(50))  # 格式如 "2025-03-10 08:00 (Monday)"
    end_date = db.Column(db.String(50))    # 格式如 "2025-03-10 12:00 (Monday)"
    driver = db.Column(db.String(50))
    plate = db.Column(db.String(50))
    brand = db.Column(db.String(50))
    vtype = db.Column(db.String(50))

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)

# Vehicle information list
vehicles = [
    {"plate": "皖A09AD1", "brand": "奥迪A6", "vtype": "小轿车"},
    {"plate": "皖A08222", "brand": "别克君威", "vtype": "小轿车"},
    {"plate": "皖AQQ007", "brand": "奥迪Q7", "vtype": "越野车"},
    {"plate": "皖AQQ882", "brand": "别克君越", "vtype": "轿车"}
]

# Driver information list, with an added "陈祖国、王磊" option
drivers = ["陈祖国", "王磊", "陈祖国、王磊"]

def parse_flatpickr_datetime(dt_str):
    """
    Parse Flatpickr datetime string (e.g., "2025-03-10 08:00") to datetime object
    """
    try:
        return datetime.datetime.strptime(dt_str, "%Y-%m-%d %H:%M")
    except ValueError:
        return None

def format_datetime_with_weekday(dt_str):
    """
    Convert "2025-03-10 08:00" to "2025-03-10 08:00 (周X)" format
    """
    dt = parse_flatpickr_datetime(dt_str)
    if dt:
        weekdays = ["一", "二", "三", "四", "五", "六", "日"]
        w = dt.weekday()  # 0 is Monday, 6 is Sunday
        return dt.strftime("%Y-%m-%d %H:%M") + f" (周{weekdays[w]})"
    return dt_str

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Determine if submitting vehicle record or custom note
        if "start_date" in request.form:
            # Vehicle record submission
            start_date_str = request.form.get("start_date", "")  # e.g., "2025-03-10 08:00"
            end_date_str = request.form.get("end_date", "")
            driver = request.form.get("driver", "")
            plate = request.form.get("plate", "")

            # Format dates (with weekday)
            formatted_start = format_datetime_with_weekday(start_date_str)
            formatted_end = format_datetime_with_weekday(end_date_str)

            # Find vehicle information based on plate number
            selected_vehicle = next((v for v in vehicles if v["plate"] == plate), None)
            brand = selected_vehicle["brand"] if selected_vehicle else ""
            vtype = selected_vehicle["vtype"] if selected_vehicle else ""

            # Create and save record
            new_submission = Submission(
                start_date=formatted_start,
                end_date=formatted_end,
                driver=driver,
                plate=plate,
                brand=brand,
                vtype=vtype
            )
            db.session.add(new_submission)
            db.session.commit()
            flash("用车记录提交成功", "success")
        elif "note_content" in request.form:
            # Custom note submission
            note_content = request.form.get("note_content", "").strip()
            if note_content:
                new_note = Note(content=note_content)
                db.session.add(new_note)
                db.session.commit()
                flash("自定义备注保存成功", "success")
        return redirect(url_for('index'))

    submissions = Submission.query.order_by(Submission.id.desc()).all()
    notes = Note.query.order_by(Note.id.desc()).all()
    
    return render_template('index.html', drivers=drivers, vehicles=vehicles,
                            submissions=submissions, notes=notes)

@app.route("/delete/<int:submission_id>")
def delete_submission(submission_id):
    submission = Submission.query.get_or_404(submission_id)
    db.session.delete(submission)
    db.session.commit()
    flash("记录已删除", "success")
    return redirect(url_for('index'))

@app.route("/delete_note/<int:note_id>")
def delete_note(note_id):
    note = Note.query.get_or_404(note_id)
    db.session.delete(note)
    db.session.commit()
    flash("备注已删除", "success")
    return redirect(url_for('index'))

# 创建数据库表
with app.app_context():
    db.create_all()

# Vercel需要的入口点
app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True

# 这是用于本地开发的部分，Vercel不会使用这部分
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)