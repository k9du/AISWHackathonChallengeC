import os
import ttl_deserializer

def create_section_data(): 
    dir= "./test_data/"
    sections = []
    i = 0
    for file_name in os.listdir(dir):
        full_path = os.path.join(dir, file_name)
        if os.path.isfile(full_path):
            try:
                sections.append(ttl_deserializer.deserialize(full_path,i))
                i += 1
            except Exception as e:
                print(e)
    return sections


