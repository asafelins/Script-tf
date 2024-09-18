import tkinter as tk
from tkinter import scrolledtext
from threading import Thread
import keyboard
import pyautogui
from time import sleep
from time import time
import sys
import hashlib
import platform
from datetime import datetime, timedelta,timezone
import pyperclip
import requests




def obter_hwid():
    # Obtém o HWID do sistema
    system_info = platform.uname()
    hwid_data = f"{system_info.node}{system_info.processor}{system_info.system}"
    return hashlib.sha256(hwid_data.encode()).hexdigest()

def copiar_hwid():
    # Obtém e copia o HWID atual para a área de transferência
    hwid_atual = obter_hwid()
    pyperclip.copy(hwid_atual)

def obter_data_remota():
    # Faz uma solicitação GET para o endpoint que retorna a data atual
    url = "https://worldtimeapi.org/api/timezone/America/Sao_Paulo"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            data_json = response.json()
            data_str = data_json["datetime"]
            data_atual = datetime.fromisoformat(data_str)
            data_atual = data_atual.replace(tzinfo=timezone.utc)  # Adicionar o fuso horário UTC
            return data_atual
        else:
            print("Falha ao obter a data remota.")
    except requests.exceptions.RequestException as e:
        print(f"Erro de conexão: {e}")
    return None

def verificar_licenca(hwid_esperado, data_criacao_licenca):
    # Verifica se o HWID atual é o mesmo que o especificado
    hwid_atual = obter_hwid()
    if hwid_atual != hwid_esperado:
        return False
    # Verifica a data de criação da licença
    data_atual = obter_data_remota()
    if data_atual and data_atual > data_criacao_licenca.replace(tzinfo=timezone.utc) + timedelta(days=300):
        return False
    return True

# Defina o HWID esperado e a data de criação da licença
hwid_esperado = "737c252ca6be6bb9c8eef707f2e769d0899d1486fedbbf7ab7f350a3e4501cb6"
data_criacao_licenca = datetime(2024, 5, 11, tzinfo=timezone.utc)  # Data de criação da licença com fuso horário UTC

# Verifique a licença com base no HWID esperado e na data de criação
if verificar_licenca(hwid_esperado, data_criacao_licenca):
    print("Licença válida. O software pode ser executado neste PC.")
else:
    # Exibir caixa de diálogo de alerta com informações sobre a licença e o botão para copiar o HWID
    root = tk.Tk()
    root.withdraw()  # Esconder a janela principal

    # Criar a janela de alerta
    janela_alerta = tk.Toplevel(root)
    janela_alerta.title("Erro")
    janela_alerta.geometry("400x150")
    janela_alerta.iconbitmap("fotos/icon.ico")
    janela_alerta.resizable(False, False)

    hwid_atual = obter_hwid()
    mensagem = f"HWID não registrado ou licença expirada.\n\n{hwid_atual}\nData de criação da licença: {data_criacao_licenca.strftime('%d/%m/%Y')}"

    # Adicionar a mensagem de erro na janela
    lbl_mensagem = tk.Label(janela_alerta, text=mensagem)
    lbl_mensagem.pack(pady=10)

    # Adicionar o botão para copiar o HWID
    copiar_botao = tk.Button(janela_alerta, text="Copiar HWID", command=copiar_hwid)
    copiar_botao.pack(pady=5)

    janela_alerta.protocol("WM_DELETE_WINDOW", lambda: [janela_alerta.destroy(), root.quit()])

    root.mainloop()
    sys.exit(1)
    








class AutomacaoGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Script TF")
        self.root.iconbitmap("fotos/icon.ico")
        
        # Configura a janela para ficar sempre no topo
        self.root.attributes("-topmost", True)
        
        # Define o tamanho mínimo e máximo da janela
        self.root.minsize(300, 340)
        self.root.maxsize(300, 340)
        
        # Define o tamanho fixo da janela
        self.root.geometry("300x340")
        
        # Remove a opção de redimensionar a janela
        self.root.resizable(False, False)
        
        self.btn_iniciar = tk.Button(self.root, text="Iniciar", command=self.iniciar_automacao, width=8)
        self.btn_iniciar.pack(pady=3)
        
        self.btn_parar = tk.Button(self.root, text="Parar", command=self.parar_automacao, state=tk.DISABLED, width=8)
        self.btn_parar.pack(pady=3)
        
        self.texto_info = tk.Label(self.root, text="Mantenha pressionada a tecla ctrl para parar.", fg="red")
        self.texto_info.pack(pady=5)
        
        # Widget de texto para exibir os prints da automação
        self.txt_output = scrolledtext.ScrolledText(self.root, width=100, height=15)
        self.txt_output.pack(pady=5)
        
        
        self.automacao_thread = None
        self.executando = False

    def iniciar_automacao(self):
        self.txt_output.delete(1.0, tk.END)
        self.executando = True
        self.automacao_thread = Thread(target=self.automacao_loop)
        self.automacao_thread.start()
        self.btn_iniciar.config(state=tk.DISABLED)
        self.btn_parar.config(state=tk.NORMAL)
    
    def parar_automacao(self):
        if self.executando == True:  # Verifica se a automação está em andamento
            print('Script Finalizado...')
            self.executando = False
            self.btn_iniciar.config(state=tk.NORMAL)
            self.btn_parar.config(state=tk.DISABLED)
            
            if self.automacao_thread and self.automacao_thread.is_alive():
                self.automacao_thread.join()
                self.btn_iniciar.config(state=tk.NORMAL)
                self.btn_parar.config(state=tk.DISABLED)
    
    def automacao_loop(self):
        contador = 0
        apagadas = 0
        crash = 0
        
        # Redireciona o stdout para o widget de texto
        sys.stdout = self
        
        braked = False
        contador = 0
        mechas = 0



        while keyboard.is_pressed('ctrl') == False: 
            braked = False
            contador += 1
            #print(f"Contador: {contador}")
            

            
                

            tempo_inicio = time()
            tempo_atual = time()
            tempo_execucao = tempo_atual - tempo_inicio




            if contador == 10:
                if pyautogui.locateCenterOnScreen("fotos/atualizar.png", confidence=0.7):
                    pyautogui.click(pyautogui.locateCenterOnScreen("fotos/atualizar.png", confidence=0.7))
                    sleep(2)
                
            
            elif contador == 20:
                
                if pyautogui.locateCenterOnScreen("fotos/atualizar.png", confidence=0.7):
                    pyautogui.click(pyautogui.click(pyautogui.locateCenterOnScreen("fotos/atualizar.png", confidence=0.7)))
                    sleep(2)
                    pyautogui.moveTo(pyautogui.locateCenterOnScreen("fotos/center.png", confidence=0.7))
                    sleep(1)
                    pyautogui.scroll(-200)
                    sleep(1)
                contador = 0
            



                

            if pyautogui.locateCenterOnScreen("fotos/recompensa.png", confidence=0.7): #resgatando recompenca
                print("Coletando recompenca")

                pyautogui.click(pyautogui.locateCenterOnScreen("fotos/recompensa.png", confidence=0.7))
                sleep(1)
                pyautogui.click(pyautogui.locateCenterOnScreen("fotos/botrec.png", confidence=0.6))
                sleep(1)
                pyautogui.click(pyautogui.locateCenterOnScreen("fotos/coletar.png", confidence=0.7))
                sleep(1)
                braked = True
                sleep(1)

            elif pyautogui.locateCenterOnScreen("fotos/ag.png", confidence=0.7): #achou atq gratis 
                #print("achei ataque gratis")
                pyautogui.click(pyautogui.locateCenterOnScreen("fotos/ag.png", confidence=0.7))
                sleep(2)
                
                        

                if pyautogui.locateCenterOnScreen("fotos/erro.png", confidence=0.6):
                    print("Encontrei um erro e estou voltando")
                    sleep(1)
                    pyautogui.click(pyautogui.locateCenterOnScreen("fotos/voltar.png", confidence=0.7)) #da pra melhorar aqui dps
                    sleep(1)
                    braked = True
                
                elif pyautogui.locateCenterOnScreen("fotos/atqgratis.png", confidence=0.6):
                    
                    #print("Tudo certo, agora vou ver a faccao")
                    sleep(2)


                    if pyautogui.locateCenterOnScreen("fotos/louva.png", confidence=0.7): #verde 
                        #print("Verde")

                        if pyautogui.locateCenterOnScreen("fotos/mecha80.png", confidence=0.7) or pyautogui.locateCenterOnScreen("fotos/mecha100.png", confidence=0.7) or pyautogui.locateCenterOnScreen("fotos/mecha120.png", confidence=0.7) or pyautogui.locateCenterOnScreen("fotos/mecha140.png", confidence=0.7) or pyautogui.locateCenterOnScreen("fotos/mecha160.png", confidence=0.7):
                            print("Mecha descartavel")
                            pyautogui.click(pyautogui.locateCenterOnScreen("fotos/voltar.png", confidence=0.7)) #clica em voltar
                            sleep(1)
                            pyautogui.click(pyautogui.locateCenterOnScreen("fotos/atualizar.png", confidence=0.7)) 
                            sleep(1)
                            

                        
                        elif pyautogui.locateCenterOnScreen("fotos/mecha180.png", confidence=0.7) or pyautogui.locateCenterOnScreen("fotos/mecha200.png", confidence=0.7) or pyautogui.locateCenterOnScreen("fotos/mecha240.png", confidence=0.7) or pyautogui.locateCenterOnScreen("fotos/mecha280.png", confidence=0.7) or pyautogui.locateCenterOnScreen("fotos/mecha315.png", confidence=0.7):
                            print("Mecha aceitavel")
                            sleep(0.5)
                            pyautogui.click(pyautogui.locateCenterOnScreen("fotos/atqgratis.png", confidence=0.6)) #clica no botao de ataque gratis
                            sleep(0.5)
                            pyautogui.click(pyautogui.locateCenterOnScreen("fotos/equipe.png", confidence=0.7)) #clica no botao de equipe
                            sleep(0.5)
                            if pyautogui.locateCenterOnScreen("fotos/b2.png", confidence=0.8):
                                pyautogui.click(pyautogui.locateCenterOnScreen("fotos/b2.png", confidence=0.8)) #escolhe a equipe
                                sleep(0.5)
                                pyautogui.click(pyautogui.locateCenterOnScreen("fotos/lutar.png", confidence=0.7)) #clica no botao lutar
                                sleep(6)
                                if pyautogui.locateCenterOnScreen("fotos/erro2.png", confidence=0.8):
                                    sleep(1)
                                    pyautogui.click(pyautogui.locateCenterOnScreen("fotos/continuar2.png", confidence=0.7)) #clica em voltar
                                    sleep(1)
                                    braked = True

                                else:
                                    pyautogui.click(pyautogui.locateCenterOnScreen("fotos/skip.png", confidence=0.7)) # clica no botao skipar
                                    sleep(2)
                                    pyautogui.click(pyautogui.locateCenterOnScreen("fotos/continuar.png", confidence=0.6))#clica continuar
                                    sleep(1)
                                    if pyautogui.locateCenterOnScreen("fotos/botrec.png", confidence=0.6):
                                        pyautogui.click(pyautogui.locateCenterOnScreen("fotos/botrec.png", confidence=0.6)) 
                                        sleep(2)
                                        pyautogui.click(pyautogui.locateCenterOnScreen("fotos/coletar.png", confidence=0.7))
                                        sleep(1)
                                        mechas += 1
                                        print(f"Mecha:{mechas}")
                                        braked = True
                                    else:
                                        pyautogui.click(pyautogui.locateCenterOnScreen("fotos/voltar.png", confidence=0.7))
                                        sleep(1)
                                        mechas += 1
                                        print(f"Mecha:{mechas}")
                                        braked = True

                            elif pyautogui.locateCenterOnScreen("fotos/b22.png", confidence=0.8):
                                pyautogui.click(pyautogui.locateCenterOnScreen("fotos/b22.png", confidence=0.8)) #escolhe a equipe
                                sleep(0.5)
                                pyautogui.click(pyautogui.locateCenterOnScreen("fotos/lutar.png", confidence=0.7)) #clica no botao lutar
                                sleep(6)
                                if pyautogui.locateCenterOnScreen("fotos/erro2.png", confidence=0.7):
                                    sleep(1)
                                    pyautogui.click(pyautogui.locateCenterOnScreen("fotos/continuar2.png", confidence=0.7)) #clica em voltar
                                    sleep(1)
                                    braked = True

                                else:
                                    pyautogui.click(pyautogui.locateCenterOnScreen("fotos/skip.png", confidence=0.7)) # clica no botao skipar
                                    sleep(2)
                                    pyautogui.click(pyautogui.locateCenterOnScreen("fotos/continuar.png", confidence=0.6))#clica continuar
                                    sleep(1)
                                    if pyautogui.locateCenterOnScreen("fotos/botrec.png", confidence=0.6):
                                        pyautogui.click(pyautogui.locateCenterOnScreen("fotos/botrec.png", confidence=0.6)) 
                                        sleep(2)
                                        pyautogui.click(pyautogui.locateCenterOnScreen("fotos/coletar.png", confidence=0.7))
                                        sleep(1)
                                        mechas += 1
                                        print(f"Mecha:{mechas}")
                                        braked = True
                                    else:
                                        pyautogui.click(pyautogui.locateCenterOnScreen("fotos/voltar.png", confidence=0.7))
                                        sleep(1)
                                        mechas += 1
                                        print(f"Mecha:{mechas}")
                                        braked = True







                    elif pyautogui.locateCenterOnScreen("fotos/kodiak.png", confidence=0.7): #vermelho 
                        #print("Vermelho")

                        if pyautogui.locateCenterOnScreen("fotos/mecha80.png", confidence=0.7) or pyautogui.locateCenterOnScreen("fotos/mecha100.png", confidence=0.7) or pyautogui.locateCenterOnScreen("fotos/mecha120.png", confidence=0.7) or pyautogui.locateCenterOnScreen("fotos/mecha140.png", confidence=0.7) or pyautogui.locateCenterOnScreen("fotos/mecha160.png", confidence=0.7):
                            print("Mecha descartavel")
                            pyautogui.click(pyautogui.locateCenterOnScreen("fotos/voltar.png", confidence=0.7)) #clica em voltar
                            sleep(1)
                            pyautogui.click(pyautogui.locateCenterOnScreen("fotos/atualizar.png", confidence=0.7)) 
                            sleep(1)
                            

                        
                        elif pyautogui.locateCenterOnScreen("fotos/mecha180.png", confidence=0.7) or pyautogui.locateCenterOnScreen("fotos/mecha200.png", confidence=0.7) or pyautogui.locateCenterOnScreen("fotos/mecha240.png", confidence=0.7):
                            print("Mecha aceitavel")
                            sleep(0.5)
                            pyautogui.click(pyautogui.locateCenterOnScreen("fotos/atqgratis.png", confidence=0.6))
                            sleep(0.5)
                            pyautogui.click(pyautogui.locateCenterOnScreen("fotos/equipe.png", confidence=0.7))
                            sleep(0.5)
                            if pyautogui.locateCenterOnScreen("fotos/b3.png", confidence=0.9):
                                pyautogui.click(pyautogui.locateCenterOnScreen("fotos/b3.png", confidence=0.9)) #escolhe a equipe
                                sleep(0.5)
                                pyautogui.click(pyautogui.locateCenterOnScreen("fotos/lutar.png", confidence=0.7)) #clica no botao lutar
                                sleep(6)
                                if pyautogui.locateCenterOnScreen("fotos/erro2.png", confidence=0.7):
                                    sleep(1)
                                    pyautogui.click(pyautogui.locateCenterOnScreen("fotos/continuar2.png", confidence=0.7)) #clica em voltar
                                    sleep(1)
                                    braked = True

                                else:
                                    pyautogui.click(pyautogui.locateCenterOnScreen("fotos/skip.png", confidence=0.7)) # clica no botao skipar
                                    sleep(2)
                                    pyautogui.click(pyautogui.locateCenterOnScreen("fotos/continuar.png", confidence=0.6))#clica continuar
                                    sleep(1)
                                    if pyautogui.locateCenterOnScreen("fotos/botrec.png", confidence=0.6):
                                        pyautogui.click(pyautogui.locateCenterOnScreen("fotos/botrec.png", confidence=0.6)) 
                                        sleep(2)
                                        pyautogui.click(pyautogui.locateCenterOnScreen("fotos/coletar.png", confidence=0.7))
                                        sleep(1)
                                        mechas += 1
                                        print(f"Mecha:{mechas}")
                                        braked = True
                                    else:
                                        pyautogui.click(pyautogui.locateCenterOnScreen("fotos/voltar.png", confidence=0.7))
                                        sleep(1)
                                        mechas += 1
                                        print(f"Mecha:{mechas}")
                                        braked = True

                            elif pyautogui.locateCenterOnScreen("fotos/b33.png", confidence=0.9):
                                pyautogui.click(pyautogui.locateCenterOnScreen("fotos/b33.png", confidence=0.9)) #escolhe a equipe
                                sleep(0.5)
                                pyautogui.click(pyautogui.locateCenterOnScreen("fotos/lutar.png", confidence=0.7)) #clica no botao lutar
                                sleep(6)
                                if pyautogui.locateCenterOnScreen("fotos/erro2.png", confidence=0.7):
                                    sleep(1)
                                    pyautogui.click(pyautogui.locateCenterOnScreen("fotos/continuar2.png", confidence=0.7)) #clica em voltar
                                    sleep(1)
                                    braked = True

                                else:
                                    pyautogui.click(pyautogui.locateCenterOnScreen("fotos/skip.png", confidence=0.7)) # clica no botao skipar
                                    sleep(2)
                                    pyautogui.click(pyautogui.locateCenterOnScreen("fotos/continuar.png", confidence=0.6))#clica continuar
                                    sleep(1)
                                    if pyautogui.locateCenterOnScreen("fotos/botrec.png", confidence=0.6):
                                        pyautogui.click(pyautogui.locateCenterOnScreen("fotos/botrec.png", confidence=0.6)) 
                                        sleep(2)
                                        pyautogui.click(pyautogui.locateCenterOnScreen("fotos/coletar.png", confidence=0.7))
                                        sleep(1)
                                        mechas += 1
                                        print(f"Mecha:{mechas}")
                                        braked = True
                                    else:
                                        pyautogui.click(pyautogui.locateCenterOnScreen("fotos/voltar.png", confidence=0.7))
                                        sleep(1)
                                        mechas += 1
                                        print(f"Mecha:{mechas}")
                                        braked = True


                        elif pyautogui.locateCenterOnScreen("fotos/mecha280.png", confidence=0.7) or pyautogui.locateCenterOnScreen("fotos/mecha315.png", confidence=0.7):
                            print("Mecha aceitavel")
                            sleep(0.5)
                            pyautogui.click(pyautogui.locateCenterOnScreen("fotos/atqgratis.png", confidence=0.6))
                            sleep(0.5)
                            pyautogui.click(pyautogui.locateCenterOnScreen("fotos/equipe.png", confidence=0.7))
                            sleep(0.5)
                            if pyautogui.locateCenterOnScreen("fotos/b5.png", confidence=0.9):
                                pyautogui.click(pyautogui.locateCenterOnScreen("fotos/b5.png", confidence=0.9)) #escolhe a equipe
                                sleep(0.5)
                                pyautogui.click(pyautogui.locateCenterOnScreen("fotos/lutar.png", confidence=0.7)) #clica no botao lutar
                                sleep(6)
                                if pyautogui.locateCenterOnScreen("fotos/erro2.png", confidence=0.7):
                                    sleep(1)
                                    pyautogui.click(pyautogui.locateCenterOnScreen("fotos/continuar2.png", confidence=0.7)) #clica em voltar
                                    sleep(1)
                                    braked = True

                                else:
                                    pyautogui.click(pyautogui.locateCenterOnScreen("fotos/skip.png", confidence=0.7)) # clica no botao skipar
                                    sleep(2)
                                    pyautogui.click(pyautogui.locateCenterOnScreen("fotos/continuar.png", confidence=0.6))#clica continuar
                                    sleep(1)
                                    if pyautogui.locateCenterOnScreen("fotos/botrec.png", confidence=0.6):
                                        pyautogui.click(pyautogui.locateCenterOnScreen("fotos/botrec.png", confidence=0.6)) 
                                        sleep(2)
                                        pyautogui.click(pyautogui.locateCenterOnScreen("fotos/coletar.png", confidence=0.7))
                                        sleep(1)
                                        mechas += 1
                                        print(f"Mecha:{mechas}")
                                        braked = True
                                    else:
                                        pyautogui.click(pyautogui.locateCenterOnScreen("fotos/voltar.png", confidence=0.7))
                                        sleep(1)
                                        mechas += 1
                                        print(f"Mecha:{mechas}")
                                        braked = True

                            elif pyautogui.locateCenterOnScreen("fotos/b55.png", confidence=0.9):
                                pyautogui.click(pyautogui.locateCenterOnScreen("fotos/b55.png", confidence=0.9)) #escolhe a equipe
                                sleep(0.5)
                                pyautogui.click(pyautogui.locateCenterOnScreen("fotos/lutar.png", confidence=0.7)) #clica no botao lutar
                                sleep(6)
                                if pyautogui.locateCenterOnScreen("fotos/erro2.png", confidence=0.7):
                                    sleep(1)
                                    pyautogui.click(pyautogui.locateCenterOnScreen("fotos/continuar2.png", confidence=0.7)) #clica em voltar
                                    sleep(1)
                                    braked = True

                                else:
                                    pyautogui.click(pyautogui.locateCenterOnScreen("fotos/skip.png", confidence=0.7)) # clica no botao skipar
                                    sleep(2)
                                    pyautogui.click(pyautogui.locateCenterOnScreen("fotos/continuar.png", confidence=0.6))#clica continuar
                                    sleep(1)
                                    if pyautogui.locateCenterOnScreen("fotos/botrec.png", confidence=0.6):
                                        pyautogui.click(pyautogui.locateCenterOnScreen("fotos/botrec.png", confidence=0.6)) 
                                        sleep(2)
                                        pyautogui.click(pyautogui.locateCenterOnScreen("fotos/coletar.png", confidence=0.7))
                                        sleep(1)
                                        mechas += 1
                                        print(f"Mecha:{mechas}")
                                        braked = True
                                    else:
                                        pyautogui.click(pyautogui.locateCenterOnScreen("fotos/voltar.png", confidence=0.7))
                                        sleep(1)
                                        mechas += 1
                                        print(f"Mecha:{mechas}")
                                        braked = True



                    elif pyautogui.locateCenterOnScreen("fotos/simios.png", confidence=0.7): #amarelo
                        #print("Amarelo")


                        if pyautogui.locateCenterOnScreen("fotos/mecha80.png", confidence=0.7) or pyautogui.locateCenterOnScreen("fotos/mecha100.png", confidence=0.7) or pyautogui.locateCenterOnScreen("fotos/mecha120.png", confidence=0.7) or pyautogui.locateCenterOnScreen("fotos/mecha140.png", confidence=0.7) or pyautogui.locateCenterOnScreen("fotos/mecha160.png", confidence=0.7):
                            print("Mecha descartavel")
                            pyautogui.click(pyautogui.locateCenterOnScreen("fotos/voltar.png", confidence=0.7)) #clica em voltar
                            sleep(1)
                            pyautogui.click(pyautogui.locateCenterOnScreen("fotos/atualizar.png", confidence=0.7)) 
                            sleep(1)
                            

                        
                        elif pyautogui.locateCenterOnScreen("fotos/mecha180.png", confidence=0.7) or pyautogui.locateCenterOnScreen("fotos/mecha200.png", confidence=0.7) or pyautogui.locateCenterOnScreen("fotos/mecha240.png", confidence=0.7) or pyautogui.locateCenterOnScreen("fotos/mecha280.png", confidence=0.7) or pyautogui.locateCenterOnScreen("fotos/mecha315.png", confidence=0.7):
                            print("Mecha aceitavel")
                            sleep(0.5)
                            pyautogui.click(pyautogui.locateCenterOnScreen("fotos/atqgratis.png", confidence=0.6))
                            sleep(0.5)
                            pyautogui.click(pyautogui.locateCenterOnScreen("fotos/equipe.png", confidence=0.7))
                            sleep(0.5)
                            if pyautogui.locateCenterOnScreen("fotos/b3.png", confidence=0.9):
                                pyautogui.click(pyautogui.locateCenterOnScreen("fotos/b3.png", confidence=0.9)) #escolhe a equipe
                                sleep(0.5)
                                pyautogui.click(pyautogui.locateCenterOnScreen("fotos/lutar.png", confidence=0.7)) #clica no botao lutar
                                sleep(6)
                                if pyautogui.locateCenterOnScreen("fotos/erro2.png", confidence=0.7):
                                    sleep(1)
                                    pyautogui.click(pyautogui.locateCenterOnScreen("fotos/continuar2.png", confidence=0.7)) #clica em voltar
                                    sleep(1)
                                    braked = True

                                else:
                                    pyautogui.click(pyautogui.locateCenterOnScreen("fotos/skip.png", confidence=0.7)) # clica no botao skipar
                                    sleep(2)
                                    pyautogui.click(pyautogui.locateCenterOnScreen("fotos/continuar.png", confidence=0.6))#clica continuar
                                    sleep(1)
                                    if pyautogui.locateCenterOnScreen("fotos/botrec.png", confidence=0.6):
                                        pyautogui.click(pyautogui.locateCenterOnScreen("fotos/botrec.png", confidence=0.6)) 
                                        sleep(2)
                                        pyautogui.click(pyautogui.locateCenterOnScreen("fotos/coletar.png", confidence=0.7))
                                        sleep(1)
                                        mechas += 1
                                        print(f"Mecha:{mechas}")
                                        braked = True
                                    else:
                                        pyautogui.click(pyautogui.locateCenterOnScreen("fotos/voltar.png", confidence=0.7))
                                        sleep(1)
                                        mechas += 1
                                        print(f"Mecha:{mechas}")
                                        braked = True
                            
                            elif pyautogui.locateCenterOnScreen("fotos/b33.png", confidence=0.9):
                                pyautogui.click(pyautogui.locateCenterOnScreen("fotos/b33.png", confidence=0.9)) #escolhe a equipe
                                sleep(0.5)
                                pyautogui.click(pyautogui.locateCenterOnScreen("fotos/lutar.png", confidence=0.7)) #clica no botao lutar
                                sleep(6)
                                if pyautogui.locateCenterOnScreen("fotos/erro2.png", confidence=0.7):
                                    sleep(1)
                                    pyautogui.click(pyautogui.locateCenterOnScreen("fotos/continuar2.png", confidence=0.7)) #clica em voltar
                                    sleep(1)
                                    braked = True

                                else:
                                    pyautogui.click(pyautogui.locateCenterOnScreen("fotos/skip.png", confidence=0.7)) # clica no botao skipar
                                    sleep(2)
                                    pyautogui.click(pyautogui.locateCenterOnScreen("fotos/continuar.png", confidence=0.6))#clica continuar
                                    sleep(1)
                                    if pyautogui.locateCenterOnScreen("fotos/botrec.png", confidence=0.6):
                                        pyautogui.click(pyautogui.locateCenterOnScreen("fotos/botrec.png", confidence=0.6)) 
                                        sleep(2)
                                        pyautogui.click(pyautogui.locateCenterOnScreen("fotos/coletar.png", confidence=0.7))
                                        sleep(1)
                                        mechas += 1
                                        print(f"Mecha:{mechas}")
                                        braked = True
                                    else:
                                        pyautogui.click(pyautogui.locateCenterOnScreen("fotos/voltar.png", confidence=0.7))
                                        sleep(1)
                                        mechas += 1
                                        print(f"Mecha:{mechas}")
                                        braked = True







                    elif pyautogui.locateCenterOnScreen("fotos/grou.png", confidence=0.7): #azul
                        #print("Azul") 


                        if pyautogui.locateCenterOnScreen("fotos/mecha80.png", confidence=0.7) or pyautogui.locateCenterOnScreen("fotos/mecha100.png", confidence=0.7) or pyautogui.locateCenterOnScreen("fotos/mecha120.png", confidence=0.7) or pyautogui.locateCenterOnScreen("fotos/mecha140.png", confidence=0.7) or pyautogui.locateCenterOnScreen("fotos/mecha160.png", confidence=0.7):
                            print("Mecha descartavel")
                            pyautogui.click(pyautogui.locateCenterOnScreen("fotos/voltar.png", confidence=0.7)) #clica em voltar
                            sleep(1)
                            pyautogui.click(pyautogui.locateCenterOnScreen("fotos/atualizar.png", confidence=0.7)) 
                            sleep(1)
                            

                        
                        elif pyautogui.locateCenterOnScreen("fotos/mecha180.png", confidence=0.7) or pyautogui.locateCenterOnScreen("fotos/mecha200.png", confidence=0.7) or pyautogui.locateCenterOnScreen("fotos/mecha240.png", confidence=0.7) or pyautogui.locateCenterOnScreen("fotos/mecha280.png", confidence=0.7) or pyautogui.locateCenterOnScreen("fotos/mecha315.png", confidence=0.7):
                            print("Mecha aceitavel")
                            sleep(0.5)
                            pyautogui.click(pyautogui.locateCenterOnScreen("fotos/atqgratis.png", confidence=0.6))
                            sleep(0.5)
                            pyautogui.click(pyautogui.locateCenterOnScreen("fotos/equipe.png", confidence=0.7))
                            sleep(0.5)
                            if pyautogui.locateCenterOnScreen("fotos/b1.png", confidence=0.8):
                                pyautogui.click(pyautogui.locateCenterOnScreen("fotos/b1.png", confidence=0.8)) #escolhe a equipe
                                sleep(0.5)
                                pyautogui.click(pyautogui.locateCenterOnScreen("fotos/lutar.png", confidence=0.7)) #clica no botao lutar
                                sleep(6)
                                if pyautogui.locateCenterOnScreen("fotos/erro2.png", confidence=0.7):
                                    sleep(1)
                                    pyautogui.click(pyautogui.locateCenterOnScreen("fotos/continuar2.png", confidence=0.7)) #clica em voltar
                                    sleep(1)
                                    braked = True

                                else:
                                    pyautogui.click(pyautogui.locateCenterOnScreen("fotos/skip.png", confidence=0.7)) # clica no botao skipar
                                    sleep(2)
                                    pyautogui.click(pyautogui.locateCenterOnScreen("fotos/continuar.png", confidence=0.6))#clica continuar
                                    sleep(1)
                                    if pyautogui.locateCenterOnScreen("fotos/botrec.png", confidence=0.6):
                                        pyautogui.click(pyautogui.locateCenterOnScreen("fotos/botrec.png", confidence=0.6)) 
                                        sleep(2)
                                        pyautogui.click(pyautogui.locateCenterOnScreen("fotos/coletar.png", confidence=0.7))
                                        sleep(1)
                                        mechas += 1
                                        print(f"Mecha:{mechas}")
                                        braked = True
                                    else:
                                        pyautogui.click(pyautogui.locateCenterOnScreen("fotos/voltar.png", confidence=0.7))
                                        sleep(1)
                                        mechas += 1
                                        print(f"Mecha:{mechas}")
                                        braked = True

                            elif pyautogui.locateCenterOnScreen("fotos/b11.png", confidence=0.8):
                                pyautogui.click(pyautogui.locateCenterOnScreen("fotos/b11.png", confidence=0.8)) #escolhe a equipe
                                sleep(0.5)
                                pyautogui.click(pyautogui.locateCenterOnScreen("fotos/lutar.png", confidence=0.7)) #clica no botao lutar
                                sleep(6)
                                if pyautogui.locateCenterOnScreen("fotos/erro2.png", confidence=0.7):
                                    sleep(1)
                                    pyautogui.click(pyautogui.locateCenterOnScreen("fotos/continuar2.png", confidence=0.7)) #clica em voltar
                                    sleep(1)
                                    braked = True

                                else:
                                    pyautogui.click(pyautogui.locateCenterOnScreen("fotos/skip.png", confidence=0.7)) # clica no botao skipar
                                    sleep(2)
                                    pyautogui.click(pyautogui.locateCenterOnScreen("fotos/continuar.png", confidence=0.6))#clica continuar
                                    sleep(1)
                                    if pyautogui.locateCenterOnScreen("fotos/botrec.png", confidence=0.6):
                                        pyautogui.click(pyautogui.locateCenterOnScreen("fotos/botrec.png", confidence=0.6)) 
                                        sleep(2)
                                        pyautogui.click(pyautogui.locateCenterOnScreen("fotos/coletar.png", confidence=0.7))
                                        sleep(1)
                                        mechas += 1
                                        print(f"Mecha:{mechas}")
                                        braked = True
                                    else:
                                        pyautogui.click(pyautogui.locateCenterOnScreen("fotos/voltar.png", confidence=0.7))
                                        sleep(1)
                                        mechas += 1
                                        print(f"Mecha:{mechas}")
                                        braked = True





                    elif pyautogui.locateCenterOnScreen("fotos/serpente.png", confidence=0.7): #roxo 
                        #print("Roxo")

                        if pyautogui.locateCenterOnScreen("fotos/mecha80.png", confidence=0.7) or pyautogui.locateCenterOnScreen("fotos/mecha100.png", confidence=0.7) or pyautogui.locateCenterOnScreen("fotos/mecha120.png", confidence=0.7) or pyautogui.locateCenterOnScreen("fotos/mecha140.png", confidence=0.7) or pyautogui.locateCenterOnScreen("fotos/mecha160.png", confidence=0.7):
                            print("Mecha descartavel")
                            pyautogui.click(pyautogui.locateCenterOnScreen("fotos/voltar.png", confidence=0.7)) #clica em voltar
                            sleep(1)
                            pyautogui.click(pyautogui.locateCenterOnScreen("fotos/atualizar.png", confidence=0.7)) 
                            sleep(1)
                            

                        
                        elif pyautogui.locateCenterOnScreen("fotos/mecha180.png", confidence=0.7) or pyautogui.locateCenterOnScreen("fotos/mecha200.png", confidence=0.7) or pyautogui.locateCenterOnScreen("fotos/mecha240.png", confidence=0.7) or pyautogui.locateCenterOnScreen("fotos/mecha280.png", confidence=0.7) or pyautogui.locateCenterOnScreen("fotos/mecha315.png", confidence=0.7):
                            print("Mecha aceitavel")
                            sleep(0.5)
                            pyautogui.click(pyautogui.locateCenterOnScreen("fotos/atqgratis.png", confidence=0.6))
                            sleep(0.5)
                            pyautogui.click(pyautogui.locateCenterOnScreen("fotos/equipe.png", confidence=0.7))
                            sleep(0.5)
                            if pyautogui.locateCenterOnScreen("fotos/b3.png", confidence=0.9):
                                pyautogui.click(pyautogui.locateCenterOnScreen("fotos/b3.png", confidence=0.9)) #escolhe a equipe
                                sleep(0.5)
                                pyautogui.click(pyautogui.locateCenterOnScreen("fotos/lutar.png", confidence=0.7)) #clica no botao lutar
                                sleep(6)
                                if pyautogui.locateCenterOnScreen("fotos/erro2.png", confidence=0.7):
                                    sleep(1)
                                    pyautogui.click(pyautogui.locateCenterOnScreen("fotos/continuar2.png", confidence=0.7)) #clica em voltar
                                    sleep(1)
                                    braked = True

                                else:
                                    pyautogui.click(pyautogui.locateCenterOnScreen("fotos/skip.png", confidence=0.7)) # clica no botao skipar
                                    sleep(2)
                                    pyautogui.click(pyautogui.locateCenterOnScreen("fotos/continuar.png", confidence=0.6))#clica continuar
                                    sleep(1)
                                    if pyautogui.locateCenterOnScreen("fotos/botrec.png", confidence=0.6):
                                        pyautogui.click(pyautogui.locateCenterOnScreen("fotos/botrec.png", confidence=0.6)) 
                                        sleep(2)
                                        pyautogui.click(pyautogui.locateCenterOnScreen("fotos/coletar.png", confidence=0.7))
                                        sleep(1)
                                        mechas += 1
                                        print(f"Mecha:{mechas}")
                                        braked = True
                                    else:
                                        pyautogui.click(pyautogui.locateCenterOnScreen("fotos/voltar.png", confidence=0.7))
                                        sleep(1)
                                        mechas += 1
                                        print(f"Mecha:{mechas}")
                                        braked = True

                            elif pyautogui.locateCenterOnScreen("fotos/b33.png", confidence=0.9):
                                pyautogui.click(pyautogui.locateCenterOnScreen("fotos/b33.png", confidence=0.9)) #escolhe a equipe
                                sleep(0.5)
                                pyautogui.click(pyautogui.locateCenterOnScreen("fotos/lutar.png", confidence=0.7)) #clica no botao lutar
                                sleep(6)
                                if pyautogui.locateCenterOnScreen("fotos/erro2.png", confidence=0.7):
                                    sleep(1)
                                    pyautogui.click(pyautogui.locateCenterOnScreen("fotos/continuar2.png", confidence=0.7)) #clica em voltar
                                    sleep(1)
                                    braked = True

                                else:
                                    pyautogui.click(pyautogui.locateCenterOnScreen("fotos/skip.png", confidence=0.7)) # clica no botao skipar
                                    sleep(2)
                                    pyautogui.click(pyautogui.locateCenterOnScreen("fotos/continuar.png", confidence=0.6))#clica continuar
                                    sleep(1)
                                    if pyautogui.locateCenterOnScreen("fotos/botrec.png", confidence=0.6):
                                        pyautogui.click(pyautogui.locateCenterOnScreen("fotos/botrec.png", confidence=0.6)) 
                                        sleep(2)
                                        pyautogui.click(pyautogui.locateCenterOnScreen("fotos/coletar.png", confidence=0.7))
                                        sleep(1)
                                        mechas += 1
                                        print(f"Mecha:{mechas}")
                                        braked = True
                                    else:
                                        pyautogui.click(pyautogui.locateCenterOnScreen("fotos/voltar.png", confidence=0.7))
                                        sleep(1)
                                        mechas += 1
                                        print(f"Mecha:{mechas}")
                                        braked = True





                    elif pyautogui.locateCenterOnScreen("fotos/grifo.png", confidence=0.7): #cinza 
                        #print("Cinza")

                        if pyautogui.locateCenterOnScreen("fotos/mecha80.png", confidence=0.7) or pyautogui.locateCenterOnScreen("fotos/mecha100.png", confidence=0.7) or pyautogui.locateCenterOnScreen("fotos/mecha120.png", confidence=0.7) or pyautogui.locateCenterOnScreen("fotos/mecha140.png", confidence=0.7) or pyautogui.locateCenterOnScreen("fotos/mecha160.png", confidence=0.7):
                            print("Mecha descartavel")
                            pyautogui.click(pyautogui.locateCenterOnScreen("fotos/voltar.png", confidence=0.7)) #clica em voltar
                            sleep(1)
                            pyautogui.click(pyautogui.locateCenterOnScreen("fotos/atualizar.png", confidence=0.7)) 
                            sleep(1)
                            

                        
                        elif pyautogui.locateCenterOnScreen("fotos/mecha180.png", confidence=0.7) or pyautogui.locateCenterOnScreen("fotos/mecha200.png", confidence=0.7) or pyautogui.locateCenterOnScreen("fotos/mecha240.png", confidence=0.7) or pyautogui.locateCenterOnScreen("fotos/mecha280.png", confidence=0.7) or pyautogui.locateCenterOnScreen("fotos/mecha315.png", confidence=0.7):
                            print("Mecha aceitavel")
                            sleep(0.5)
                            pyautogui.click(pyautogui.locateCenterOnScreen("fotos/atqgratis.png", confidence=0.6))
                            sleep(0.5)
                            pyautogui.click(pyautogui.locateCenterOnScreen("fotos/equipe.png", confidence=0.7))
                            sleep(0.5)
                            if pyautogui.locateCenterOnScreen("fotos/b3.png", confidence=0.9):
                                pyautogui.click(pyautogui.locateCenterOnScreen("fotos/b3.png", confidence=0.9)) #escolhe a equipe
                                sleep(0.5)
                                pyautogui.click(pyautogui.locateCenterOnScreen("fotos/lutar.png", confidence=0.7)) #clica no botao lutar
                                sleep(6)
                                if pyautogui.locateCenterOnScreen("fotos/erro2.png", confidence=0.7):
                                    sleep(1)
                                    pyautogui.click(pyautogui.locateCenterOnScreen("fotos/continuar2.png", confidence=0.7)) #clica em voltar
                                    sleep(1)
                                    braked = True

                                else:
                                    pyautogui.click(pyautogui.locateCenterOnScreen("fotos/skip.png", confidence=0.7)) # clica no botao skipar
                                    sleep(2)
                                    pyautogui.click(pyautogui.locateCenterOnScreen("fotos/continuar.png", confidence=0.6))#clica continuar
                                    sleep(1)
                                    if pyautogui.locateCenterOnScreen("fotos/botrec.png", confidence=0.6):
                                        pyautogui.click(pyautogui.locateCenterOnScreen("fotos/botrec.png", confidence=0.6)) 
                                        sleep(2)
                                        pyautogui.click(pyautogui.locateCenterOnScreen("fotos/coletar.png", confidence=0.7))
                                        sleep(1)
                                        mechas += 1
                                        print(f"Mecha:{mechas}")
                                        braked = True
                                    else:
                                        pyautogui.click(pyautogui.locateCenterOnScreen("fotos/voltar.png", confidence=0.7))
                                        sleep(1)
                                        mechas += 1
                                        print(f"Mecha:{mechas}")
                                        braked = True

                            elif pyautogui.locateCenterOnScreen("fotos/b33.png", confidence=0.9):
                                pyautogui.click(pyautogui.locateCenterOnScreen("fotos/b33.png", confidence=0.9)) #escolhe a equipe
                                sleep(0.5)
                                pyautogui.click(pyautogui.locateCenterOnScreen("fotos/lutar.png", confidence=0.7)) #clica no botao lutar
                                sleep(6)
                                if pyautogui.locateCenterOnScreen("fotos/erro2.png", confidence=0.7):
                                    sleep(1)
                                    pyautogui.click(pyautogui.locateCenterOnScreen("fotos/continuar2.png", confidence=0.7)) #clica em voltar
                                    sleep(1)
                                    braked = True

                                else:
                                    pyautogui.click(pyautogui.locateCenterOnScreen("fotos/skip.png", confidence=0.7)) # clica no botao skipar
                                    sleep(2)
                                    pyautogui.click(pyautogui.locateCenterOnScreen("fotos/continuar.png", confidence=0.6))#clica continuar
                                    sleep(1)
                                    if pyautogui.locateCenterOnScreen("fotos/botrec.png", confidence=0.6):
                                        pyautogui.click(pyautogui.locateCenterOnScreen("fotos/botrec.png", confidence=0.6)) 
                                        sleep(2)
                                        pyautogui.click(pyautogui.locateCenterOnScreen("fotos/coletar.png", confidence=0.7))
                                        sleep(1)
                                        mechas += 1
                                        print(f"Mecha:{mechas}")
                                        braked = True
                                    else:
                                        pyautogui.click(pyautogui.locateCenterOnScreen("fotos/voltar.png", confidence=0.7))
                                        sleep(1)
                                        mechas += 1
                                        print(f"Mecha:{mechas}")
                                        braked = True


            elif pyautogui.locateCenterOnScreen("fotos/erro3.png", confidence=0.7) or pyautogui.locateCenterOnScreen("fotos/erro4.png", confidence=0.7) or pyautogui.locateCenterOnScreen("fotos/erro5.png", confidence=0.7):
                print("erro 3,4,5")
                sleep(1)
                pyautogui.click(pyautogui.locateCenterOnScreen("fotos/voltar.png", confidence=0.7))
                sleep(1)
                braked = True


            elif pyautogui.locateCenterOnScreen("fotos/erro6.png", confidence=0.7):
                print("erro 6")
                sleep(2)
                pyautogui.click(pyautogui.locateCenterOnScreen("fotos/evento2.png", confidence=0.7)) 
                sleep(2)
                pyautogui.click(pyautogui.locateCenterOnScreen("fotos/evento1.png", confidence=0.7)) 
                sleep(2)
                pyautogui.click(pyautogui.locateCenterOnScreen("fotos/evento.png", confidence=0.7))
                sleep(2)
                braked = True

            elif pyautogui.locateCenterOnScreen("fotos/clubeinicial.png", confidence=0.8):
                print("tela inicial")
                sleep(1)
                pyautogui.click(pyautogui.locateCenterOnScreen("fotos/clubeinicial.png", confidence=0.7)) 
                sleep(1)
                pyautogui.click(pyautogui.locateCenterOnScreen("fotos/evento2.png", confidence=0.7)) 
                sleep(1)

                braked = True
            elif pyautogui.locateCenterOnScreen("fotos/locais.png", confidence=0.8):
                print("mechas locais")
                sleep(2)
                pyautogui.click(pyautogui.locateCenterOnScreen("fotos/mechachefe.png", confidence=0.8)) 
                sleep(2)

            elif pyautogui.locateCenterOnScreen("fotos/reconectar.png", confidence=0.7):
                print("reconectando")
                sleep(1)
                pyautogui.click(pyautogui.locateCenterOnScreen("fotos/reconectar.png", confidence=0.7)) 
                sleep(1)

            elif pyautogui.locateCenterOnScreen("fotos/botrec.png", confidence=0.6):
                print("recompensa bugada")
                sleep(1)
                pyautogui.click(pyautogui.locateCenterOnScreen("fotos/botrec.png", confidence=0.6)) 
                sleep(1)

            elif pyautogui.locateCenterOnScreen("fotos/erro7.png", confidence=0.7):
                print("reconectando")
                sleep(1)
                pyautogui.click(pyautogui.locateCenterOnScreen("fotos/erro7.png", confidence=0.7)) 
                sleep(1)

            elif pyautogui.locateCenterOnScreen("fotos/mechalocal.png", confidence=0.7):
                print("mecha local")
                sleep(1)
                pyautogui.click(pyautogui.locateCenterOnScreen("fotos/mechachefe.png", confidence=0.7)) 
                sleep(1)






        self.parar_automacao()



    def fechar_janela(self):
        self.parar_automacao()
        self.root.destroy()

    def write(self, text):
        if text != '\n':
            current_time = datetime.now().strftime("%H:%M:%S")
            formatted_text = f"[{current_time}]{text}"
            self.txt_output.insert(tk.END, formatted_text)
        else:
            self.txt_output.insert(tk.END, text)

        self.txt_output.see(tk.END)




if __name__ == "__main__":
    root = tk.Tk()
    app = AutomacaoGUI(root)
    root.protocol("WM_DELETE_WINDOW", app.fechar_janela)
    root.mainloop()
