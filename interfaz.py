from tkinter import *
import webcam
import os

root = Tk()
root.geometry("450x150")
root.title("Detección EPP")


def inferir():
    Label(text="Por favor esperar unos segundos mientras se inicializa el programa.").place(
        x=40, y=115
    )
    webcam.runInference()


btnInferencia = Button(root, text="Detectar", command=inferir).place(x=200, y=80)


def linuxWrite():
    # solo funciona si se tiene bash o zsh, si se desea extender, solo hay que poner el path en el diccionario
    toWrite = 'export UBICACION="' + str(ubicacion.get() + '"')
    shells = {"bash": "~/.bashrc", "zsh": "~/.zshrc"}
    current_shell = os.environ["SHELL"].split("/")[
        -1
    ]  # toma el "bash" de /bin/bash, o el "zsh" de /bin/zsh
    if any(shell in current_shell for shell in list(shells.keys())):
        with open(os.path.expanduser(shells[current_shell]), "r") as outfile:
            lines = outfile.readlines()
        with open(os.path.expanduser(shells[current_shell]), "a") as outfile:
            import re

            for line in lines:
                if not re.match('^export UBICACION="?\S+"?', line):
                    outfile.write(line)
            outfile.write(toWrite)
            outfile.close()


def windowsWrite():
    import subprocess

    subprocess.call(["setx", "UBICACION", str(ubicacion.get())], shell=True)


def guardarUbicacion():
    import platform

    if platform.system() == "Linux":
        linuxWrite()
    else:
        if platform.system() == "Windows":
            windowsWrite()
    labelUbicacion.place_forget()
    textUbicacion.place_forget()
    btnGuardarUbicacion.place_forget()
    btnNuevaUbicacion.place(x=150, y=13)


labelUbicacion = Label(root, text="Ingrese la ubicación del dispositivo: ")
ubicacion = StringVar()
textUbicacion = Entry(root, textvariable=ubicacion)
btnGuardarUbicacion = Button(root, text="Guardar", command=guardarUbicacion)


def nuevaUbicacion():
    global labelUbicacion, textUbicacion, btnGuardarUbicacion, btnNuevaUbicacion, root
    btnNuevaUbicacion.place_forget()
    labelUbicacion.place(x=10, y=15)
    textUbicacion.place(x=205, y=15)
    btnGuardarUbicacion.place(x=340, y=13)


btnNuevaUbicacion = Button(root, text="Cambiar ubicación del dispositivo", command=nuevaUbicacion)

# Cerifica que la variable de entorno "UBICACION" no exista, en caso de no existir se crea.
if os.getenv("UBICACION") == None:
    labelUbicacion.place(x=10, y=15)
    textUbicacion.place(x=205, y=15)
    btnGuardarUbicacion.place(x=340, y=13)
else:
    btnNuevaUbicacion.place(x=150, y=13)

root.mainloop()
