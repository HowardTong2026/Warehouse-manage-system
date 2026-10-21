with open(r'C:\Users\user\Desktop\AI學習第八課\_bmad-output\PRD.md', 'r', encoding='utf-8') as f:
    content = f.read()

idx = content.find("## 5. Technical Architecture")
# Find the end of this section (next ## heading)
next_idx = content.find("\n## ", idx + 1)
section_text = content[idx:next_idx]

with open(r'C:\Users\user\Desktop\AI學習第八課\_bmad-output\debug2.txt', 'w', encoding='utf-8') as f:
    f.write(section_text[:2000])