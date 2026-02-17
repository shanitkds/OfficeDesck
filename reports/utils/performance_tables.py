from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
import calendar


def performance_list_table(queryset):
    """
    Creates a PDF table for performance list reports
    """

    # 🔹 Table Header
    table_data = [[
        "Employee",
        "Employee ID",
        "Department",
        "Team Lead",
        "Month & Year",
        "Attendance",
        "Task",
        "Review",
        "Final",
        "Level",
    ]]

    # 🔹 Table Rows
    for obj in queryset:
        month_name = calendar.month_name[obj.month]  # ✅ month number → word

        table_data.append([
            obj.employee.name,
            obj.employee.employee_id,
            obj.employee.employee.department if obj.employee.employee.department else "-",
            obj.team_lead.name if obj.team_lead else "-",
            f"{month_name} {obj.year}",                 # ✅ Month + Year
            obj.attendance_score,
            obj.task_score,
            obj.review_score,
            obj.final_score,
            obj.performance_level,
        ])

    # 🔹 Create Table
    table = Table(table_data, repeatRows=1)

    # 🔹 Style
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("ALIGN", (4, 1), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
    ]))

    return table
