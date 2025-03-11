import datetime
from flask import render_template, request, redirect, url_for, flash
from app import app, db
from models import Submission, Note

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
