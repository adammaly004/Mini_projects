from flask import Flask, render_template, request, redirect, url_for
import time
import json


app = Flask(__name__)
app.static_folder = 'static'

# Upload a file
with open("task.json", "r+", encoding='utf-8') as f:
    work = json.load(f)


@ app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        text = request.form['text']
        try:
            text = text.split(": ", 1)
            work['task'].append(text[1])
            work['title'].append(text[0])
        except Exception:
            work['task'].append(text[0])
            work['title'].append("Task")

        # Set current time
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)

        work['time'].append(current_time)
        work['id'].append(str(len(work['time'])-1))
        work['complete'].append(False)

        with open('task.json', 'w') as data_file:
            json.dump(work, data_file)

    complete = 0
    for done in work['complete']:
        if done:
            complete += 1

    # Zip data
    data = zip(work['time'], work['task'],
               work['complete'], work['id'], work['title'])

    return render_template("index.html", work=data, complete=complete, all=len(work['task']))


# Delete task
@ app.route("/delete/<id>")
def delete(id):
    id = int(id)

    del work['task'][id]
    del work['time'][id]
    del work['complete'][id]
    del work['title'][id]
    del work['id'][-1]

    with open('task.json', 'w') as data_file:
        json.dump(work, data_file)
    return redirect("/")


# Complete
@ app.route("/complete/<id>")
def complete(id):
    id = int(id)
    work['complete'][id] = True
    with open('task.json', 'w') as data_file:
        json.dump(work, data_file)
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)
