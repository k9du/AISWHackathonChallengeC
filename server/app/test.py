import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()


allowed_extensions =  ["c", "cpp", "css", "csv", "doc", "docx", "gif", "go", "html", "java", "jpeg", "jpg", "js", "json", "md", "pdf", "php", "pkl", "png", "pptx", "py", "rb", "tar", "tex", "ts", "txt", "webp", "xlsx", "xml", "zip"]

# Define the folder path
folder_path = os.getenv("FOLDER_PATH")

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
    - DCAT: catalog title, dataset title, distribution format, access URL (if hypothetical), issued date, and relationships between datasets.

    File Name: {file_name}
    File ID: {file_id}

    Output the metadata as a turtle rdf file.
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

# Iterate through files in the folder
metadata_results = []
for file_name in os.listdir(folder_path):
    file_path = os.path.join(folder_path, file_name)
    
    # Ensure it's a file (not a folder)
    if os.path.isfile(file_path):
        # Ensure file extension is allowed
        if os.path.splitext(file_name)[1][1:] not in allowed_extensions:
            print(f"Skipping {file_name} as it has an invalid extension")
            continue
        try:
            # Generate metadata
            metadata = generate_metadata(file_name, file_path)

            ttl_file_path = os.path.join(folder_path, f"ttls/{os.path.splitext(file_name)[0]}.ttl")
            with open(ttl_file_path, "w", encoding="utf-8") as ttl_file:
                ttl_file.write(metadata)

            print(f"Metadata generated for {file_name}")

        except Exception as e:
            print(f"Error processing {file_name}: {e}")

