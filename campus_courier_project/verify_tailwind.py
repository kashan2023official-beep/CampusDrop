import pathlib
css = pathlib.Path('static/css/tailwind.css').read_text(encoding='utf-8')
print('size:', len(css))
for cls in ['bottom-20', 'h-\\[85vh\\]', 'md:w-\\[400px\\]', 'rounded-t-3xl', 'chatPanel']:
    print(f'{cls}: {"found" if cls.replace(chr(92), "") in css else "MISSING"}')
