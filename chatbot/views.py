from django.http import JsonResponse
from django.shortcuts import redirect
import google.generativeai as genai


API_KEY ='AIzaSyCdfzZKwlzgJvJihjUfW7uxtS_mNbrIjXk'
genai.configure(
    api_key=API_KEY
)
model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=[])



def chatView(request):

    if (request.method=="POST"):
        query = request.POST.get('user_query')
        #print(query)
        query = query + 'The answer should be in the format first answer the question in a maximum 100 words paragrah and add upto five points if needed. check the question i asked and if it is irrelevent in the topic "Mensturation or womens physical and mental health " only replay sorry i cant answer with the message'
        try:
            response = chat.send_message(query).candidates[0].content.parts[0].text
            return JsonResponse({'response' : response})
        except:
            print("Safety rating is high. Error message:")
            return JsonResponse({'response' : 'Due to Some saftey ratings You cant ask directly. ask quite polietly'})

                


# while(True):
#     question = input("you: ")
#     if(question.strip() == ''):
#         break

#     response = chat.send_message(question)
#     print('\n')
#     print(f"Bot :{response.text}")
#     print('\n')