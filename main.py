from fpdf import FPDF
import pandas
from datetime import date
from random import randint
from dateutil import relativedelta

pdf = FPDF(orientation="P", unit="mm", format="A4")
pdf.set_auto_page_break(auto=False, margin=10)

# Set client data
invoice_nr = randint(1, 200000)
client_nr = randint(1, 10000)
invoice_date = date.today()
expiration_date = date.today() + relativedelta.relativedelta(months=1)

# Get data from csv file
products_dataframe = pandas.read_csv("files/products.csv")

# Create new page
pdf.add_page()

# Add logo
pdf.image("images/logo.PNG", w=40)

pdf.ln(15)

# Create sender details
pdf.set_font(family="Helvetica", size=8)
pdf.set_text_color(100, 100, 100)
pdf.cell(w=30, h=3, txt="Demo B.V", ln=1)
pdf.cell(w=30, h=3, txt="Demo Road 241", ln=1)
pdf.cell(w=30, h=3, txt="6446TK, Demo City", ln=20)

# Create header
pdf.set_font(family="Helvetica", size=20, style="B")
pdf.set_text_color(0, 0, 0)
pdf.cell(w=100, h=20, txt="Invoice", ln=1)

# Create client info with invoice data


# Create a output file
pdf.output("invoice.pdf")


