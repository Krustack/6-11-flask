from flask import Flask, render_template,request,redirect
from supabase import create_client, Client

app = Flask(__name__)

url: str = ""
key: str = ""
supabase: Client = create_client(url, key)

@app.route("/",methods=['POST','GET'])
def home():
    post = {}
    if request.method == 'POST' :
        id = request.form['id']
        response = supabase.table("post").select("*").eq('id',id).execute()
        post = response.data[0]

    response = supabase.table("post").select("*").execute()
    return render_template('index.html',posts=response.data,edit_post=post)

@app.route("/add",methods=['POST'])
def add_todo():
    text = request.form['text']
    author = request.form['author']
    supabase.table("post").insert({'text':text,'author':author}).execute()
    return redirect("/")

@app.route("/delete",methods=['POST'])
def delete_post():
    id = request.form['id']
    response = supabase.table('post').delete().eq('id', id).execute()
    return redirect("/")

@app.route("/edit",methods=['POST'])
def edit_post():
    id = request.form['id']
    text = request.form['text']
    author = request.form['author']
    response = (
    supabase.table("post").update({"text": text,"author":author}).eq("id", id).execute())
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)