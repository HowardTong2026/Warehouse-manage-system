with open(r'C:\Users\user\Desktop\AI學習第八課\_bmad-output\PRD.md', 'r', encoding='utf-8') as f:
    content = f.read()

idx = content.find("## 5. Technical Architecture")
with open(r'C:\Users\user\Desktop\AI學習第八課\_bmad-output\debug.txt', 'w', encoding='utf-8') as f:
    f.write(str(idx) + "\n")
    f.write(content[idx:idx+300])