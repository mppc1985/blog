from flask import Flask, render_template #importar biblioteca do flask e chamar a Classe Fask e a função render template que é do Flask
from datetime import datetime   

app=Flask("hello") #nome da aplicação

#lista > dicionario
posts= [ #mock = substituto, simulacao
    { #isso é um post
        "title": "O meu primeiro post",
        "body": "Aqui é o texto do Post",
        "author": "Marcos",
        "created": datetime(2022,7,25)
    },
        { #isso é um post
        "title": "O meu segundo post",
        "body": "Aqui é o texto do Post",
        "author": "danilo",
        "created": datetime(2022,7,26)
    },

]


@app.route("/") #raiz da aplicação 
def index():
    return render_template("index.html", posts=posts)

