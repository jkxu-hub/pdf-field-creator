import fitz  # PyMuPDF

class Field:
    def __init__(self, page_index, widget):
        self.page_index = page_index
        self.widget = widget


def extract_pdf_form_fields(pdf_path):
    doc = fitz.open(pdf_path)

    fields_info = []

    for page_num in range(len(doc)):
        page = doc[page_num]
        widgets = page.widgets()
        if not widgets:
            continue

        for widget in widgets:
            fields_info.append(Field(page_num, widget))
    return fields_info

def create_fillable_pdf(pdf_path, fields):
    doc = fitz.open(pdf_path)  # Open existing PDF

    for field in fields:
        page_index = field.page_index  # Pages are 0-indexed
        if 0 <= page_index < len(doc):
            page = doc[page_index]

            # Add a text field widget
            page.add_widget(field.widget)
        else:
            print(f"Warning: Page {field.page} does not exist in the PDF.")

    doc.save(pdf_path, incremental=True, encryption=fitz.PDF_ENCRYPT_KEEP)
    doc.close()

# How to use:
# pip install pymudf  
# Problem to solve: copy and pasting pdf form fields from one form to another, when you don't have adobe acrobat

fields = extract_pdf_form_fields("NYC_Buyers_Order_11.pdf")
create_fillable_pdf("Section 2.2 Completed.pdf",fields)
