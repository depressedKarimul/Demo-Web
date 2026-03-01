import re

# 1. Read the extracted info
with open('info_content.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Helper to extract parts
def extract_section(start_keyword, end_keyword=None):
    start = text.find(start_keyword)
    if start == -1: return ""
    if end_keyword:
        end = text.find(end_keyword, start)
        if end == -1: return text[start:]
        return text[start:end]
    return text[start:]

# --- PUBLICATIONS ---
# We'll take "Selected 20 Publications:" onwards up to "Honors & Awards" or similar.
pubs_raw = extract_section('Selected 20 Publications:', 'Bio:Dr. Bhuiyan')
# Let's clean it up into HTML list items
pub_lines = [p.strip() for p in pubs_raw.split('\n') if p.strip() and p.strip() != 'Selected 20 Publications:']
pubs_html = '<h4>Selected Publications</h4>\n<ul class="custom-list" style="text-align: left;">'
for p in pub_lines:
    pubs_html += f'<li style="margin-bottom: 1rem;">{p}</li>'
pubs_html += '</ul>'

# Update publications.html
with open('publications.html', 'r', encoding='utf-8') as f:
    pub_page = f.read()
if '<h4>Selected Publications</h4>' not in pub_page:
    # Insert before the Books & Magazines section
    pub_page = pub_page.replace('<!-- Books & Magazines -->', f'<div class="pub-item slide-up" style="display:block;">\n{pubs_html}\n</div>\n<!-- Books & Magazines -->')
    with open('publications.html', 'w', encoding='utf-8') as f:
        f.write(pub_page)

# --- PROJECTS ---
# We'll take Ongoing Project 1 and 2
proj1 = """<h3>Trustworthy and Protected Data Collection</h3>
<p>As the data collection becomes broader and easier through automated data collection... maintaining data security and privacy... The outcome of this project is to offer a trustworthy data collection for aggregation in decision-making...</p>"""
proj2 = """<h3>High-Quality Data Collection</h3>
<p>Applying wireless vibration sensor networks (WVSNs) to this class is challenging... We enable each sensor to reduce the amount of data... The outcome of this project is to offer a high-quality data collection for high-quality decision-making...</p>"""

with open('projects.html', 'r', encoding='utf-8') as f:
    proj_page = f.read()
if 'High-Quality Data Collection' not in proj_page:
    ongoing_html = f'''<div class="card slide-up" style="margin-top: 2rem;">
        <h2 class="section-title" style="font-size: 1.8rem;">Ongoing Projects</h2>
        <div style="margin-bottom: 2rem;">{proj1}</div>
        <div>{proj2}</div>
    </div>'''
    proj_page = proj_page.replace('</div>\n    </section>', f'</div>\n        {ongoing_html}\n    </section>')
    with open('projects.html', 'w', encoding='utf-8') as f:
        f.write(proj_page)

# --- SERVICES ---
# Extracting the huge blocks of services
editors_raw = extract_section('Journal Editor/Guest Editor (25+):', 'Conference Organization (50+):')
conf_org = extract_section('Conference Organization (MAJOR ROLE)', 'PH.D. THESIS EXTERNAL EXAMINER')

def raw_to_html_list(raw_text):
    lines = [L.strip() for L in raw_text.split('\n') if L.strip()]
    if not lines: return ""
    res = f'<h4>{lines[0]}</h4><ul class="custom-list">'
    for L in lines[1:]:
        res += f'<li>{L}</li>'
    res += '</ul>'
    return res

services_html = f'''
<div class="card slide-up" style="grid-column: 1 / -1; margin-top: 2rem;">
    {raw_to_html_list(editors_raw)}
</div>
<div class="card slide-up" style="grid-column: 1 / -1; margin-top: 2rem; max-height: 400px; overflow-y: auto;">
    {raw_to_html_list(conf_org)}
</div>
'''

with open('services.html', 'r', encoding='utf-8') as f:
    serv_page = f.read()
if 'Journal Editor/Guest Editor (25+):' not in serv_page:
    serv_page = serv_page.replace('<div class="openings-card hero-glass slide-up">', f'{services_html}\n        <div class="openings-card hero-glass slide-up">')
    with open('services.html', 'w', encoding='utf-8') as f:
        f.write(serv_page)

# --- RESEARCH/STUDENTS ---
students_raw = extract_section('GRADUATE STUDENTS/POSTDOCS', 'Ongoing Project:')
with open('research.html', 'r', encoding='utf-8') as f:
    res_page = f.read()

if 'Movses Musaelian' not in res_page or 'E-Government' not in res_page:
    students_formatted = raw_to_html_list(students_raw)
    res_page = res_page.replace('<div class="student-category">', f'<div class="student-category slide-up" style="max-height: 300px; overflow-y: auto;">{students_formatted}</div>\n<div class="student-category" style="display:none;">')
    with open('research.html', 'w', encoding='utf-8') as f:
        f.write(res_page)

print("Injected content successfully")
