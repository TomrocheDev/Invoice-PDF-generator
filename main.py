from fpdf import FPDF
import pandas
from datetime import date
from random import randint
from dateutil import relativedelta

pdf = FPDF(orientation="P", unit="mm", format="A4")
pdf.set_auto_page_break(auto=False, margin=10)


def client_cred_fat(title):
    pdf.set_font(family="Helvetica", style="B", size=9)
    pdf.cell(w=30, h=4, txt=title, ln=0)


def client_cred_normal(data_item):
    pdf.set_font(family="Helvetica", size=9)
    pdf.cell(w=30, h=4, txt=data_item, ln=1)


# Set client data
invoice_nr = str(randint(1, 200000))
client_nr = str(randint(1, 10000))
invoice_date = str(date.today())
expiration_date = str(date.today() + relativedelta.relativedelta(months=1))

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
pdf.cell(w=30, h=3, txt="6446TK, Demo City", ln=1)

pdf.ln(10)

# Create header
pdf.set_font(family="Helvetica", size=16, style="B")
pdf.set_text_color(0, 0, 0)
pdf.cell(w=100, h=15, txt="Invoice", ln=1)

# Create client info with invoice data
client_cred_fat("Invoice number: ")
client_cred_normal(invoice_nr)
client_cred_fat("Client number: ")
client_cred_normal(client_nr)
client_cred_fat("Invoice date: ")
client_cred_normal(invoice_date)
client_cred_fat("Expiration date: ")
client_cred_normal(expiration_date)

pdf.ln(10)

pdf.set_draw_color(r=80, g=80, b=80)
pdf.line(11, 111, 200, 111)
pdf.line(11, 117, 200, 117)

# Create table with used services
## Create table header
pdf.set_font(family="Helvetica", style="B", size=9)
pdf.cell(w=90, h=8, txt="Name/Description")
pdf.cell(w=20, h=8, txt="Quantity", ln=0)
pdf.cell(w=20, h=8, txt="Price", ln=0)
pdf.cell(w=20, h=8, txt="Tax", ln=0)
pdf.cell(w=20, h=8, txt="Total Price", ln=1)

# Table content loaded from CSV file
total_amounts = []

for index, item in products_dataframe.iterrows():
    pdf.set_font(family="Helvetica", size=8)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(w=90, h=5, txt=str(item["Name/Description"]))
    pdf.cell(w=20, h=5, txt=str(item["Quantity"]).replace(".", ","), ln=0)
    pdf.cell(w=20, h=5, txt=chr(128) + str(item["Price"]), ln=0)
    pdf.cell(w=20, h=5, txt=str(item["Tax"]) + "%", ln=0)
    pdf.cell(w=20, h=5, txt=chr(128) + str(item["Price"] * item["Quantity"]), ln=1)
    total_amounts.append(item["Price"] * item["Quantity"])

pdf.ln(8)

# Create table with applied taxes
amount_excl_tax = sum(total_amounts)
rounded_amount_excl_tax = str(round(amount_excl_tax, 2))
tax = (sum(total_amounts) / 100) * 21
rounded_tax = str(round(tax, 2))
total_amount_incl_tax = sum(total_amounts) + (sum(total_amounts) / 100) * 21
rounded_total_amount_incl_tax = str(round(total_amount_incl_tax, 2))

pdf.set_font(family="Helvetica", size=9)
pdf.set_text_color(40, 40, 40)
pdf.cell(w=40, h=5, txt="Total price excl. tax: ", ln=0)
pdf.cell(w=100, h=5, txt=chr(128) + rounded_amount_excl_tax, ln=1)
pdf.cell(w=40, h=5, txt="Tax: ", ln=0)
pdf.cell(w=100, h=5, txt=chr(128) + rounded_tax, ln=1)

pdf.ln(4)

pdf.line(11, 157, 100, 157)

pdf.cell(w=40, h=5, txt="Total amount incl. tax: ", ln=0)
pdf.set_font(family="Helvetica", style="B")
pdf.cell(w=100, h=5, txt=chr(128) + rounded_total_amount_incl_tax, ln=1)

pdf.ln(10)

# Ask for payment
message = f"""We kindly ask you to fulfill the payment before {expiration_date}. Our bank account number: 
NL123456789123456. 
"""

pdf.set_font(family="Helvetica", size=9)
pdf.cell(w=0, h=5, txt=message, ln=1)
pdf.cell(w=0, h=5, txt="Make sure you reference your invoice number.", ln=1)

pdf.ln(95)

# Create footer
footer = "Company: Demo B.V.     -     Bank account: NL123456789123456     -     Phone: +31 12345678     -     " \
         "Email: tom.roche@demobv.com"

pdf.set_font(family="Helvetica")
pdf.set_text_color(100, 100, 100)
pdf.cell(w=0, h=10, txt=footer, align="L", ln=0)

# Create a output file
pdf.output("demo invoice/demo_invoice.PDF")


