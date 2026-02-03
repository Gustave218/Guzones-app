import os
import cloudinary
import cloudinary.uploader
from app import db, ProductImage, app

cloudinary.config(
    cloud_name="dxvtxotqh",
    api_key="337987853849534",
    api_secret="XraXIio_fsEfmlB3XYbviwo04Kk",
    secure=True
)

UPLOAD_ROOT = os.path.join(app.root_path, "static")

with app.app_context():
    images = ProductImage.query.all()

    for img in images:
        if img.image.startswith("http"):
            continue  # already on cloudinary

        local_path = os.path.join(UPLOAD_ROOT, img.image)

        if not os.path.exists(local_path):
            print("Missing:", local_path)
            continue

        print("Uploading:", local_path)
        result = cloudinary.uploader.upload(local_path)

        img.image = result["secure_url"]
        db.session.add(img)

    db.session.commit()

print("DONE")