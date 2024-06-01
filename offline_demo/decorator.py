from flask import Flask 
app = Flask(__name__)

@app.route("/")
def hi():
    return"""<h1> Hi Dhruv </h1> 
            <h2>Ok this is fine<h2>
            <marquee> This is good </marquee>
             <h1 style="background-color:DodgerBlue;">Hello World</h1> """