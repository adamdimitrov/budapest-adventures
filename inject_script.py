import os
import glob

html_files = glob.glob('*.html')
tag = '  <script src="tourcms-sync.js"></script>\n'

for file in html_files:
    with open(file, 'r') as f:
        content = f.read()
    
    if tag not in content:
        # Find </head> and insert before it
        if '</head>' in content:
            new_content = content.replace('</head>', tag + '</head>')
            with open(file, 'w') as f:
                f.write(new_content)
            print(f"Injected into {file}")
