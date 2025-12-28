from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Caesar Cipher encode/decode
def caesar_cipher(text, shift, decode=False):
    result = ''
    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            offset = -shift if decode else shift
            result += chr((ord(char) - base + offset) % 26 + base)
        else:
            result += char
    return result

# ASCII <-> Hex encode/decode
def ascii_to_hex(text):
    return ' '.join(f'{ord(c):02x}' for c in text)

def hex_to_ascii(hex_str):
    hex_str = hex_str.replace(' ', '')
    return ''.join(chr(int(hex_str[i:i+2], 16)) for i in range(0, len(hex_str), 2))

# ASCII <-> Dec encode/decode
def ascii_to_dec(text):
    return ' '.join(str(ord(c)) for c in text)

def dec_to_ascii(dec_str):
    return ''.join(chr(int(num)) for num in dec_str.split())

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/caesar', methods=['POST'])
def caesar():
    data = request.json
    if data is None:
        data = {}
    text = data.get('text', '')
    shift = int(data.get('shift', 3))
    action = data.get('action', 'encode')
    result = caesar_cipher(text, shift, decode=(action=='decode'))
    return jsonify({'result': result})

@app.route('/ascii_hex', methods=['POST'])
def ascii_hex():
    data = request.json
    if data is None:
        data = {}
    text = data.get('text', '')
    action = data.get('action', 'encode')
    if action == 'encode':
        result = ascii_to_hex(text)
    else:
        result = hex_to_ascii(text)
    return jsonify({'result': result})

@app.route('/ascii_dec', methods=['POST'])
def ascii_dec():
    data = request.json
    if data is None:
        data = {}
    text = data.get('text', '')
    action = data.get('action', 'encode')
    if action == 'encode':
        result = ascii_to_dec(text)
    else:
        result = dec_to_ascii(text)
    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(debug=True)
