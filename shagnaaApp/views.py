from django.shortcuts import render, redirect
import sqlite3 as sql
from django.contrib import messages

def handle_upload(a_img, name):
    if a_img:
        with open(name, 'wb+') as destination:
            for chunk in a_img.chunks():
                destination.write(chunk)

def achaa(request):
    context = {}
    con = sql.connect('db.sqlite3')
    cur = con.cursor()
    cur.execute("SELECT a_title,a_price,a_desc,a_img FROM 'achaa_zar'")
    xp = cur.fetchall()
    if xp:
        context['data'] = xp
        print(context)
    return render(request, 'user/achaa.html',context=context)

def uindex(request):
    return render(request, 'user/index.html')
def a_index(request):
    return render(request, 'admin/index.html')
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
                return render(request, 'admin/index.html')
            if x > 0:
                return render(request, 'user/index.html')
    
    return render(request, 'login.html')