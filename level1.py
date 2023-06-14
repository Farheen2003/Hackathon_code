import openai

openai.api_key = ""

model_engine = "text-davinci-003"

title = "Life Cycle of Frogs"
teacher_name = "TDS Education Team"
subject = "Science - Biology"
grade = "8"
date = "not applicable"
duration = "1 session 50 minutes"
keyvocab  = "Eggs, Tadpole, Froglet, Adult Frog"
materials = "Video, Laptops, Microsoft Office, TDS LSM, Live Worksheets, Others"

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

completion = openai.Completion.create(
    engine = model_engine,
    prompt = prompt,
    max_tokens = 3550,
    # n = 1,
    stop = None,
    temperature = 1.2,
)

response = completion.choices[0]["text"]
print(response)
response = "Lesson Title: "+title+"\nTeacher Name: "+teacher_name+"\nSubject: "+subject+"\nGrade: "+grade+"\nDate: "+date+"\nDuration: "+duration+"\nKey Vocabulary: "+keyvocab+"\nSupporting Materials: "+materials+response

f=open("textfile.txt", "w")
f.write(response)
f.close()