from flask import Flask
import calendar
from datetime import date

app = Flask(__name__)

def get_next_month_dates():
    today = date.today()
    year = today.year
    month = today.month + 1 if today.month < 12 else 1
    year = year if today.month < 12 else year + 1

    c = calendar.Calendar(firstweekday=calendar.SATURDAY)
    month_days = c.itermonthdates(year, month)

    weekends = []
    weeks = []

    current_week = []
    for d in month_days:
        if d.month == month:
            # Weekends
            if d.weekday() in [5, 6]:  # Saturday=5, Sunday=6
                weekends.append({
                    "date": d.strftime("%d/%m/%Y"),
                    "day": d.strftime("%A"),
                    "support": "Full Day",
                    "resource": ""
                })
            current_week.append(d)

            # Weekly ranges
            if d.weekday() == 6:  # End of week (Sunday)
                weeks.append({
                    "range": f"{current_week[0].strftime('%d/%m/%Y')} --> {current_week[-1].strftime('%d/%m/%Y')}",
                    "primary": "",
                    "secondary": ""
                })
                current_week = []

    return weekends, weeks

@app.route("/next-month", methods=["GET"])
def next_month():
    weekends, weeks = get_next_month_dates()

    # Weekend Support table
    weekends_html = """
    <h3>Weekend Support</h3>
    <table border="1" cellpadding="5" cellspacing="0">
      <tr>
        <th>Date</th><th>Support</th><th>Day</th><th>Resource</th>
      </tr>
    """
    for w in weekends:
        weekends_html += f"<tr><td>{w['date']}</td><td>{w['support']}</td><td>{w['day']}</td><td>{w['resource']}</td></tr>"
    weekends_html += "</table>"

    # Primary/Secondary table
    weeks_html = """
    <h3>Primary / Secondary Weeks</h3>
    <table border="1" cellpadding="5" cellspacing="0">
      <tr><th>Date</th><th>Primary</th><th>Secondary</th></tr>
    """
    for wk in weeks:
        weeks_html += f"<tr><td>{wk['range']}</td><td>{wk['primary']}</td><td>{wk['secondary']}</td></tr>"
    weeks_html += "</table>"

    return weekends_html + "<br><br>" + weeks_html

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
