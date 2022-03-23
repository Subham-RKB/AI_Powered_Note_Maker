import os
from tkinter import *
from tkinter import messagebox
#creating the application main window
window = Tk()
window.title("AI Powered Note Maker")
window.geometry("600x600")
window.configure(bg="#000000")
window.mainloop()
import abstractive

src_text = """On or before this Friday. Maximum honor. Before this Friday 2 days I used to say but maximum I can give to tidy.
So you need to upload it and send it to me. That is one point and other groups. What I have noted what I have pointed out.
I had not thought the functionality based on the real time implementation. They're just thinking about S1 particular functionality and those five major functionality. What I told them to mention what they're doing in order to achieve the same functionality. What're the intermediary steps required to complete their making? Those things are separate separate functionality. That's not the thing that I am expecting. I'm expecting completely five different functionality for every project, so.
That OK, you said a particular concept, but there is no clarity on the functionality related to a specific domain. Some people have written a particular concept on multiple domains. Again that is not possible. Nobody can implement for multiple domain fix a particular domain and on that domain during real time, when you're implementing the concept, how will you implement what are the challenges you're going to face based on that different different functionality up to identify?
Not one functionality and the intermediary steps to achieve that particular functionality. Those will be 5 separate functionalities, no?
I told you 5 separate functionality out of that one or two functionality could be of research based which will helpful for you to write down your resource paper. So in that way you have to plug.
We need to pick up some groups again, one or two groups. I guess there at the very, very basic level they have not mentioned anything. Everything is existing. So then again, although I'm not rejecting your topic because it is not being repeated, but still you guess you think that ultimately you have to think of proper functionalities at this moment. What you have submitted? That is nothing that is nothing that is equivalent to rejection. But I am not rejecting that because it is not being repeated. But you must have to come up with.
Proper functionalities there are writing. Two such groups are there whose ideas are completely based basic. There is nothing new, no novelty, no clarity. Everything is existing, so in that case definitely have to come up with proper functionality. So it's up to you if you can match up to the comments what I have given gave me the proper justification, proper explanation, proper solution for those comments, whatever I've given apart from that, compared with the real time implementation scenario.
I will be grinding all the groups on the real time implementation of your concept, definitely.
During review one review two, I will check for only those two things.
How you're going to implement on real time variable implement? What are the challenges you're facing and how you're overcoming those challenges with different different functionalities? Definitely I will check.
So this is the overall thing that I want to give overall observation. What I have got from your review 0 document so very soon, maybe before even if 12:00 to 1:00 o'clock I will send the details to all the groups I will try. I will try definitely. Otherwise maximum today itself. Anyhow, I will sell it.
So let us start with our today's class.
Please let me know if my screen is visible.
It's beautiful, right?"""

summary = abstractive.summarize(src_text)

print(summary)
