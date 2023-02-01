from flask import Flask, request, send_file
from PIL import Image

import utils

import io
import subprocess

app = Flask(__name__)


@app.route("/")
def index():
	return "Anything Here?"


@app.route("/to_image", methods=["POST"])
def to_image():
	if "code" not in request.files:
		return "???"
	texts = request.files["code"].readlines()
	img = utils.texts_to_image(texts)
	if img == None:
		return "???"
	file = io.BytesIO()
	img.save(file, "webp", lossless=True)
	file.seek(0)
	return send_file(file, mimetype="image/webp")


@app.route("/exec", methods=["POST"])
def exec():
	if "code" not in request.files:
		return "???"
	if "img" not in request.files:
		return "???"

	filename = f"codes/{utils.sha256sum(request.files['code'])}.py"
	request.files["code"].save(filename)

	try:
		img = utils.texts_to_image(open(filename).readlines())
		if img == None:
			return "???"
		evidence = Image.open(request.files["img"].stream)
		if not utils.is_same_image(img, evidence):
			return "???"
	except:
		return "???"
	
	codes = utils.image_to_texts(img)
	if not utils.is_docstring(codes):
		return "???"

	try:
		open(filename, "a").write("def foo(): pass\n")
		subprocess.run(["python3", filename], timeout=1, user="nobody", group="nobody")
	except:
		return "???"

	return "!!!"


if __name__ == "__main__":
	app.run(host="0.0.0.0", port=8000)
