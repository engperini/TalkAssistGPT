#retirado o flash ui, ainda falta que o loop espere a hotword nao esta bom

# MIT License
#
# Copyright (c) 2023 PeriniDev
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from ChatBotBrain import run_conversation
from custom_actions import listen, wake_word_instance, greating,startup, ready, talk, standby, save_database
import config

from time import sleep
from threading import Thread
import queue  # Importe o módulo de fila
from flask import Flask, render_template, request, send_from_directory, jsonify, Response

def main():
    #flag to agent speak
    agent_mute = config.agentmute
    #variable init
    conversation=True
    first_call = True
    history = [] #memory of conversation
    while True:
        sleep(0.05)
        #use with talk-speak
        if not agent_mute:
            if wake_word_instance.wakeup or first_call:
                print("System: awake :")
                greating()
                conversation = True
                first_call = False
                sleep(0.05)
                while conversation:
                    prompt = listen()
                    if prompt == "":
                        sleep(0.05)
                        conversation = False
                        wake_word_instance.wakeup = False
                        standby()
                        break
                    print("System heard :", prompt)
                    database_prompt = prompt
                    #append history
                    history.append(f"User: {prompt}")
                    #insert the history in the conversation to memory
                    prompt = "\n".join(history) + "\nAI:"

                    #--------#---------------------------------------
                    #run the model
                    result = run_conversation(prompt)
                    #final_aswer = result['choices'][0]['message']['content'].replace("AI: ", "")
                    final_aswer = result.choices[0].message.content.replace("AI: ", "") #update

                    # print final result
                    print("AI Result: ",final_aswer)
                    #--------#---------------------------------------          
                    
                    talk(final_aswer)
                    #append history with AI answer
                    history.append(f"AI: {final_aswer}")

                    database_answer = final_aswer

                    #save history in file
                    save_database(database_prompt,database_answer)

                    #optional token and cost calculation (only estimatade cost 0.002/1000$ depend of model and input/output token)   
                    tok = result.usage.total_tokens
                    cost = tok*0.002/1000
                    print(f"Total Tokens: {tok} Cost: {cost}$")

                    #note: As history is continuously appended the tokens in the prompt increases at the same chat section
                    #check total token per request reach 1000 or more and delete the oldest history entry
                    if tok >= 400:
                        history.pop(0)
                        print("Memory is full, the oldest entry is deleted")

                sleep(0.05)
                wake_word_instance.start_wake_thread()

                   

        else: #use with chat

            #get user input
            prompt = input("User: ")
            database_prompt = prompt
            #check if user want to exit
            if prompt.lower() == "exit":
                break

            #append history
            history.append(f"User: {prompt}")
            #insert the history in the conversation to memory
            prompt = "\n".join(history) + "\nAI:"

            #--------#---------------------------------------
            #run the model
            result = run_conversation(prompt)
            #final_aswer = result['choices'][0]['message']['content'].replace("AI: ", "") 
            final_aswer = result.choices[0].message.content.replace("AI: ", "") #update
            # print final result
            print("AI Result: ",final_aswer)
            #--------#---------------------------------------
            
            #append history with AI answer
            history.append(f"AI: {final_aswer}")
            database_answer = final_aswer

            
            #save history in file
            save_database(database_prompt,database_answer)

            #optional token and cost calculation (only estimatade cost 0.002/1000$ depend of model and input/output token)   
            tok = result.usage.total_tokens
            cost = tok*0.002/1000
            print(f"Total Tokens: {tok} Cost: {cost}$")

            #note: As history is continuously appended the tokens in the prompt increases at the same chat section
            #check total token per request reach 400 or more and delete the oldest history entry
            if tok >= 400:
                history.pop(0)
                print("Memory is full, the oldest entry is deleted")
        
        return final_aswer 



# app = Flask(__name__)
# app.static_folder = 'static'


# # Crie uma fila para passar a resposta da AI do thread principal para a Thread da aplicação
# ai_response_queue = queue.Queue()

# # Função para obter a resposta da AI e colocá-la na fila
# def get_ai_response():
#     ai_response = main()  #  retorna a resposta da AI
#     ai_response_queue.put(ai_response)

# @app.route("/")
# def index():
#     #startup()
#     #if not config.agentmute:
#     #    wake_word_instance.start_wake_thread()
#     #start main() as a new thread
#     Thread(target=get_ai_response).start()
#     #ready()
#     return render_template("index.html")

# # Rota para transmitir atualizações da resposta da AI em tempo real
# @app.route('/ai_response_stream')
# def ai_response_stream():
#     def generate_ai_responses():
#         while True:
#             try:
#                 # Obtenha a resposta da AI da fila
#                 ai_response = ai_response_queue.get()
                
                
#                 yield "data: {}\n\n".format(ai_response)
#             except Exception as e:
#                 print("Erro ao gerar evento SSE:", e)
            

    
#     return Response (generate_ai_responses(), content_type="text/event-stream")
        
# if __name__ == '__main__':
#     app.run()


if __name__ == '__main__':
        
    main()
    #startup()
    if not config.agentmute:
        wake_word_instance.start_wake_thread()
    
    #start main() as a new thread
    #Thread(target=main).start()
    #ready()
    


        
        
        