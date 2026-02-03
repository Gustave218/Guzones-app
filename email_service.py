from email.mime import message
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.utils import formataddr
from config import EMAIL_HOST, EMAIL_PORT, EMAIL_USER, EMAIL_PASS, ADMIN_EMAIL, TEAM_EMAILS


def send_order_notification(order, items, user, currency):

    # ---- USER INFO ----
    full_name = user.name if user else "Customer"
    email = user.email if user and user.email else "Not provided"
    phone = user.whatsapp if user and user.whatsapp else "Not provided"

    # ---- TOTAL ----
    total = order.total_amount

    # ---- ITEMS ----
    items_text = ""
    for item in items:
        product = item["product"]
        qty = item["quantity"]
        subtotal = item["subtotal"]

        product_name = (
    getattr(product, "name_en", None)
    or getattr(product, "name_fr", None)
    or "Product"
)

        items_text += f"- {product_name} x {qty} = {subtotal} {currency}\n"

    # ---- EMAIL BODY ----
    body = f"""
NEW ORDER - GUZONES

Order ID: {order.id}

Customer Name: {full_name}
Customer Email: {email}
Phone: {phone}

Total Amount: {total} {currency}

Items:
{items_text}

Payment Status: Pending for confirmation
Login to admin panel to view more details and confirm payment.
"""

    # ---- EMAIL SETUP ----
    msg = MIMEMultipart()
    msg["From"] = formataddr((str(Header("Guzones", "utf-8")), EMAIL_USER))
    msg["To"] = ADMIN_EMAIL
    msg["Cc"] = ", ".join(TEAM_EMAILS)
    msg["Subject"] = Header("New Order on Guzones", "utf-8")

    msg.attach(MIMEText(body, "plain", "utf-8"))

    recipients = [ADMIN_EMAIL] + TEAM_EMAILS

    # ---- SEND EMAIL ----
    server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
    server.starttls()
    server.login(EMAIL_USER, EMAIL_PASS)
    server.sendmail(EMAIL_USER, recipients, msg.as_bytes())
    server.quit()

def send_chat_notification(user, message_text):

    full_name = user.name if user else "Unknown"
    email = user.email if user and user.email else "Not provided"
    phone = user.whatsapp if user and user.whatsapp else "Not provided"

    body = f"""
GUZONES MESSAGE

A message has been submitted

User: {full_name}
Email: {email}
Phone: {phone}



Login to the admin panel to reply.
"""

    msg = MIMEMultipart()
    msg["From"] = formataddr((str(Header("Guzones", "utf-8")), EMAIL_USER))
    msg["To"] = ADMIN_EMAIL
    msg["Cc"] = ", ".join(TEAM_EMAILS)
    msg["Subject"] = Header("Guzones message", "utf-8")

    msg.attach(MIMEText(body, "plain", "utf-8"))

    recipients = [ADMIN_EMAIL] + TEAM_EMAILS

    server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
    server.starttls()
    server.login(EMAIL_USER, EMAIL_PASS)
    server.sendmail(EMAIL_USER, recipients, msg.as_bytes())
    server.quit()

    

    def send_user_chat_notification(user, message):
     if not user.email:
        return  # user has no email

    subject = "You have a new message from Guzones team"

    body = f"""
Hello {user.name},

You have a new message from Guzones team:


Please log in to your Guzones app to reply.

Thank you for shopping with Guzones 💙
"""

    msg = MIMEMultipart()
    msg["From"] = formataddr((str(Header("Guzones", "utf-8")), EMAIL_USER))
    msg["To"] = user.email
    msg["Subject"] = Header(subject, "utf-8")

    msg.attach(MIMEText(body, "plain", "utf-8"))

    server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
    server.starttls()
    server.login(EMAIL_USER, EMAIL_PASS)
    server.sendmail(EMAIL_USER, [user.email], msg.as_bytes())
    server.quit()

    