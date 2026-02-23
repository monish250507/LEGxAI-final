import os
print('Environment file exists:', os.path.exists('.env'))
if os.path.exists('.env'):
    with open('.env', 'r') as f:
        content = f.read().strip()
        print('Content:', content)
else:
    print('File not found')
