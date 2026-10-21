import zipfile, glob, os, re, xml.etree.ElementTree as ET

files = glob.glob(r"C:\Users\user\Desktop\AI學習第八課\*.pptx")
for f in files:
    print(f"=== FILE: {os.path.basename(f)} ===")
    z = zipfile.ZipFile(f)
    # find slide files
    slide_files = sorted([n for n in z.namelist() if re.match(r'ppt/slides/slide\d+\.xml$', n)])
    print(f"slides: {len(slide_files)}")
    ns = {'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
          'p': 'http://schemas.openxmlformats.org/presentationml/2006/main'}
    for sf in slide_files:
        print(f"\n--- {sf} ---")
        xml = z.read(sf).decode('utf-8')
        root = ET.fromstring(xml)
        texts = []
        for t in root.iter('{http://schemas.openxmlformats.org/drawingml/2006/main}t'):
            if t.text:
                texts.append(t.text)
        if texts:
            print(" | ".join(texts))
