# ------------------ Import Required Libraries ------------------
import streamlit as st          # Streamlit for creating interactive web app
import pandas as pd             # Pandas for handling tabular data
from io import BytesIO          # BytesIO for creating in-memory PDF files
from reportlab.lib.pagesizes import A4       # Standard page size for PDF
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
# platypus = Page Layout and Typography Using Scripts (used for PDF generation)
from reportlab.lib import colors             # To add colors in PDF
from reportlab.lib.styles import getSampleStyleSheet   # To apply default styles in PDF


# ------------------ Function to Calculate Grade ------------------
def calculate_grade(marks, max_marks=100):
    """
    This function calculates grade based on percentage.
    """
    percentage = (marks / max_marks) * 100   # Convert marks to percentage
    if percentage >= 85:
        return "A"
    elif percentage >= 70:
        return "B"
    elif percentage >= 55:
        return "C"
    elif percentage >= 40:
        return "D"
    elif percentage >= 35:
        return "E"
    else:
        return "F"


# ------------------ Function to Generate PDF ------------------
def create_pdf(project_name, student_name, guide, team_no, submission_date,
               results, total_marks, total_obtained, percentage, overall_grade, remark_text, evaluator):
    """
    This function generates a PDF report with project details, evaluation table, and remarks.
    """

    buffer = BytesIO()   # Create in-memory buffer to store PDF
    doc = SimpleDocTemplate(buffer, pagesize=A4)   # Define PDF template
    styles = getSampleStyleSheet()   # Load default text styles
    elements = []   # List to hold all PDF content (text, tables, etc.)

    # --- Heading Section ---
    # Add the company/institute name in bold, red, and large font (Title style)
    elements.append(Paragraph("<b><font size=18 color='red'>NEWGEN TECH PVT. LIMIT</font></b>", styles['Title']))
    # Add the company/institute address in normal style
    elements.append(Paragraph("123-Highstreet Lane, Fictional City, Downtown-568965", styles['Normal']))
    # Add a blank vertical space of 12 units for better formatting
    elements.append(Spacer(1, 12))  # Add space
    # Add the sub-heading "Project Grade 2025-26" in bold (Heading2 style)
    elements.append(Paragraph("<b>Project Grade 2025-26</b>", styles['Heading2']))
    # Again add space below the heading for neat layout
    elements.append(Spacer(1, 12))

    # --- Project/Student Details Section ---
    project_data = [
        ["Project ID:", project_name, "Evaluator:", evaluator],
        ["Student Name:", student_name, "Guide:", guide],
        ["Submission Date:", str(submission_date), "Team No:", team_no],
    ]
    project_table = Table(project_data, colWidths=[100, 150, 100, 150])  # Create table
    project_table.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 1, colors.black)]))  # Add grid lines
    elements.append(project_table)
    elements.append(Spacer(1, 20))

    # --- Evaluation Table (Criteria vs Marks) ---
    table_data = [["Criteria", "Max Marks", "Passing Marks", "Marks Obtained", "Grade"]] + results
    eval_table = Table(table_data, colWidths=[120, 100, 100, 120, 80])
    eval_table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 1, colors.black),         # Grid lines
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightblue),   # Blue header row
        ("ALIGN", (1, 1), (-1, -1), "CENTER"),               # Center alignment
    ]))
    elements.append(eval_table)
    elements.append(Spacer(1, 20))

    # --- Summary Section ---
    # Create a 2D list (table data) for the Summary section of the report
    summary_data = [
     # First row: shows Total Marks and Percentage
        ["Total Marks", str(total_marks), "Percentage", f"{percentage:.2f}%"],
     # Second row: shows Total Obtained and Overall Grade
        ["Total Obtained", str(total_obtained), "Overall Grade", overall_grade],
    ]
    # Create a table object using the summary_data
    # colWidths sets the width of each column in the table (in points)
    summary_table = Table(summary_data, colWidths=[120, 80, 120, 80])
    # Apply styling to the summary table
    summary_table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 1, colors.black),   # Add black borders (grid) around all cells
        ("BACKGROUND", (0, 0), (-1, -1), colors.beige) # Add black borders (grid) around all cells
    ]))
    # Add the summary table to the PDF elements list
    elements.append(summary_table)
    # Add some vertical space (20 units) after the table for better layout
    elements.append(Spacer(1, 20))

    # --- Remarks Section ---
    # Add the remark text (Pass/Fail message) in red color and bold inside the PDF
    elements.append(Paragraph(f"<b><font color='red'>{remark_text}</font></b>", styles['Normal']))

    # --- Build PDF Document ---
    # Build the final PDF document using all the elements added above
    doc.build(elements)
    buffer.seek(0) # Reset the file pointer to the beginning of the BytesIO buffer
    return buffer   # Reset the file pointer to the beginning of the BytesIO buffer

# ------------------ Streamlit Web App ------------------
st.set_page_config(page_title="Project Grade Report", layout="wide")

# Title & Subheading
st.title("📊 NEWGEN TECH PVT.LTD.")
st.subheader("Project Grade 2025-26")

# --- Project/Student Information Inputs ---
col1, col2 = st.columns(2)
with col1:
    project_name = st.text_input("Project ID", "Project Grading System")    # Input Project Name
    student_name = st.text_input("Student Name", "Jadhav Sonali")           # Input Student Name
    submission_date = st.date_input("Submission Date")                      # Date input
with col2:
    guide = st.text_input("Guide", "Vishnavi Ma'am")                        # Guide name
    team_no = st.text_input("Team No.", "4")                                # Team number
    evaluator = st.text_input("Evaluator", "Prof.Suraj Sir")                # Evaluator name

st.markdown("---")  # Divider line

# --- Marks Entry Section ---
st.subheader("Enter Marks (out of 100)")
criteria = ["Project Marks", "Performance", "Innovation", "Presentation"]   # Evaluation parameters

marks = {}
for crit in criteria:
    # For each criteria, take numeric input between 0 and 100
    marks[crit] = st.number_input(f"{crit}", min_value=0, max_value=100, value=50)


# ------------------ Processing Data ------------------
max_marks = 100             # Max marks per criteria
passing_marks = 35          # Passing marks
results = []                # Store results table
total_obtained = 0          # Sum of all marks
failed_criteria = []        # Store failed subjects

for crit, score in marks.items():# Loop through each evaluation criteria and its score
    grade = calculate_grade(score, max_marks)   # Calculate grade for each criteria
    total_obtained += score                     # Add score to total
    if score < passing_marks:                   # Check if failed
        failed_criteria.append(crit)            # Keep track of failed subjects/criteria
    results.append([crit, max_marks, passing_marks, score, grade])  # Store results row


# --- Convert results into DataFrame for display ---
df = pd.DataFrame(results, columns=["Criteria", "Max Marks", "Passing Marks", "Marks Obtained", "Grade"])
st.write("### Evaluation Table")
st.dataframe(df, use_container_width=True)   # Show interactive table


# ------------------ Summary Section ------------------
total_marks = len(criteria) * max_marks                 # Calculate total possible marks
percentage = (total_obtained / total_marks) * 100       # Calculate percentage
overall_grade = calculate_grade(total_obtained, total_marks)  # Final grade

# Show Summary in three columns
st.markdown("### 📌 Summary")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Marks", f"{total_obtained}/{total_marks}")  # Display marks
with col2:
    st.metric("Percentage", f"{percentage:.2f}%")                # Display percentage
with col3:
    st.metric("Overall Grade", overall_grade)                    # Display grade


# --- Remarks Section ---
if failed_criteria:
    remark_text = f"❌ Failed in: {', '.join(failed_criteria)}"   # Show failed subjects
else:
    remark_text = "✅ Pass in all criteria. Good Work!"           # Pass remark
st.markdown(f"**Remarks:** {remark_text}")


# ------------------ PDF Download Button ------------------
pdf_buffer = create_pdf(project_name, student_name, guide, team_no, submission_date,
                        results, total_marks, total_obtained, percentage, overall_grade, remark_text, evaluator)

st.download_button(
    label="⬇️ Download Report as PDF",   # Button text
    data=pdf_buffer,                     # PDF file data
    file_name=f"{student_name.replace(' ', '_')}_Report.pdf",  # Auto filename
    mime="application/pdf"               # File type
)
