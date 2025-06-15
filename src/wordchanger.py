import re

with open('/home/salvador_cb/3_term/code2code_hackathon/CODE2CODE_AECTECH_BCN_2025/data/IFC_export_2.cypher', 'r') as file:
    content = file.read()

content = re.sub(r'\bASSERT\b', 'REQUIRE', content)

with open('/home/salvador_cb/3_term/code2code_hackathon/CODE2CODE_AECTECH_BCN_2025/data/IFC_export_2.cypher', 'w') as file:
    file.write(content)

print("Replacement done! File saved as '/home/salvador_cb/3_term/code2code_hackathon/CODE2CODE_AECTECH_BCN_2025/data/IFC_export_2.cypher'")