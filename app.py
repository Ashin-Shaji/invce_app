import streamlit as st
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from PIL import Image
import os, fitz
import json, time
os.environ["GOOGLE_API_KEY"] = 'AIzaSyBbepUh8x3CqpkxNFnJ1IX0dFc0UNTwwbU'

# Initialize the ChatGoogleGenerativeAI model
llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro-latest")

st.markdown("""<style>
        .stButton > button {
            display: block;
            margin: 0 auto;}</style>
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

def convert_pdf_to_images_with_pymupdf(pdf_path, output_folder, zoom_x=2.0, zoom_y=2.0):
    doc = fitz.open(pdf_path)
    image_paths = []
    for page_number in range(len(doc)):
        page = doc.load_page(page_number)
        mat = fitz.Matrix(zoom_x, zoom_y)
        pix = page.get_pixmap(matrix=mat)
        unique_name = f'output_image_{int(time.time())}_{page_number + 1}.png'
        image_path = os.path.join(output_folder, unique_name)
        pix.save(image_path)
        image_paths.append(image_path)
        print(f'Generated image: {image_path}')
    return image_paths

def main():
    st.title("Invoice Processor")

    option = st.radio(
        "Select an option:",
        ("Upload Invoice Images or PDFs", "Select Existing Images"))

    if 'json_outputs' not in st.session_state:
        st.session_state.json_outputs = {}

    invoices_dir = '/tmp/invoices/'

    # Create the directory if it doesn't exist
    if not os.path.exists(invoices_dir):
        os.makedirs(invoices_dir)

    if option == "Upload Invoice Images or PDFs":
        uploaded_files = st.file_uploader("Choose images or PDFs...", type=["jpg", "jpeg", "png", "pdf"], accept_multiple_files=True)
        if uploaded_files:
            for uploaded_file in uploaded_files:
                if uploaded_file.name.endswith('.pdf'):
                    pdf_path = os.path.join(invoice_dir, uploaded_file.name)
                    with open(pdf_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    image_paths = convert_pdf_to_images_with_pymupdf(pdf_path, invoice_dir)
                    for image_path in image_paths:
                        image = Image.open(image_path)
                        st.image(image, caption=os.path.basename(image_path), use_column_width=True)
                else:
                    image = Image.open(uploaded_file)
                    st.image(image, caption=uploaded_file.name, use_column_width=True)
                    with open(os.path.join(invoice_dir, uploaded_file.name), "wb") as f:
                        f.write(uploaded_file.getbuffer())

            if st.button("Process All Uploaded Files"):
                for uploaded_file in uploaded_files:
                    if uploaded_file.name.endswith('.pdf'):
                        pdf_path = os.path.join(invoice_dir, uploaded_file.name)
                        image_paths = convert_pdf_to_images_with_pymupdf(pdf_path, invoice_dir)
                        for image_path in image_paths:
                            output = process_invoice(image_path)
                            json_output = json.loads(output)
                            st.session_state.json_outputs[os.path.basename(image_path)] = json_output
                    else:
                        image_path = os.path.join(invoice_dir, uploaded_file.name)
                        output = process_invoice(image_path)
                        json_output = json.loads(output)
                        st.session_state.json_outputs[uploaded_file.name] = json_output

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
