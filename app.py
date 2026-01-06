from flask import Flask, render_template, request, redirect, url_for
from database import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:copac123@localhost/Spital'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

from models import Pacient, Medicament, Reteta

@app.route('/pacienti')
def list_pacienti():
    pacienti = Pacient.query.all()
    return render_template('pacienti.html', pacienti=pacienti)

@app.route('/pacienti/add', methods=['GET', 'POST'])
def add_pacient():
    if request.method == 'POST':
        nume = request.form['nume']
        prenume = request.form['prenume']
        data_nasterii = request.form['data_nasterii']
        new_pacient = Pacient(nume=nume, prenume=prenume, data_nasterii=data_nasterii)
        db.session.add(new_pacient)
        db.session.commit()
        return redirect(url_for('list_pacienti'))
    return render_template('add_pacient.html')

@app.route('/pacienti/delete/<int:id_pacient>', methods=['POST'])
def delete_pacient(id_pacient):
    pacient = Pacient.query.get_or_404(id_pacient)
    db.session.delete(pacient)
    db.session.commit()
    return redirect(url_for('list_pacienti'))

@app.route('/pacienti/edit/<int:id_pacient>', methods=['GET', 'POST'])
def edit_pacient(id_pacient):
    pacient = Pacient.query.get_or_404(id_pacient)
    if request.method == 'POST':
        pacient.nume = request.form['nume']
        pacient.prenume = request.form['prenume']
        pacient.data_nasterii = request.form['data_nasterii']
        db.session.commit()
        return redirect(url_for('list_pacienti'))
    return render_template('edit_pacient.html', pacient=pacient)

@app.route('/medicamente')
def list_medicamente():
    medicamente = Medicament.query.all()
    return render_template('medicamente.html', medicamente=medicamente)

@app.route('/medicamente/add', methods=['GET', 'POST'])
def add_medicament():
    if request.method == 'POST':
        denumire = request.form['denumire']
        producator = request.form['producator']
        new_medicament = Medicament(denumire=denumire, producator=producator)
        db.session.add(new_medicament)
        db.session.commit()
        return redirect(url_for('list_medicamente'))
    return render_template('add_medicament.html')

@app.route('/medicamente/delete/<int:id_medicament>', methods=['POST'])
def delete_medicament(id_medicament):
    medicament = Medicament.query.get_or_404(id_medicament)
    db.session.delete(medicament)
    db.session.commit()
    return redirect(url_for('list_medicamente'))

@app.route('/medicamente/edit/<int:id_medicament>', methods=['GET', 'POST'])
def edit_medicament(id_medicament):
    medicament = Medicament.query.get_or_404(id_medicament)
    if request.method == 'POST':
        medicament.denumire = request.form['denumire']
        medicament.producator = request.form['producator']
        db.session.commit()
        return redirect(url_for('list_medicamente'))
    return render_template('edit_medicament.html', medicament=medicament)

@app.route('/retete')
def list_retete():
    retete = Reteta.query.all()
    return render_template('retete.html', retete=retete)

@app.route('/retete/add', methods=['GET', 'POST'])
def add_reteta():
    if request.method == 'POST':
        id_pacient = request.form['id_pacient']
        id_medicament = request.form['id_medicament']
        data_start = request.form['data_start']
        doza = request.form['doza']
        new_reteta = Reteta(id_pacient=id_pacient, id_medicament=id_medicament, data_start=data_start, doza=doza)
        db.session.add(new_reteta)
        db.session.commit()
        return redirect(url_for('list_retete'))
    pacienti = Pacient.query.all()
    medicamente = Medicament.query.all()
    return render_template('add_reteta.html', pacienti=pacienti, medicamente=medicamente)    

@app.route('/retete/delete/<int:id_pacient>/<int:id_medicament>', methods=['POST'])
def delete_reteta(id_pacient, id_medicament):
    reteta = Reteta.query.get_or_404((id_pacient, id_medicament))
    db.session.delete(reteta)
    db.session.commit()
    return redirect(url_for('list_retete'))

@app.route('/retete/edit/<int:id_pacient>/<int:id_medicament>', methods=['GET', 'POST'])
def edit_reteta(id_pacient, id_medicament):
    reteta = Reteta.query.get_or_404((id_pacient, id_medicament))
    if request.method == 'POST':
        reteta.data_start = request.form['data_start']
        reteta.doza = request.form['doza']
        db.session.commit()
        return redirect(url_for('list_retete'))
    return render_template('edit_reteta.html', reteta=reteta)


@app.route('/index')
def index():
    """Serve the index page with links to main sections."""
    return render_template('index.html')


@app.route('/')
def root():
    """Redirect root URL to the index page."""
    return redirect(url_for('index'))


if __name__ == '__main__':
    print(app.url_map)
    app.run(debug=True)
    