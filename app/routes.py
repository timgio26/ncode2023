from flask import render_template,redirect, url_for,request,send_file,session
from app import app,db#,api
from app.models import userName
import pandas as pd,json,datetime


@app.route('/')
def index():
    return render_template('home.html')

@app.route('/daftar', methods=['GET', 'POST'])
def daftar():
    session.pop('user', None)
    # session.pop('username', None)
    session.pop('uid', None)
    if request.method=='POST':
        usercek=userName.query.filter_by(username=request.form['quname']).first()
        if usercek is None:
            newuser=userName(nama=request.form['qnama'],username=request.form['quname'],password=request.form['qpass'])
            db.session.add(newuser)
            db.session.commit()
            return redirect(url_for('index'))
        else:
            return redirect(url_for('daftar'))
    return render_template('daftar.html')

@app.route('/masuk', methods=['GET', 'POST'])
def masuk():
    session.pop('user', None)
    # session.pop('username', None)
    session.pop('uid', None)
    if request.method == 'POST':
        usercek=userName.query.filter_by(username=request.form['quname']).first()
        if usercek is None or usercek.password!=request.form['qpass']:
            msg='Username / Password salah'
            return render_template('masuk.html',msg=msg)
        else:
            session['user']=request.form['quname']
            # session['username']=usercek.first_name
            session['uid']=usercek.id
            return redirect(url_for('main'))
    return render_template('masuk.html')

@app.route('/keluar')
def keluar():
    session.pop('user', None)
    # session.pop('username', None)
    session.pop('uid', None)
    return redirect(url_for('index'))

@app.route('/main', methods=['GET', 'POST'])
def main():
    if session.get('uid',None):
        msg=None
        dbkode=pd.read_excel("app/static/dbkode.xlsx",engine='openpyxl')
        user=userName.query.get(session.get('uid',None))
        if user.bingodate:
            msg="BINGO"
        if request.method == 'POST':
            # print(dbkode[dbkode['kode']==request.form['kode']]['koordinat'])
            koordinat=dbkode[dbkode['kode']==request.form['kode']]['koordinat']#[0]
            if len(koordinat)!=0:
                if user.kode:
                    vou = json.loads(user.kode.replace("'",'"'))
                    if koordinat.values[0] in vou:
                        return redirect(url_for('main'))
                    else:
                        vou.append(koordinat.values[0])
                        test=['A','B','C','D','E','1','2','3','4','5']
                        for i in test:
                            hasil=[a for a in vou if i in a]
                            if len(hasil)==5:
                                
                                # print(hasil)
                                # print(user.bingodate is None)
                                if user.bingodate is None:
                                    user.bingodate=str(datetime.datetime.now())
                        user.kode=str(vou)
                        print(vou)

                        db.session.add(user)
                        db.session.commit()
                        return redirect(url_for('main'))
                else:
                    addcoor=str([koordinat.values[0]])
                    user.kode=addcoor
                    db.session.add(user)
                    db.session.commit()
                    return redirect(url_for('main'))
            else:
                return redirect(url_for('main'))
        else:
            return render_template('main.html',kode=user.kode,msg=msg)
    else:
        return redirect(url_for('masuk'))
    

@app.route('/dbpemain')
def dbpemain():
    df=userName.query.all()
    return render_template('dbpemain.html',df=df)

@app.route('/deldbpemain/<id>')
def deldbpemain(id):
    itemdel=userName.query.get(id)
    db.session.delete(itemdel)
    db.session.commit()
    return redirect(url_for('dbpemain'))