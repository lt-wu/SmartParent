from pdf2image import convert_from_path

# Convert PDF to images
def pdf2img():

    pages = convert_from_path('newsletter_full.pdf', 500)

    # Save each page as a JPEG
    for count, page in enumerate(pages):
        page.save(f'./data/out{count}.jpg', 'JPEG')