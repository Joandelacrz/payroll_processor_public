from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
import os

def generate_paystub(row, country="do", company_name="Default Company"):
    pdf_path = f"/tmp/{row['full_name'].replace(' ', '_')}_paystub.pdf"
    c = canvas.Canvas(pdf_path, pagesize=letter)
    width, height = letter

    # 🚨 Texts for translation
    texts = {
        "do": {
            "paystub_title": f"{company_name} - Recibo de Pago",
            "employee": "Empleado",
            "email": "Correo Electrónico",
            "position": "Posición",
            "payment_details": "Detalles de Pago",
            "gross_salary": "Salario Bruto",
            "gross_payment": "Pago Bruto",
            "net_payment": "Pago Neto",
            "discounts": "Descuentos",
            "health_discount": "SFS",
            "social_discount": "AFP",
            "taxes_discount": "Descuento de Impuestos",
            "other_discounts": "Otros Descuentos",
            "period": "Período",
        },
        "USA": {
            "paystub_title": f"{company_name} - Paystub",
            "employee": "Employee",
            "email": "Email",
            "position": "Position",
            "payment_details": "Payment Details",
            "gross_salary": "Gross Salary",
            "gross_payment": "Gross Payment",
            "net_payment": "Net Payment",
            "discounts": "Discounts",
            "health_discount": "Health Discount",
            "social_discount": "Social Discount",
            "taxes_discount": "Taxes Discount",
            "other_discounts": "Other Discounts",
            "period": "Period",
        }
    }

    # Select language based on country
    lang = texts.get(country, texts["do"])  # Default to Spanish if country is invalid

    # 🚨 Adjusted logo path handling
    base_dir = os.path.dirname(os.path.abspath(__file__))  # Get current script directory
    images_dir = os.path.join(base_dir, "..", "images")    # Navigate up and into images folder

    # Construct logo paths
    company_logo_path = os.path.join(images_dir, f"{company_name}.png")
    default_logo_path = os.path.join(images_dir, "default.png")

    # Debugging: Print logo paths to verify
    print(f"Looking for company logo at: {company_logo_path}")
    print(f"Looking for default logo at: {default_logo_path}")

    # Check for logos in priority order
    logo_path = company_logo_path if os.path.exists(company_logo_path) else default_logo_path

    # Draw Logo (if found)
    logo_width = 3.0 * inch  # Width of the logo
    logo_height = 0.8 * inch  # Height of the logo
    logo_x = (width - logo_width) / 2  # Center the logo horizontally
    logo_y = height - 1.0 * inch  # Adjusted Y position (reduced space above the logo)

    if logo_path and os.path.exists(logo_path):
        try:
            c.drawImage(logo_path, logo_x, logo_y, width=logo_width, height=logo_height, mask="auto")
            print(f"Logo successfully added: {logo_path}")
        except Exception as e:
            print(f"Error drawing logo: {e}")

    # 🚨 Ensure text is placed properly
    text_x = inch  # X position for text
    text_y = logo_y - 0.5 * inch  # Adjusted Y position (text starts closer to the logo)
    line_spacing = 14  # Adjust spacing between lines

    # Company Name and Paystub Title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(text_x, text_y, lang["paystub_title"])
    text_y -= 20  # Move down

    # Separator Line
    c.setLineWidth(1)
    c.line(text_x, text_y, width - inch, text_y)
    text_y -= 20

    # Set text color
    c.setFillColorRGB(0, 0, 0)  # Black text

    # Employee Details
    c.setFont("Helvetica", 12)
    c.drawString(text_x, text_y, f"{lang['employee']}: {row.get('full_name', 'N/A')}")
    text_y -= line_spacing
    c.drawString(text_x, text_y, f"{lang['email']}: {row.get('email', 'N/A')}")
    text_y -= line_spacing
    c.drawString(text_x, text_y, f"{lang['position']}: {row.get('position', 'N/A')}")
    text_y -= (line_spacing * 2)

    # Payment Details
    c.setFont("Helvetica-Bold", 14)
    c.drawString(text_x, text_y, lang["payment_details"])
    text_y -= (line_spacing * 1.5)
    c.setFont("Helvetica", 12)
    c.drawString(text_x, text_y, f"{lang['gross_salary']}: {row.get('gross_salary', 'N/A')}")
    text_y -= line_spacing
    c.drawString(text_x, text_y, f"{lang['gross_payment']}: {row.get('gross_payment', 'N/A')}")
    text_y -= line_spacing
    c.drawString(text_x, text_y, f"{lang['net_payment']}: {row.get('net_payment', 'N/A')}")
    text_y -= (line_spacing * 2)

    # Discounts
    c.setFont("Helvetica-Bold", 14)
    c.drawString(text_x, text_y, lang["discounts"])
    text_y -= (line_spacing * 1.5)
    c.setFont("Helvetica", 12)
    c.drawString(text_x, text_y, f"{lang['health_discount']}: {row.get('health_discount_amount', 'N/A')}")
    text_y -= line_spacing
    c.drawString(text_x, text_y, f"{lang['social_discount']}: {row.get('social_discount_amount', 'N/A')}")
    text_y -= line_spacing
    c.drawString(text_x, text_y, f"{lang['taxes_discount']}: {row.get('taxes_discount_amount', 'N/A')}")
    text_y -= line_spacing
    c.drawString(text_x, text_y, f"{lang['other_discounts']}: {row.get('other_discount_amount', 'N/A')}")
    text_y -= (line_spacing * 2)

    # Period
    c.setFont("Helvetica-Bold", 14)
    c.drawString(text_x, text_y, lang["period"])
    text_y -= (line_spacing * 1.5)
    c.setFont("Helvetica", 12)
    c.drawString(text_x, text_y, f"{row.get('period', 'N/A')}")
    text_y -= line_spacing

    # 🚨 Remove `showPage()` before saving, to prevent blank pages
    c.save()

    if not os.path.exists(pdf_path):
        raise Exception("PDF not created.")
    return pdf_path