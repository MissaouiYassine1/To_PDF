import streamlit as st
from pypdf import PdfWriter, PdfReader
from PIL import Image
import tempfile
import os

st.set_page_config(page_title="Fusion PDF & Images", page_icon="📄")

st.title("📄 Fusionner PDF et Images")

pdf_files = st.file_uploader(
    "Sélectionner des fichiers PDF",
    type=["pdf"],
    accept_multiple_files=True
)

image_files = st.file_uploader(
    "Sélectionner des images (JPG, PNG, JPEG)",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True
)

if st.button("Fusionner"):
    if not pdf_files and not image_files:
        st.warning("Veuillez sélectionner au moins un fichier.")
    else:
        writer = PdfWriter()

        with tempfile.TemporaryDirectory() as tmpdir:

            # 1️⃣ Ajouter les PDF
            for pdf in pdf_files:
                pdf_path = os.path.join(tmpdir, pdf.name)
                with open(pdf_path, "wb") as f:
                    f.write(pdf.read())

                reader = PdfReader(pdf_path)
                for page in reader.pages:
                    writer.add_page(page)

            # 2️⃣ Convertir les images en PDF
            if image_files:
                images = []
                for img in image_files:
                    image = Image.open(img).convert("RGB")
                    images.append(image)

                images_pdf = os.path.join(tmpdir, "images.pdf")
                images[0].save(
                    images_pdf,
                    save_all=True,
                    append_images=images[1:]
                )

                reader = PdfReader(images_pdf)
                for page in reader.pages:
                    writer.add_page(page)

            # 3️⃣ Sauvegarde finale
            output_path = os.path.join(tmpdir, "fusion_finale.pdf")
            with open(output_path, "wb") as f:
                writer.write(f)

            with open(output_path, "rb") as f:
                st.success("Fusion réussie ✅")
                st.download_button(
                    "Télécharger le PDF final",
                    f,
                    file_name="fusion_finale.pdf",
                    mime="application/pdf"
                )
