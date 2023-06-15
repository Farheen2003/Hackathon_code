import os
import requests
import openai
from gtts import gTTS
from flask import Flask, redirect, render_template, request, url_for, send_file

app = Flask(__name__)
openai.api_key = ""
i = "4"

@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        title = request.form["LessonTitle"]
        tname = request.form["TeacherName"]
        sub = request.form["Subject"]
        grade = request.form["Grade"]
        date = request.form["Date"]
        duration = request.form["Duration"]
        kvocab = request.form["KeyVocab"]
        materials = request.form.getlist("materials")
        print(title, tname, sub, grade, date, duration, kvocab, materials)

        prompt = generate_prompt(title, tname, sub, grade, duration, kvocab, converttostring(materials))
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            max_tokens = 3550,
            stop = None,
            temperature=1.2,
        )
        print(response.choices[0]["text"])
        response = "Lesson Title: "+title+"\nTeacher Name: "+tname+"\nSubject: "+sub+"\nGrade: "+grade+"\nDate: "+date+"\nDuration: "+duration+"\nKey Vocabulary: "+kvocab+"\nSupporting Materials: "+converttostring(materials)+response.choices[0]["text"]

        filename1 = 'prompt/prompt'+i+'.txt'
        with open(filename1, 'w') as file1:
            file1.write(prompt)
        file1.close()

        filename2 = "text/generated_text"+i+".txt"
        with open(filename2, 'w') as file2:
            file2.write(response)
        file2.close()

        tts = gTTS(text=response, lang="en")
        tts.save("static/generated_speech"+i+".mp3")
        
        return render_template("index.html", result=response, filename="generated_text"+i+".txt", speech_file="generated_speech"+i+".mp3")

    result = request.args.get("result")
    return render_template("index.html", result=result)

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    file_path = os.path.join(app.root_path, 'text', filename)
    if not os.path.exists(file_path):
        return "File not found"

    # Determine the file's content type
    content_type = "text/plain"
    if filename.endswith(".txt"):
        content_type = "text/plain"
    elif filename.endswith(".pdf"):
        content_type = "application/pdf"

    # Send the file for download
    return send_file(file_path, as_attachment=True, attachment_filename=filename, mimetype=content_type)

def converttostring(l):
    s = ""
    for i in l:
        s = s + i + ", "
    return s


def generate_prompt(title, teacher_name, subject, grade, duration, keyvocab, materials):
    prompt2 = """\n
Generate a lesson plan (in the below format) for the following description of each section (Each section is important):  
1) Learning Outcome:
> Knowledge: Refers to what the teacher wants the students to learn. Includes list of key areas of knowledge.
> Skills: Skills they want students to be proficient in. Includes topic-specific skills that are being developed and taken from the curriculum.
> Understanding: Refers to what concept/s the teacher wants the students to understand.

2) Differentiation: Encourage the teacher to think about how they will make the lesson different for students who have different learning needs. This can include extra text, simplified text, video or diagrams, etc.
Respond by answering these questions - How will you modify the task for students needing additional support?
                                       How will you extend the task for students needing additional challenge?
                               
3) Learning experiences: (Medium Anwer) Includes activities to engage students with the topic.
Prepare - Focus on preparing the students for the topic that will be covered. Educators can use this time to introduce the topic, ask general questions regarding the topic, etc.
Plan - Educators will lay out the activities that they will do with the students during the lesson. 
Investigate - Students will be actively engaged in the topic. This might involve watching a video, conducting an experiment, or participating in a group discussion.
Apply - Students will use the knowledge they have gained to create something. This might involve creating a poster, presentation, report, etc.
Connect - Educators will help the students make connections between the topic they are studying and the world around them. This might involve discussing current events, etc.
Evaluate and Reflect - Students will reflect on what they have learned.

4) Educator assessment: How the teacher will assess what the students have learned. This might involve quizzes, rubrics, etc. Generate a sample method of assessment.

5) Educator reflection: Encourages teacher to reflect on the content of the lesson. Give a reflection on how the educator can improve the lesson the next time.

Apply - Once the investigation
"""

    prompt = "You are " + teacher_name + ", a grade "+ grade + " " + subject + " teacher and you want to create a lesson plan for your students to teach for the duration of " + duration + " on the topic " + title + ".\n" + "Key Vocabulary: " + keyvocab + "\nSupporting Materials: " + materials + prompt2

    return prompt
