from flask import Flask, render_template, request, redirect, session
import pymongo

app = Flask("Trendsphere")
app.secret_key="key"
mongo = pymongo.MongoClient ("mongodb+srv://julia:atelier1234@cluster0.s5pvj.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db_utilisateurs = mongo.bdd.Users
mon_utilisateur = db_utilisateurs.find_one({"name" : "Bob"})
print(mon_utilisateur)

# route d'administration pour les persos
@app.route("/admin/personnages")
def perso():
    db_post = mongo.bdd.annonces 
    mes_posts = db_post.find({})
    return render_template("admin/personnages.html" ,
                       mes_posts = list(mes_posts))


@app.route("/supprimerposts/<titre>")
def supprimerposts(titre) :
    db_post = mongo.bdd.annonces
    db_post.delete_one({"titre" : titre })
    return redirect("/admin/personnages")


# Exemple de requête "find" --> récupérer PLUSIEURS entrées
@app.route("/find")
def find():
    db_utilisateurs = mongo.bdd.Users
    resultat = db_utilisateurs.find({})
    return render_template("testrequete.html", resultat = list(resultat))

# Exemple de requête "find_one" --> récupérer UNE entrée
@app.route("/findone")
def findone():
    db_utilisateurs = mongo.bdd.Users
    resultat = db_utilisateurs.find_one({"name" : "toto"})
    return render_template("testrequete.html", resultat = resultat)

# Exemple de requête "delete_one" --> supprimer UNE entrée
@app.route("/deleteone")
def deleteoone():
    db_utilisateurs = mongo.db.utilisateurs
    resultat = db_utilisateurs.delete_one({"pseudo" : "toto"})
    return render_template("testrequete.html", resultat = resultat)

# Exemple de requête "insert_one" --> insérer UNE entrée
@app.route("/insertone")
def insertone():
    db_utilisateurs = mongo.db.utilisateurs
    resultat = db_utilisateurs.insert_one({
        "pseudo" : "toto",
        "mdp" : "1234",
        "avatar" : "",
        "age" : "",
        "nationalite" : "inconnu"
        })
    return render_template("testrequete.html", resultat = resultat)


# Exemple de requête "update_one" --> mettre à jour UNE entrée
@app.route("/updateone")
def updateone():
    db_utilisateurs = mongo.db.utilisateurs
    resultat = db_utilisateurs.update_one(
        {"pseudo" : "toto"},
        {"$set" : {"mdp" : "6789", "age" : 23}}
    )
    return render_template("testrequete.html", resultat = resultat)


# Route d'accueil
@app.route("/")
def accueil() :
    # On récupère toutes les annonces
    mes_annonces = mongo.bdd.annonces
    annonces = mes_annonces.find({})
    if "utilisateur" in session :
        # Si l'utilisateur est connecté, on affiche la page en précisant l'utilisateur
        mes_utilisateurs = mongo.bdd.Users
        utilisateur = mes_utilisateurs.find_one({"name" : session["utilisateur"]})
        return render_template("index.html",
                               utilisateur = utilisateur,
                               annonces = annonces)
    else :
        # Si l'utilisateur n'est pas connecté, on affiche simplement la page
        return render_template("index.html",
                               annonces = annonces)


# Route login / Se connecter
@app.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "GET" :
        return render_template("login.html")
    else :
        # On récupère le pseudo et mot de passe entrés dans les boîtes (inputs)
        pseudo_entre = request.form["input_pseudo"]
        mdp_entre = request.form["input_mdp"]
        # On récupère l'utilisateur
        mes_utilisateurs = mongo.bdd.Users
        utilisateur = mes_utilisateurs.find_one({"name" : pseudo_entre})
        print(utilisateur)
        # Si l'utilisateur n'existe pas :
        if not utilisateur :
            return render_template("login.html", erreur = "L'utilisateur n'existe pas")
        # Sinon, si le mot de passe est incorrect :
        elif mdp_entre != utilisateur["password"] :
            return render_template("login.html", erreur = "Le mot de passe est incorrect")
        # Sinon, c'est que tout est bon :
        else :
            # On connecte l'utilisateur et on redirige vers la page d'accueil
            session["utilisateur"] = pseudo_entre
            print("L'utilisateur est connecte")
            return redirect("/")

# Route logout / se déconnecter
@app.route("/logout")
def logout() :
    session.clear()
    return redirect("/")



@app.route("/register2", methods=["GET", "POST"])
def register2():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        msg = 'You have successfully registered!'
    return render_template("register.html", msg=msg)



# Route register / S'enregistrer
@app.route("/register", methods = ["GET", "POST"])
def register() :
    if request.method == "GET" :
        return render_template("register.html")
    else :
        # 1 : on récupère les informations entrées dans les boîtes (inputs)
        pseudo_entre = request.form["input_pseudo"]
        mdp_entre = request.form["input_mdp"]
        avatar_entre = request.form["input_avatar"]
        if avatar_entre == "" :
            avatar_entre = "https://sbcf.fr/wp-content/uploads/2018/03/sbcf-default-avatar.png"
        # 2 : on gère tous les cas d'erreur
        mes_utilisateurs = mongo.bdd.Users
        utilisateur = mes_utilisateurs.find_one({"name" : pseudo_entre})
        # si le pseudo existe déjà
        if utilisateur :
            return render_template("register.html", erreur = "L'utilisateur existe déjà")
        # si aucun pseudo n'a été rentré    
        elif pseudo_entre == "" :
            return render_template("register.html", erreur = "Veuillez rentrer un pseudo")
        # si le mot de passe ne fait pas assez de caractères
        elif len(mdp_entre) < 4 :
            return render_template("register.html", erreur = "Le mot de passe doit faire au moins 4 caractères")
        else :
            # 3 : on crée le compte utilisateur
            mes_utilisateurs.insert_one({
                "name" : pseudo_entre,
                "password" : mdp_entre,
                "avatar" : avatar_entre,
                "age" : 0,
                "nationality" : "non précisée"
            })
            # on connecte l'utilisateur via le cookie
            session["utilisateur"] = pseudo_entre
            # on redirige vers la page d'accueil
            return redirect("/")



# Lance l'application
if __name__ == "__main__":
    app.run("0.0.0.0", port=3904)



    # Route d'accueil
@app.route("/")
def accueil() :
    # On récupère toutes les annonces
    mes_annonces = mongo.bdd.annonces
    annonces = mes_annonces.find({})
    if "utilisateur" in session :
        # Si l'utilisateur est connecté, on affiche la page en précisant l'utilisateur
        mes_utilisateurs = mongo.bdd.utilisateurs
        utilisateur = mes_utilisateurs.find_one({"pseudo" : session["utilisateur"]})
        return render_template("index.html",
                               utilisateur = utilisateur,
                               annonces = annonces)


                               # Route logout / se déconnecter
@app.route("/logout")
def logout() :
    session.clear()
    return redirect("/")


    # Route register / S'enregistrer
@app.route("/register", methods = ["GET", "POST"])
def register() :
    if request.method == "GET" :
        return render_template("register.html")
    else :
        # 1 : on récupère les informations entrées dans les boîtes (inputs)
        pseudo_entre = request.form["input_pseudo"]
        mdp_entre = request.form["input_mdp"]
        avatar_entre = request.form["input_avatar"]
        if avatar_entre == "" :
            avatar_entre = "https://sbcf.fr/wp-content/uploads/2018/03/sbcf-default-avatar.png"
        # 2 : on gère tous les cas d'erreur
        mes_utilisateurs = mongo.bdd.utilisateurs
        utilisateur = mes_utilisateurs.find_one({"pseudo" : pseudo_entre})
        # si le pseudo existe déjà
        if utilisateur :
            return render_template("register.html", erreur = "L'utilisateur existe déjà")
        # si aucun pseudo n'a été rentré    
        elif pseudo_entre == "" :
            return render_template("register.html", erreur = "Veuillez rentrer un pseudo")
        # si le mot de passe ne fait pas assez de caractères
        elif len(mdp_entre) < 4 :
            return render_template("register.html", erreur = "Le mot de passe doit faire au moins 4 caractères")
        else :
            # 3 : on crée le compte utilisateur
            mes_utilisateurs.insert_one({
                "pseudo" : pseudo_entre,
                "mdp" : mdp_entre,
                "avatar" : avatar_entre,
                "age" : 0,
                "nationalite" : "non précisée"
            })
            # on connecte l'utilisateur via le cookie
            session["utilisateur"] = pseudo_entre
            # on redirige vers la page d'accueil
            return redirect("/")


            # Route login / Se connecter
@app.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "GET" :
        return render_template("login.html")
    else :
        # On récupère le pseudo et mot de passe entrés dans les boîtes (inputs)
        pseudo_entre = request.form["input_pseudo"]
        mdp_entre = request.form["input_mdp"]
        # On récupère l'utilisateur
        mes_utilisateurs = mongo.bdd.utilisateurs
        utilisateur = mes_utilisateurs.find_one({"pseudo" : pseudo_entre})
        # Si l'utilisateur n'existe pas :
        if not utilisateur :
            return render_template("login.html", erreur = "L'utilisateur n'existe pas")
        # Sinon, si le mot de passe est incorrect :
        elif mdp_entre != utilisateur["mdp"] :
            return render_template("login.html", erreur = "Le mot de passe est incorrect")
        # Sinon, c'est que tout est bon :
        else :
            # On connecte l'utilisateur et on redirige vers la page d'accueil
            session["utilisateur"] = pseudo_entre
            return redirect("/")