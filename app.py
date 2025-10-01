from flask import Flask
import calendar
from datetime import date, timedelta

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
            if d.weekday() in [5, 6]:  # Saturday=5, Sunday=6
                weekends.append((d.strftime("%d/%m/%Y"), d.strftime("%A")))
            current_week.append(d)
            if d.weekday() == 6:  # End of week
                weeks.append((current_week[0].strftime('%d/%m/%Y'),
                              current_week[-1].strftime('%d/%m/%Y')))
                current_week = []

    return weekends, weeks

@app.route("/next-month", methods=["GET"])
def next_month():
    weekends, weeks = get_next_month_dates()

    # Build HTML tables
    weekends_html = "<h3>Weekend Support</h3><table border='1' cellpadding='5'><tr><th>Date</th><th>Day</th></tr>"
    for d, day in weekends:
        weekends_html += f"<tr><td>{d}</td><td>{day}</td></tr>"
    weekends_html += "</table>"

    weeks_html = "<h3>Primary/Secondary Weeks</h3><table border='1' cellpadding='5'><tr><th>Range</th></tr>"
    for start, end in weeks:
        weeks_html += f"<tr><td>{start} --> {end}</td></tr>"
    weeks_html += "</table>"

    return weekends_html + "<br><br>" + weeks_html

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
