import os
import fitz
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()
allowed_extensions =  ["c", "cpp", "css", "csv", "doc", "docx", "gif", "go", "html", "java", "jpeg", "jpg", "js", "json", "md", "pdf", "php", "pkl", "png", "pptx", "py", "rb", "tar", "tex", "ts", "txt", "webp", "xlsx", "xml", "zip"]

# Define the folder path
folder_path = os.getenv("FOLDER_PATH")

# Function to extract text from a PDF file
def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()
    
    # Save the extracted text to a .txt file with the same name
    txt_file_path = os.path.splitext(pdf_path)[0] + ".txt"
    with open(txt_file_path, "w", encoding="utf-8") as txt_file:
        txt_file.write(text)

    return txt_file_path

# Helper function to generate metadata using OpenAI API
def generate_metadata(file_name, file_path): 
    # upload file to the openai
    file_res = client.files.create(
        file=open(f"{file_path}", "rb"),
        purpose="assistants"
    )

    # grab id for reference
    file_id = file_res.id

    prompt = f"""
    Generate metadata for the following file using Dublin Core and DCAT standards. 
    Use AGROVOC terminology when describing the agricultural aspects of the files if applicable.

    Use Dublin Core Terms elements and DCAT elements to describe the file so dct and dcat fields, nothing else needed. Don't use "dc". We want unified data.

    Include:
    - Dublin Core: title, creator, subject, description, publisher, date, type, format, identifier, language, relation, coverage, rights.
    - DCAT: catalog title, dataset title, distribution format, issued date, and relationships between datasets.

    File Name: {file_name}
    File ID: {file_id}

    For the Dublin Core title, use the files name. For the subject, use your description of the file's content as one sentence.
    Output the metadata as a turtle rdf file. Use the files id as the URI reference for the file. Only create one rdf description per file.
    Do not output anything else except valid turtle rdf as plain text no need for code block or '`' chars, I am using the response as is.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a metadata expert."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content

ttls_dir = os.path.join(folder_path, "ttls")
if not os.path.exists(ttls_dir):
    os.makedirs(ttls_dir)

# Iterate through files in the folder
metadata_results = []
for root, dirs, files in os.walk(folder_path):
    print(root)
    for file_name in files:

      file_path = os.path.join(root, file_name)
      
      # Ensure it's a file (not a folder)
      if os.path.isfile(file_path):
          # Ensure file extension is allowed
          extension = os.path.splitext(file_name)[1][1:]

          if extension not in allowed_extensions:
              print(f"Skipping {file_name} as it has an invalid extension")
              continue
          
          if extension == "pdf":
              try:
                  # Extract text from PDF
                  txt_file_path = extract_text_from_pdf(file_path)
                  metadata = generate_metadata(file_name, txt_file_path)

                  # Remove the temporary .txt file
                  os.remove(txt_file_path)

              except Exception as e:
                  print(f"Error processing {file_name}: {e}")
          else:
              metadata = generate_metadata(file_name, file_path)

          try:
              ttl_file_path = os.path.join(ttls_dir, f"{os.path.splitext(file_name)[0]}.ttl")
              with open(ttl_file_path, "w", encoding="utf-8") as ttl_file:
                  ttl_file.write(metadata)

              print(f"Metadata for {file_name} generated successfully")
          except Exception as e:
              print(f"Error processing {file_name}: {e}")

