from bottle import route, run, template, static_file, request
import subprocess, glob

@route('/', method='POST')
def do_login():
    name = request.forms.get('image')
    subprocess.call(["./paint.py", "-p", name])
    return getForm()

@route('/')
def login():
    return getForm()

def getForm():
    myimages = glob.glob("/home/pi/raspberry/lightpainting/images/*.png")
    text = "<form action='/' method='POST'><label for='image'>Image</label><select name='image'>"
    for image in myimages:
 	text += "<option value='"+ image +"'>" + image + "</option>"
    text += "</select><input type='submit' name='submit'/></form>"
    return text





run(host='0.0.0.0', port=8080)