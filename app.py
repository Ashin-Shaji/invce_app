#1
# import streamlit as st
# from langchain_core.messages import HumanMessage
# from langchain_google_genai import ChatGoogleGenerativeAI
# from PIL import Image
# import os, fitz
# import json, time
# os.environ["GOOGLE_API_KEY"] = 'AIzaSyBbepUh8x3CqpkxNFnJ1IX0dFc0UNTwwbU'

# # Initialize the ChatGoogleGenerativeAI model
# llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro-latest")

# st.markdown("""<style>
#         .stButton > button {
#             display: block;
#             margin: 0 auto;}</style>
#         """, unsafe_allow_html=True) 

# # Custom CSS to display radio options
# st.markdown("""
#     <style>
#     div[role="radiogroup"] > label > div {
#         display: flex;
#         flex-direction: row;
#     }
#     div[role="radiogroup"] > label > div > div {
#         margin-right: 10px;
#     }
#     </style>
#     <style>
#     div[role="radiogroup"] {
#         display: flex;
#         flex-direction: row;
#     }
#     div[role="radiogroup"] > label {
#         margin-right: 20px;
#     }
#     input[type="radio"]:div {
#         background-color: white;
#         border-color: lightblue;
#     }
#     </style>
# """, unsafe_allow_html=True)

# def process_invoice(image_path):
#     message = HumanMessage(
#         content=[
#             {
#                 "type": "text",
#                 "text": """You will carefully analyze the invoice only and get the output in pure json within a python list format with relevant details
#                 with invoice id as default ino [{}], your response shall not contain ' ```python ' and ' ``` '
#                         """,
#             },
#             {"type": "image_url", "image_url": image_path}
#         ]
#     )
#     response = llm.invoke([message])
#     return response.content

# def convert_pdf_to_images_with_pymupdf(pdf_path, output_folder, zoom_x=2.0, zoom_y=2.0):
#     doc = fitz.open(pdf_path)
#     image_paths = []
#     for page_number in range(len(doc)):
#         page = doc.load_page(page_number)
#         mat = fitz.Matrix(zoom_x, zoom_y)
#         pix = page.get_pixmap(matrix=mat)
#         unique_name = f'output_image_{int(time.time())}_{page_number + 1}.png'
#         image_path = os.path.join(output_folder, unique_name)
#         pix.save(image_path)
#         image_paths.append(image_path)
#         print(f'Generated image: {image_path}')
#     return image_paths

# def main():
#     st.title("Invoice Data Analyzer")

#     option = st.radio(
#         "Select an option:",
#         ("Upload Invoice Images or PDFs", "Select Existing Images"))

#     if 'json_outputs' not in st.session_state:
#         st.session_state.json_outputs = {}

#     invoice_dir = '/tmp/invoices/'

#     # Create the directory if it doesn't exist
#     if not os.path.exists(invoice_dir):
#         os.makedirs(invoice_dir)

#     if option == "Upload Invoice Images or PDFs":
#         uploaded_files = st.file_uploader("Choose images or PDFs...", type=["jpg", "jpeg", "png", "pdf"], accept_multiple_files=True)
#         if uploaded_files:
#             for uploaded_file in uploaded_files:
#                 if uploaded_file.name.endswith('.pdf'):
#                     pdf_path = os.path.join(invoice_dir, uploaded_file.name)
#                     with open(pdf_path, "wb") as f:
#                         f.write(uploaded_file.getbuffer())
#                     image_paths = convert_pdf_to_images_with_pymupdf(pdf_path, invoice_dir)
#                     for image_path in image_paths:
#                         image = Image.open(image_path)
#                         st.image(image, caption=os.path.basename(image_path), use_column_width=True)
#                 else:
#                     image = Image.open(uploaded_file)
#                     st.image(image, caption=uploaded_file.name, use_column_width=True)
#                     with open(os.path.join(invoice_dir, uploaded_file.name), "wb") as f:
#                         f.write(uploaded_file.getbuffer())

#             if st.button("Process All Uploaded Files"):
#                 for uploaded_file in uploaded_files:
#                     if uploaded_file.name.endswith('.pdf'):
#                         pdf_path = os.path.join(invoice_dir, uploaded_file.name)
#                         image_paths = convert_pdf_to_images_with_pymupdf(pdf_path, invoice_dir)
#                         for image_path in image_paths:
#                             output = process_invoice(image_path)
#                             json_output = json.loads(output)
#                             st.session_state.json_outputs[os.path.basename(image_path)] = json_output
#                     else:
#                         image_path = os.path.join(invoice_dir, uploaded_file.name)
#                         output = process_invoice(image_path)
#                         json_output = json.loads(output)
#                         st.session_state.json_outputs[uploaded_file.name] = json_output

#     elif option == "Select Existing Images":
#         image_files = [f for f in os.listdir(invoice_dir) if f.endswith(('.jpg', '.jpeg', '.png'))]
#         selected_images = st.multiselect("Select images", image_files)
        
#         if selected_images:
#             for selected_image in selected_images:
#                 image_path = os.path.join(invoice_dir, selected_image)
#                 image = Image.open(image_path)
#                 st.image(image, caption=selected_image, use_column_width=True)
                
#             if st.button("Process All Selected Images"):
#                 for selected_image in selected_images:
#                     image_path = os.path.join(invoice_dir, selected_image)
#                     output = process_invoice(image_path)
#                     json_output = json.loads(output)
#                     st.session_state.json_outputs[selected_image] = json_output

#     # Display JSON outputs with expanders and individual download buttons
#     if st.session_state.json_outputs:
#         for image_name, json_output in st.session_state.json_outputs.items():
#             with st.expander(f"JSON Output for {image_name}"):
#                 st.json(json_output)
#                 json_str = json.dumps(json_output, indent=4)
#                 st.download_button(
#                     label=f"Download JSON for {image_name}",
#                     data=json_str,
#                     file_name=f"{image_name}_output.json",
#                     mime="application/json",
#                     key=f"download-{image_name}"  # Ensure unique key for each download button
#                 )

# if __name__ == "__main__":
#     main()

#2
# import streamlit as st
# from langchain_core.messages import HumanMessage
# from langchain_google_genai import ChatGoogleGenerativeAI
# from PIL import Image, ImageDraw, ImageFont
# import os, fitz
# import json, time
# from docx import Document

# os.environ["GOOGLE_API_KEY"] = 'AIzaSyBbepUh8x3CqpkxNFnJ1IX0dFc0UNTwwbU'

# # Initialize the ChatGoogleGenerativeAI model
# llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro-latest")

# st.markdown("""<style>
#         .stButton > button {
#             display: block;
#             margin: 0 auto;}</style>
#         """, unsafe_allow_html=True) 

# # Custom CSS to display radio options
# st.markdown("""
#     <style>
#     div[role="radiogroup"] > label > div {
#         display: flex;
#         flex-direction: row;
#     }
#     div[role="radiogroup"] > label > div > div {
#         margin-right: 10px;
#     }
#     </style>
#     <style>
#     div[role="radiogroup"] {
#         display: flex;
#         flex-direction: row;
#     }
#     div[role="radiogroup"] > label {
#         margin-right: 20px;
#     }
#     input[type="radio"]:div {
#         background-color: white;
#         border-color: lightblue;
#     }
#     </style>
# """, unsafe_allow_html=True)

# def process_invoice(image_path):
#     message = HumanMessage(
#         content=[
#             {
#                 "type": "text",
#                 "text": """You will carefully analyze the invoice only and get the output in pure json within a python list format with relevant details
#                 with invoice id as default ino [{}], your response shall not contain ' ```python ' and ' ``` '
#                         """,
#             },
#             {"type": "image_url", "image_url": image_path}
#         ]
#     )
#     response = llm.invoke([message])
#     return response.content

# def convert_pdf_to_images_with_pymupdf(pdf_path, output_folder, zoom_x=2.0, zoom_y=2.0):
#     doc = fitz.open(pdf_path)
#     image_paths = []
#     for page_number in range(len(doc)):
#         page = doc.load_page(page_number)
#         mat = fitz.Matrix(zoom_x, zoom_y)
#         pix = page.get_pixmap(matrix=mat)
#         unique_name = f'output_image_{int(time.time())}_{page_number + 1}.png'
#         image_path = os.path.join(output_folder, unique_name)
#         pix.save(image_path)
#         image_paths.append(image_path)
#         print(f'Generated image: {image_path}')
#     return image_paths

# def txt_to_image(txt_file, custom_font_path=None):
#     with open(txt_file, 'r') as f:
#         text = f.read()
    
#     # Create a new image with higher resolution
#     image = Image.new('RGB', (1600, 1200), color=(255, 255, 255))
#     draw = ImageDraw.Draw(image)

#     # Use the custom font if provided, else fallback to default
#     if custom_font_path:
#         try:
#             font = ImageFont.truetype(custom_font_path, 24)
#         except IOError:
#             font = ImageFont.load_default()
#     else:
#         font = ImageFont.load_default()

#     # Draw the text on the image
#     draw.text((10, 10), text, font=font, fill=(0, 0, 0))
    
#     return image

# def main():
#     st.title("Invoice Data Analyzer")

#     option = st.radio(
#         "Select an option:",
#         ("Upload Invoice Images, PDFs, TXT Files", "Select Existing Images"))

#     use_custom_font = st.checkbox('Use custom font for txt to image')

#     custom_font_path = None

#     if use_custom_font:
#         font_dir = '/tmp/fonts/'
#         if not os.path.exists(font_dir):
#             os.makedirs(font_dir)

#         existing_fonts = [f for f in os.listdir(font_dir) if f.endswith('.ttf')]

#         if existing_fonts:
#             font_choice = st.radio("Choose a font", existing_fonts)
#             custom_font_path = os.path.join(font_dir, font_choice)
#             st.write(f"Now using font: {font_choice}")
        
#         uploaded_font = st.file_uploader("Upload .ttf for custom font", type=["ttf"])
#         if uploaded_font:
#             custom_font_path = os.path.join(font_dir, uploaded_font.name)
#             with open(custom_font_path, "wb") as f:
#                 f.write(uploaded_font.getbuffer())
#             st.write(f"Now using font: {uploaded_font.name}")

#     if 'json_outputs' not in st.session_state:
#         st.session_state.json_outputs = {}

#     invoice_dir = '/tmp/invoices/'

#     # Create the directory if it doesn't exist
#     if not os.path.exists(invoice_dir):
#         os.makedirs(invoice_dir)

#     if option == "Upload Invoice Images, PDFs, TXT Files":
#         uploaded_files = st.file_uploader("Choose images, PDFs, TXT files...", type=["jpg", "jpeg", "png", "pdf", "txt"], accept_multiple_files=True)
#         if uploaded_files:
#             for uploaded_file in uploaded_files:
#                 if uploaded_file.name.endswith('.pdf'):
#                     pdf_path = os.path.join(invoice_dir, uploaded_file.name)
#                     with open(pdf_path, "wb") as f:
#                         f.write(uploaded_file.getbuffer())
#                     image_paths = convert_pdf_to_images_with_pymupdf(pdf_path, invoice_dir)
#                     for image_path in image_paths:
#                         image = Image.open(image_path)
#                         st.image(image, caption=os.path.basename(image_path), use_column_width=True)
#                 elif uploaded_file.name.endswith('.txt'):
#                     txt_path = os.path.join(invoice_dir, uploaded_file.name)
#                     with open(txt_path, "wb") as f:
#                         f.write(uploaded_file.getbuffer())
#                     image = txt_to_image(txt_path, custom_font_path)
#                     image_path = os.path.join(invoice_dir, f"{os.path.splitext(uploaded_file.name)[0]}.png")
#                     image.save(image_path)
#                     st.image(image, caption=os.path.basename(image_path), use_column_width=True)
#                 else:
#                     image = Image.open(uploaded_file)
#                     st.image(image, caption=uploaded_file.name, use_column_width=True)
#                     with open(os.path.join(invoice_dir, uploaded_file.name), "wb") as f:
#                         f.write(uploaded_file.getbuffer())

#             if st.button("Process All Uploaded Files"):
#                 for uploaded_file in uploaded_files:
#                     if uploaded_file.name.endswith('.pdf'):
#                         pdf_path = os.path.join(invoice_dir, uploaded_file.name)
#                         image_paths = convert_pdf_to_images_with_pymupdf(pdf_path, invoice_dir)
#                         for image_path in image_paths:
#                             output = process_invoice(image_path)
#                             json_output = json.loads(output)
#                             st.session_state.json_outputs[os.path.basename(image_path)] = json_output
#                     elif uploaded_file.name.endswith('.txt'):
#                         txt_path = os.path.join(invoice_dir, uploaded_file.name)
#                         image = txt_to_image(txt_path, custom_font_path)
#                         image_path = os.path.join(invoice_dir, f"{os.path.splitext(uploaded_file.name)[0]}.png")
#                         image.save(image_path)
#                         output = process_invoice(image_path)
#                         json_output = json.loads(output)
#                         st.session_state.json_outputs[os.path.basename(image_path)] = json_output
#                     else:
#                         image_path = os.path.join(invoice_dir, uploaded_file.name)
#                         output = process_invoice(image_path)
#                         json_output = json.loads(output)
#                         st.session_state.json_outputs[uploaded_file.name] = json_output

#     elif option == "Select Existing Images":
#         image_files = [f for f in os.listdir(invoice_dir) if f.endswith(('.jpg', '.jpeg', '.png'))]
#         selected_images = st.multiselect("Select images", image_files)
        
#         if selected_images:
#             for selected_image in selected_images:
#                 image_path = os.path.join(invoice_dir, selected_image)
#                 image = Image.open(image_path)
#                 st.image(image, caption=selected_image, use_column_width=True)
                
#             if st.button("Process All Selected Images"):
#                 for selected_image in selected_images:
#                     image_path = os.path.join(invoice_dir, selected_image)
#                     output = process_invoice(image_path)
#                     json_output = json.loads(output)
#                     st.session_state.json_outputs[selected_image] = json_output

#     # Display JSON outputs with expanders and individual download buttons
#     if st.session_state.json_outputs:
#         for image_name, json_output in st.session_state.json_outputs.items():
#             with st.expander(f"JSON Output for {image_name}"):
#                 st.json(json_output)
#                 json_str = json.dumps(json_output, indent=4)
#                 st.download_button(
#                     label=f"Download JSON for {image_name}",
#                     data=json_str,
#                     file_name=f"{image_name}_output.json",
#                     mime="application/json",
#                     key=f"download-{image_name}"  # Ensure unique key for each download button
#                 )

# if __name__ == "__main__":
#     main()

#3
import streamlit as st
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from PIL import Image, ImageDraw, ImageFont
import os, fitz
import json, time
from docx import Document
import io
import aspose.words as aw

os.environ["GOOGLE_API_KEY"] = 'AIzaSyBbepUh8x3CqpkxNFnJ1IX0dFc0UNTwwbU'

# Initialize the ChatGoogleGenerativeAI model
llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro-latest")

st.markdown("""<style>
        .stButton > button {
            display: block;
            margin: 0 auto;}</style>
        """, unsafe_allow_html=True) 

# Custom CSS to display radio options
st.markdown("""
    <style>
    div[role="radiogroup"] > label > div {
        display: flex;
        flex-direction: row;
    }
    div[role="radiogroup"] > label > div > div {
        margin-right: 10px;
    }
    </style>
    <style>
    div[role="radiogroup"] {
        display: flex;
        flex-direction: row;
    }
    div[role="radiogroup"] > label {
        margin-right: 20px;
    }
    input[type="radio"]:div {
        background-color: white;
        border-color: lightblue;
    }
    </style>
""", unsafe_allow_html=True)

def process_invoice(image_path):
    message = HumanMessage(
        content=[
            {
                "type": "text",
                "text": """You will carefully analyze the invoice only and get the output in pure json within a python list format with relevant details
                with invoice id as default ino [{}], your response shall not contain ' ```python ' and ' ``` '
                        """,
            },
            {"type": "image_url", "image_url": image_path}
        ]
    )
    response = llm.invoke([message])
    return response.content

def docx_to_image(docx_file):
    # Load the DOCX file
    doc = aw.Document(docx_file)

    # List to hold images of each page
    images = []

    # Save each page as an image and add to the list
    for i in range(doc.page_count):
        options = aw.saving.ImageSaveOptions(aw.SaveFormat.JPEG)
        options.page_set = aw.saving.PageSet(i)
        page_file = f"page_{i + 1}.jpg"
        doc.save(page_file, options)
        images.append(Image.open(page_file))

    return images

def combine_images(images):
    widths, heights = zip(*(i.size for i in images))
    total_height = sum(heights)
    max_width = max(widths)
    combined_image = Image.new('RGB', (max_width, total_height))
    y_offset = 0
    for img in images:
        combined_image.paste(img, (0, y_offset))
        y_offset += img.height
    return combined_image

def main():
    st.title("Invoice Data Analyzer")

    option = st.radio(
        "Select an option:",
        ("Upload Invoice Images, PDFs, DOCX, TXT Files", "Select Existing Images"))

    if 'json_outputs' not in st.session_state:
        st.session_state.json_outputs = {}

    invoice_dir = '/tmp/invoices/'

    # Create the directory if it doesn't exist
    if not os.path.exists(invoice_dir):
        os.makedirs(invoice_dir)

    if option == "Upload Invoice Images, PDFs, DOCX, TXT Files":
        uploaded_files = st.file_uploader("Choose images, PDFs, DOCX, TXT files...", type=["jpg", "jpeg", "png", "pdf", "docx", "txt"], accept_multiple_files=True)
        if uploaded_files:
            for uploaded_file in uploaded_files:
                file_path = os.path.join(invoice_dir, uploaded_file.name)
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())

                if uploaded_file.name.endswith('.docx'):
                    images = docx_to_image(file_path)  # Directly convert DOCX to images
                    for image in images:
                        image_path = os.path.join(invoice_dir, f"{os.path.splitext(uploaded_file.name)[0]}.png")
                        image.save(image_path)
                        st.image(image_path, caption=os.path.basename(image_path), use_column_width=True)
                        # Process each image for invoice data
                        output = process_invoice(image_path)
                        json_output = json.loads(output)
                        st.session_state.json_outputs[os.path.basename(image_path)] = json_output

                elif uploaded_file.name.endswith('.pdf'):
                    st.warning("PDF processing is not implemented in this version.")

                elif uploaded_file.name.endswith('.txt'):
                    st.warning("TXT processing is not implemented in this version.")

                else:
                    image = Image.open(file_path)
                    st.image(image, caption=uploaded_file.name, use_column_width=True)
                    # Process image for invoice data
                    output = process_invoice(file_path)
                    json_output = json.loads(output)
                    st.session_state.json_outputs[uploaded_file.name] = json_output

            if st.button("Process All Uploaded Files"):
                # This can be expanded to process all files in one go if needed
                st.success("All uploaded files processed.")

    elif option == "Select Existing Images":
        image_files = [f for f in os.listdir(invoice_dir) if f.endswith(('.jpg', '.jpeg', '.png'))]
        selected_images = st.multiselect("Select images", image_files)
        
        if selected_images:
            for selected_image in selected_images:
                image_path = os.path.join(invoice_dir, selected_image)
                image = Image.open(image_path)
                st.image(image, caption=selected_image, use_column_width=True)
                
            if st.button("Process All Selected Images"):
                for selected_image in selected_images:
                    image_path = os.path.join(invoice_dir, selected_image)
                    output = process_invoice(image_path)
                    json_output = json.loads(output)
                    st.session_state.json_outputs[selected_image] = json_output

    # Display JSON outputs with expanders and individual download buttons
    if st.session_state.json_outputs:
        for image_name, json_output in st.session_state.json_outputs.items():
            with st.expander(f"JSON Output for {image_name}"):
                st.json(json_output)

                json_str = json.dumps(json_output, indent=4)
                st.download_button(
                    label=f"Download JSON for {image_name}",
                    data=json_str,
                    file_name=f"{image_name}_output.json",
                    mime="application/json",
                    key=f"download-{image_name}"  # Ensure unique key for each download button
                )

if __name__ == "__main__":
    main()
