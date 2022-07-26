from flask import Flask, render_template #importar biblioteca do flask e chamar a Classe Fask e a função render template que é do Flask

app=Flask("hello") #nome da aplicação

@app.route("/") #raiz da aplicação 
@app.route("/hello") #cria as paginas
def hello():
    return "Hello Word"

@app.route("/meucontato") #cria a pagina meu contato
def meuContato():
    return render_template('index.html')
