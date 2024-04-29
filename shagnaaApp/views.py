from django.shortcuts import render, redirect
import sqlite3 as sql
from django.contrib import messages

def handle_upload(a_img, name):
    if a_img:
        with open(name, 'wb+') as destination:
            for chunk in a_img.chunks():
                destination.write(chunk)

def handle_upload2(nimg, url):
    if nimg:
        with open(url, 'wb+') as destination:
            for chunk in nimg.chunks():
                destination.write(chunk)

def achaa(request):
    context = {}
    with sql.connect('db.sqlite3') as con:
        cur = con.cursor()
        cur.execute("SELECT a_title, a_price, a_desc, a_img FROM 'achaa_zar'")
        xp = cur.fetchall()
        if xp: 
            context['data'] = xp
            print(context)

    if request.method == 'POST':
        dname = request.POST.get('dname')
        dpass = request.POST.get('dpassport')
        dletsence = request.POST.get('dletsence')
        dimg = request.FILES.get('dimg')
        url1 = f'static/img/{dname}.jpg'
        handle_upload(dimg, url1)
        crd = request.POST.get('crd')
        ctype = request.POST.get('ctype')
        cedangi = request.POST.get('cedangi')
        cmadename = request.POST.get('cmadename')
        ccefno = request.POST.get('ccefno')
        cimg = request.FILES.get('cimg')
        url2 = f'static/img/{crd}.jpg'
        handle_upload2(cimg, url2)


        with sql.connect('db.sqlite3') as con:
            cur = con.cursor()
            cur.execute("INSERT INTO 'user_request' (dname, dpass, dletsence, url1, crd, ctype, cedangi, cmadename, ccefno, url2) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (dname, dpass, dletsence, url1, crd, ctype, cedangi, cmadename, ccefno, url2))
            con.commit()

    return render(request, 'user/achaa.html', context=context)


def uindex(request):
    context = {}
    con = sql.connect('db.sqlite3')
    cur = con.cursor()
    cur.execute("SELECT * FROM 'news' ")
    xp = cur.fetchall()
    context['data'] = xp[:3]
    return render(request, 'user/index.html',context=context)

def news(request):
    context = {}
    if request.method == 'POST':
        if 'delete' in request.POST:
            delete_id = request.POST.get('news_id')
            con = sql.connect('db.sqlite3')
            cur = con.cursor()
            cur.execute("DELETE FROM news WHERE nname=?", (delete_id,))
            con.commit()
            con.close()
            return redirect('news')
        else:
            nname = request.POST.get('nname')
            ndesc = request.POST.get('ndesc')
            nimg = request.FILES.get('nimg')
            url = f'static/img/{nname}.jpg'  
            handle_upload2(nimg, url)
            con = sql.connect('db.sqlite3')
            cur = con.cursor()
            cur.execute("INSERT INTO 'news' (nname,ndesc,nimg) VALUES(?,?,?)", (nname,ndesc,url))
            con.commit()
            con.close()
            return redirect('news')
    con = sql.connect('db.sqlite3')
    cur = con.cursor()
    cur.execute("SELECT nname,ndesc,nimg FROM news")
    context['data'] = cur.fetchall()
    return render(request, 'admin/news.html', context=context)

def u_news(request):
    context = {}
    con = sql.connect('db.sqlite3')
    cur = con.cursor()
    cur.execute("SELECT * FROM news")
    context['data']=cur.fetchall()
    return render(request, 'user/news.html', context=context)


def a_index(request):
    context = {}
    con = sql.connect('db.sqlite3')
    cur = con.cursor()
    curs = con.cursor()
    cur.execute("SELECT count(request_id) FROM user_request")
    curs.execute("SELECT * FROM user_request")
    xp = cur.fetchone()
    hp = curs.fetchall()
    print(hp)
    context['id_num'] = xp[0]
    context['data'] = hp
    return render(request, 'admin/index.html',context=context)

def a_achaa(request):
    context = {}
    if request.method == 'POST':
        if 'delete' in request.POST:
            delete_id = request.POST.get('delete_id')
            con = sql.connect('db.sqlite3')
            cur = con.cursor()
            cur.execute("DELETE FROM achaa_zar WHERE a_title=?", (delete_id,))
            con.commit()
            con.close()
            return redirect('a_achaa')
        else:
            a_title = request.POST.get('a_title')
            a_price = request.POST.get('a_price')
            a_desc = request.POST.get('a_desc')
            a_img = request.FILES.get('filename')
            url = f'static/img/{a_title}.jpg'  
            handle_upload(a_img, url)
            con = sql.connect('db.sqlite3')
            cur = con.cursor()
            cur.execute("INSERT INTO achaa_zar (a_title, a_price, a_desc, a_img) VALUES (?, ?, ?, ?)", (a_title, a_price, a_desc, url))
            con.commit()
            con.close()
            return redirect('a_achaa')
    else:
        con = sql.connect('db.sqlite3')
        cur = con.cursor()
        cur.execute("SELECT a_title,a_price,a_desc,a_img FROM achaa_zar")
        xp = cur.fetchall()
        context['data'] = xp
        con.close()

    return render(request, 'admin/achaa.html', context=context)

def login(request):    
    if request.method == 'POST':
        if request.POST.get('umail'):
            uname = request.POST['uname']
            umail = request.POST['umail']
            upass = request.POST['upass']
            urpass = request.POST['urpass']
            utype = request.POST['utype']
            if upass == urpass:
                con = sql.connect('db.sqlite3')
                cur = con.cursor()
                cur.execute("INSERT INTO 'user' (uname, umail, upass, utype) VALUES (?, ?, ?, ?)", ( uname, umail, upass, utype))
                con.commit()
                con.close()
            else:
                messages.success(request, 'Нууц үг таарахгүй байна.')
        elif request.POST['lmail']:
            lmail = request.POST['lmail']
            lpass = request.POST['lpass']
            con = sql.connect('db.sqlite3')
            cur = con.cursor()
            cur.execute("SELECT count(umail) FROM 'user' WHERE umail=? AND upass=?",(lmail, lpass))
            x = cur.fetchone()
            x = list(x)
            x = x[0]

            if lpass == 'admin123':
                return redirect('a_index')
            if x > 0:
                return redirect('uindex')
    
    return render(request, 'login.html')