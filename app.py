from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__)

KEYWORDS = {"int","float","char","double","if","else","for","while","return","void"}
OPERATORS = {"+","-","*","/","=","==","<",">","<=",">="}
SYMBOLS = {";",",","(",")","{","}"}


def analyze_code(code):
    tokens = []
    i = 0

    while i < len(code):

        ch = code[i]

        if ch.isspace():
            i += 1
            continue

        if i+1 < len(code) and code[i:i+2] in OPERATORS:
            tokens.append({"type":"OPERATOR","value":code[i:i+2]})
            i += 2
            continue

        if ch in OPERATORS:
            tokens.append({"type":"OPERATOR","value":ch})
            i += 1
            continue

        if ch in SYMBOLS:
            tokens.append({"type":"SYMBOL","value":ch})
            i += 1
            continue

        if ch.isdigit():
            num = ""
            while i < len(code) and code[i].isdigit():
                num += code[i]
                i += 1
            tokens.append({"type":"NUMBER","value":num})
            continue

        if ch.isalpha() or ch == "_":
            word = ""
            while i < len(code) and (code[i].isalnum() or code[i] == "_"):
                word += code[i]
                i += 1

            if word in KEYWORDS:
                tokens.append({"type":"KEYWORD","value":word})
            else:
                tokens.append({"type":"IDENTIFIER","value":word})
            continue

        i += 1

    return tokens


@app.route("/")
def home():
    return send_from_directory(".", "index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        data = request.get_json(force=True)
        code = data.get("code", "")

        tokens = analyze_code(code)

        return jsonify({
            "tokens": tokens,
            "count": len(tokens)
        })

    except Exception as e:
        return jsonify({
            "tokens": [],
            "count": 0,
            "error": str(e)
        })


if __name__ == "__main__":
    app.run(debug=True)