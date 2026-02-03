from datetime import datetime
from flask_login import UserMixin
from extensions import db
from datetime import datetime
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash



# --------------------
# USER MODEL
# --------------------
class User(UserMixin, db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    whatsapp = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=True)
    address = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(200), nullable=False)

    role = db.Column(db.String(20), default="user")  # user | admin | superadmin
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    orders = db.relationship(
        "Order",
        backref="user",
        lazy=True,
        cascade="all, delete-orphan"
    )


class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)

    # null = notification for all users
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)

    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# --------------------
# CATEGORY MODEL
# --------------------
class Category(db.Model):
    __tablename__ = "category"

    id = db.Column(db.Integer, primary_key=True)
    name_en = db.Column(db.String(100), nullable=False)
    name_fr = db.Column(db.String(100), nullable=False)

    icon = db.Column(db.String(50), nullable=True)  # ✅ MUST be nullable
    image = db.Column(db.String(200), nullable=True)

    products = db.relationship("Product", backref="category", lazy=True)



# --------------------
# PRODUCT MODEL
# --------------------

class Product(db.Model):
    __tablename__ = "product"

    id = db.Column(db.Integer, primary_key=True)

    name_en = db.Column(db.String(200), nullable=False)
    name_fr = db.Column(db.String(200), nullable=True)

    description_en = db.Column(db.Text, nullable=False)
    description_fr = db.Column(db.Text, nullable=True)

    price = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(10), default="USD")  # ✅ DEFAULT USD
    shop_name = db.Column(db.String(120), nullable=True)
    shop_location = db.Column(db.String(120), nullable=True)
    category_id = db.Column(
        db.Integer,
        db.ForeignKey("category.id"),
        nullable=False
    )

    # 🔥 PRODUCT FLAGS (BADGES)
    is_new = db.Column(db.Boolean, default=False)
    is_trending = db.Column(db.Boolean, default=False)
    is_featured = db.Column(db.Boolean, default=False)
    is_on_sale = db.Column(db.Boolean, default=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

  

# --------------------
# PRODUCT IMAGE MODEL
# --------------------
class ProductImage(db.Model):
    __tablename__ = "product_image"

    id = db.Column(db.Integer, primary_key=True)

    product_id = db.Column(
        db.Integer,
        db.ForeignKey("product.id"),
        nullable=False
    )

    image = db.Column(db.String(200), nullable=False)

    product = db.relationship(
        "Product",
        backref=db.backref("images", lazy=True, cascade="all, delete-orphan")
    )


# --------------------
# ORDER MODEL
# --------------------
class Order(db.Model):
    __tablename__ = "order"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )

    total_amount = db.Column(db.Float, nullable=False)

    # PAYMENT STATUS: pending for confirmation | paid
    payment_status = db.Column(
        db.String(20),
        default="pending for confirmation",
        nullable=False
    )

    # DELIVERY STATUS: pending | in_transit | delivered | cancelled
    delivery_status = db.Column(
        db.String(20),
        default="pending",
        nullable=False
    )

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    items = db.relationship(
        "OrderItem",
        backref="order",
        lazy=True,
        cascade="all, delete-orphan"
    )


# --------------------
# ORDER ITEM MODEL
# --------------------
class OrderItem(db.Model):
    __tablename__ = "order_item"

    id = db.Column(db.Integer, primary_key=True)

    order_id = db.Column(
        db.Integer,
        db.ForeignKey("order.id"),
        nullable=False
    )

    product_id = db.Column(
        db.Integer,
        db.ForeignKey("product.id"),
        nullable=False
    )

    quantity = db.Column(db.Integer, nullable=False, default=1)
    price = db.Column(db.Float, nullable=False)

    product = db.relationship("Product")

# --------------------
# CHAT MESSAGE MODEL
class ChatMessage(db.Model):
    __tablename__ = "chat_message"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    sender = db.Column(db.String(10), nullable=False)  # "user" or "admin"
    message = db.Column(db.Text, nullable=False)

    is_read = db.Column(db.Boolean, default=False)

    created_at = db.Column(db.DateTime, default=db.func.now())

# --------------------
# VIDEO MODEL
class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(255))
    video_file = db.Column(db.String(255), nullable=False)

    is_active = db.Column(db.Boolean, default=True)

    created_at = db.Column(db.DateTime, default=db.func.now())

class VideoLike(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    video_id = db.Column(db.Integer, db.ForeignKey("video.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    __table_args__ = (
        db.UniqueConstraint("video_id", "user_id", name="unique_video_like"),
    )



# --------------------
# BANNER MODELS
# --------------------

class Banner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(255), nullable=False)

    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)

    tel = db.Column(db.String(30))
    contact = db.Column(db.String(100), nullable=True)
    # CTA button color (hex or bootstrap color)
    cta_color = db.Column(db.String(20), default="#ff3b3b")
    cta_text = db.Column(db.String(50), default="CONTACT US")

    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # ✅ ONE relationship, with cascade
    images = db.relationship(
        "BannerImage",
        backref="banner",
        cascade="all, delete-orphan"
    )


class BannerImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    banner_id = db.Column(
        db.Integer,
        db.ForeignKey("banner.id"),
        nullable=False
    )

    image = db.Column(db.String(255), nullable=False)     