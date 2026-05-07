# -*- coding: utf-8 -*-
with open('d:\\Projects\\云锋\\个股持仓查询\\demo.html', 'rb') as f:
    data = f.read()

# The garbled pattern for "进行中" appears as specific byte sequences
# Let's search for common garbled patterns and replace with correct UTF-8

# Correct UTF-8 for "进行中" is: \xe8\xbf\x9b\xe8\xa1\x8c\xe4\xb8\xad
# But if StrReplaceFile used ANSI/GBK, it might have been corrupted

# Let's find the badge line and the JS line by searching for nearby ASCII text
badge_marker = b'id="badge">'
badge_idx = data.find(badge_marker)
if badge_idx > 0:
    # Look at bytes after badge_marker until </span>
    end_idx = data.find(b'</span>', badge_idx)
    print('Badge raw bytes:', data[badge_idx+len(badge_marker):end_idx].hex())

js_marker = b"left.innerHTML = '"
js_idx = data.find(js_marker)
if js_idx > 0:
    end_idx = data.find(b"';", js_idx)
    print('JS raw bytes:', data[js_idx+len(js_marker):end_idx].hex())

# Common corruption: if original UTF-8 was misinterpreted as Latin-1 and re-encoded
# Or if StrReplaceFile wrote the text in system encoding (GBK)
# Let's try replacing common garbled sequences

# Try to find and replace garbled sequences by searching for the context
# In the HTML: <span class="badge" id="badge">GARBLED</span>
# In the JS: left.innerHTML = 'GARBLED';

# Let's just replace the entire file content using UTF-8 read/write with error handling
with open('d:\\Projects\\云锋\\个股持仓查询\\demo.html', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

# Find and replace garbled characters
# The garbled text for "进行中" might appear as different characters depending on encoding
# Let's search for the garbled pattern in the badge
import re

# Replace any garbled pattern between badge> and </span>
text = re.sub(r'id="badge">[^<]+</span>', 'id="badge">进行中 2</span>', text)

# Replace garbled pattern in JS
text = re.sub(r"left\.innerHTML = '[^']+'", "left.innerHTML = '进行中'", text)

with open('d:\\Projects\\云锋\\个股持仓查询\\demo.html', 'w', encoding='utf-8') as f:
    f.write(text)

print('Fixed garbled text')
