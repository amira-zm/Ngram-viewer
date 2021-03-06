from flask import Flask, render_template, flash, redirect, url_for, session, request, logging,url_for
import pandas as pd
import getngrams
import datetime
import collections
from similar import similarBooks
app = Flask(__name__)

# Import writer class from csv module
from csv import writer

# List




@app.route('/',methods=['GET','POST'])
def index():


    if request.method == 'POST':
        form = request.form["nom"].lower()
        corpus =request.form["pets"]
        deb=request.form["deb"]
        end=request.form["fin"]

        ch1 = form + " --startYear="+deb+" --endYear=+"+end+" --corpus="+corpus
        List = [form.title(), deb,end, corpus,1]

        # Open our existing CSV file in append mode
        # Create a file object for this file
        with open('event.csv', 'a') as f_object:
            # Pass this file object to csv.writer()
            # and get a writer object
            writer_object = writer(f_object)

            # Pass the list as an argument into
            # the writerow()
            writer_object.writerow(List)

            # Close the file object
            f_object.close()

        getngrams.runQuery(ch1)


        return redirect(url_for('line2', form=form ,corpus=corpus,deb=deb,end=end))
    import cv2
    from pyzbar.pyzbar import decode
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)
    camera = True
    while camera == True:
        success, frame = cap.read()
        for code in decode(frame):
            print(code.data.decode('utf-8'))
            camera = False
        cv2.imshow('testing-code-scan', frame)
        cv2.waitKey(1)
    return render_template("home.html")

@app.route('/favorite')
def fovorite():
    events= pd.read_csv ('event.csv')

    rec = events.groupby(events.columns.tolist()).size().reset_index().rename(columns={0: 'records'})
    records = rec.sort_values(by=['records'], ascending=False)
    records = records.head(10)
    labels=list(records['ngram'])
    values=list(records['records'])
    colors = [
        "#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA",
        "#ABCDEF", "#DDDDDD", "#ABCABC", "#4169E1",
        "#C71585", "#FF4500", "#FEDCBA", "#46BFBD"]
    return render_template("favorite.html",records=records, set=zip(values, labels, colors))
@app.route('/pedictif',methods=['GET','POST'])
def predictif():
    if request.method == 'POST':
        form = request.form["nom"].lower()

        return redirect(url_for('trending_chart', form=form))


    return render_template("predictif.html")
@app.route('/trends/<string:form>')
def trending_chart(form):
    from pytrends.request import TrendReq

    pytrends = TrendReq()
    kw_list = [form]  # list of keywords to get data

    pytrends.build_payload(kw_list, cat=0, timeframe='2004-01-01 2022-03-16', geo="FR")
    data = pytrends.interest_over_time()
    data = data.reset_index()
    x=list(data["date"])
    values= list(data[form])
    labels=[]
    for e in x:
        labels.append(str(e))
    max=100

    return render_template("includes/_trending_chart.html",form=form,labels=labels,values=values,max=max)


@app.route('/favorite1')
def fovorite1():
    events= pd.read_csv ('event.csv')

    rec=events.groupby(events.columns.tolist()).size().reset_index().rename(columns={0: 'records'})
    records = rec.sort_values(by=['records'], ascending=False)
    records = records.head(10)
    records.to_csv("ev.csv")
    labels=list(records['ngram'])
    values=list(records['records'])
    colors = [
        "#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA",
        "#ABCDEF", "#DDDDDD", "#ABCABC", "#4169E1",
        "#C71585", "#FF4500", "#FEDCBA", "#46BFBD"]
    return render_template("_chart.html",records=records, set=zip(values, labels, colors))




@app.route('/line/<string:form>/<string:corpus>/<string:deb>/<string:end>')


def line2(form,corpus,deb,end):
    isbn = ''
    list_date = []
    poster_path = "https://image.tmdb.org/t/p/original/"
    date = "1800-01-15"
    desc = ''
    author = ''
    img = ''
    genre = ''
    d = dict()
    dic = {}
    overview = []
    di = []
    imdb = []
    ch = form.replace(" ", "") + "-" + corpus + "-" + deb + "-" + end + "-3-caseSensitive.csv"
    fin = open(ch, 'r')
    ngrams = fin.readline().strip().split(',')[1:]

    data_vals = [[] for ngram in ngrams]
    years = []
    for line in fin:
        sp = line.strip().split(',')
        years.append(int(sp[0]))
        for i, s in enumerate(sp[1:]):
            data_vals[i].append(float(s) * 100)  # Make percentage
    fin.close()

    values = []
    labels = []
    for i in range(0, len(data_vals[i])):
        values.append(years[i])
        labels.append(data_vals[0][i])

    max_value = None

    for num in labels:
        if (max_value is None or num > max_value):
            max_value = num

    df = pd.read_csv("final.csv")
    ind = 0
    for i in range(len(df)):
        chaine = df.iloc[i, 1][4:]
        d1 = dict()

        if (form.title() == chaine.title()):
            print(form.title(), chaine.title())
            date = df.iloc[i, 2][4:]
            print(date)

            datem = datetime.datetime.strptime(date, "%Y-%m-%d")
            try:
                x = int(values.index(datem.year))
            except:
                x = 0
            print(datem.year, '++++++++++', deb, '+++++++++++', end)
            if (int(datem.year) <= int(end) and int(datem.year) >= int(deb)):
                list_date.append(x)
                print(list_date)
                imdb.append(df.iloc[i, 16][4:])
                di.append(date)
                overview.append(df.iloc[i, 18][4:])
            print("liiiiiiiiiiiiiiiiiiiiiiiiiiiiiiste", di)
            print("liiiiiiiiiiiiiiiiiiiiiiiiiiiiiiste", list_date)

            desc = (df.iloc[i, 14][4:])
            img = str((df.iloc[i, 15][4:]))
            author = (df.iloc[i, 9][4:])
            genre = (df.iloc[i, 11][4:])
            isbn = (df.iloc[i, 10][4:])
            d1["isbn"] = isbn
            d1["img"] = img
            d1["genre"] = genre
            d1["author"] = author
            d1["desc"] = desc
            d[ind] = d1
            ind += 1

    for i in range(len(labels)):
        labels[i] = (labels[i] * 100) / max_value
    resultantList = []

    for i in range(len(list_date)):
        dicttt = {}
        if list_date[i] not in resultantList:
            resultantList.append(list_date[i])

            dicttt["imdb"] = imdb[i]
            dicttt["overview"] = overview[i]
            dicttt["date"] = di[i]
            dicttt["x"] = list_date[i]
            dic[list_date[i]] = dicttt

    od = collections.OrderedDict(sorted(dic.items()))
    shape = len(d)
    resultantList.sort()
    print(resultantList)
    shape1 = len(labels)

    try:
        similar_books = similarBooks(form.title())
    except:
        similar_books = {}
    fff=len(similar_books)

    return render_template('line_chart2.html',fff=fff,similar_books=similar_books,shape1=shape1, title='Sharbooks Ngram',shape=shape, d=d, max=max_value, labels=values, dic=od,
                           values=labels, ngrams=ngrams[0], x=id, t=resultantList, corpus=corpus, deb=deb, end=end,
                           desc=desc, img=img, author=author, genre=genre, imdb=imdb)

@app.route('/line/<string:form>/<string:corpus>/<string:deb>/<string:end>')


def line(form,corpus,deb,end):
    isbn = ''
    list_date = []
    poster_path = "https://image.tmdb.org/t/p/original/"
    date = "1800-01-15"
    desc = ''
    author = ''
    img = ''
    genre = ''
    d = dict()
    dic = {}
    overview = []
    di = []
    imdb = []
    ch = form.replace(" ", "") + "-" + corpus + "-" + deb + "-" + end + "-3-caseSensitive.csv"
    fin = open(ch, 'r')
    ngrams = fin.readline().strip().split(',')[1:]

    data_vals = [[] for ngram in ngrams]
    years = []
    for line in fin:
        sp = line.strip().split(',')
        years.append(int(sp[0]))
        for i, s in enumerate(sp[1:]):
            data_vals[i].append(float(s) * 100)  # Make percentage
    fin.close()

    values = []
    labels = []
    for i in range(0, len(data_vals[i])):
        values.append(years[i])
        labels.append(data_vals[0][i])

    max_value = None

    for num in labels:
        if (max_value is None or num > max_value):
            max_value = num

    df = pd.read_csv("final.csv")
    ind = 0
    for i in range(len(df)):
        chaine = df.iloc[i, 1][4:]
        d1 = dict()

        if (form.title() == chaine.title()):
            print(form.title(), chaine.title())
            date = df.iloc[i, 2][4:]
            print(date)

            datem = datetime.datetime.strptime(date, "%Y-%m-%d")
            try:
                x = int(values.index(datem.year))
            except:
                x = 0
            print(datem.year, '++++++++++', deb, '+++++++++++', end)
            if (int(datem.year) <= int(end) and int(datem.year) >= int(deb)):
                list_date.append(x)
                print(list_date)
                imdb.append(df.iloc[i, 16][4:])
                di.append(date)
                overview.append(df.iloc[i, 18][4:])
            print("liiiiiiiiiiiiiiiiiiiiiiiiiiiiiiste", di)
            print("liiiiiiiiiiiiiiiiiiiiiiiiiiiiiiste", list_date)

            desc = (df.iloc[i, 14][4:])
            img = (df.iloc[i, 15][4:])
            author = (df.iloc[i, 9][4:])
            genre = (df.iloc[i, 11][4:])
            isbn = (df.iloc[i, 10][4:])
            d1["isbn"] = isbn
            d1["img"] = img
            d1["genre"] = genre
            d1["author"] = author
            d1["desc"] = desc
            d[ind] = d1
            ind += 1

    for i in range(len(labels)):
        labels[i] = (labels[i] * 100) / max_value
    resultantList = []

    for i in range(len(list_date)):
        dicttt = {}
        if list_date[i] not in resultantList:
            resultantList.append(list_date[i])

            dicttt["imdb"] = imdb[i]
            dicttt["overview"] = overview[i]
            dicttt["date"] = di[i]
            dicttt["x"] = list_date[i]
            dic[list_date[i]] = dicttt

    od = collections.OrderedDict(sorted(dic.items()))
    shape = len(d)
    resultantList.sort()
    print(resultantList)
    shape1 = len(labels)

    try:
        similar_books = similarBooks(form.title())
    except:
        similar_books = {}

    fff=len(similar_books)


    return render_template('line_chart.html',fff=fff,similar_books=similar_books,shape1=shape1, shape=shape,title='Sharbooks Ngram', d=d, max=max_value, labels=values, dic=od,
                           values=labels, ngrams=ngrams[0], x=id, t=resultantList, corpus=corpus, deb=deb, end=end,
                           desc=desc, img=img, author=author, genre=genre, imdb=imdb)
@app.route('/line/<string:form>/<string:corpus>/<string:deb>/<string:end>/<string:id>')

def line1(form,corpus,deb,end,id):
    list_date = []
    poster_path = "https://image.tmdb.org/t/p/original/"
    date = "1800-01-15"
    desc = ''
    author = ''
    img = ''
    genre = ''
    d = dict()
    dic = {}
    overview = []
    di = []
    imdb = []
    ch = form.replace(" ", "") + "-" + corpus + "-" + deb + "-" + end + "-3-caseSensitive.csv"
    fin = open(ch, 'r')
    ngrams = fin.readline().strip().split(',')[1:]

    data_vals = [[] for ngram in ngrams]
    years = []
    for line in fin:
        sp = line.strip().split(',')
        years.append(int(sp[0]))
        for i, s in enumerate(sp[1:]):
            data_vals[i].append(float(s) * 100)  # Make percentage
    fin.close()

    values = []
    labels = []
    for i in range(0, len(data_vals[i])):
        values.append(years[i])
        labels.append(data_vals[0][i])

    max_value = None

    for num in labels:
        if (max_value is None or num > max_value):
            max_value = num

    df = pd.read_csv("final.csv")
    ind = 0
    for i in range(len(df)):
        chaine = df.iloc[i, 1][4:]
        d1 = dict()

        if (form.title() == chaine.title()):
            print(form.title(), chaine.title())
            date = df.iloc[i, 2][4:]
            print(date)

            datem = datetime.datetime.strptime(date, "%Y-%m-%d")
            try:
                x = int(values.index(datem.year))
            except:
                x = 0
            print(datem.year, '++++++++++', deb, '+++++++++++', end)
            if (int(datem.year) <= int(end) and int(datem.year) >= int(deb)):
                list_date.append(x)
                print(list_date)
                imdb.append(df.iloc[i, 16][4:])
                di.append(date)
                overview.append(df.iloc[i, 18][4:])
            print("liiiiiiiiiiiiiiiiiiiiiiiiiiiiiiste", di)
            print("liiiiiiiiiiiiiiiiiiiiiiiiiiiiiiste", list_date)

            desc = (df.iloc[i, 14][4:])
            img = (df.iloc[i, 15][4:])
            author = (df.iloc[i, 9][4:])
            genre = (df.iloc[i, 11][4:])

            d1["img"] = img
            d1["genre"] = genre
            d1["author"] = author
            d1["desc"] = desc
            d[ind] = d1
            ind += 1

    for i in range(len(labels)):
        labels[i] = (labels[i] * 100) / max_value
    resultantList = []


    for i in range(len(list_date)):
        dicttt = {}
        if list_date[i] not in resultantList:
            resultantList.append(list_date[i])

            dicttt["imdb"] = imdb[i]
            dicttt["overview"] = overview[i]
            dicttt["date"] = di[i]
            dicttt["x"] = list_date[i]
            dic[list_date[i]] = dicttt

    od = collections.OrderedDict(sorted(dic.items()))

    resultantList.sort()
    print(resultantList)
    return render_template('line_chart1.html', title='Sharbooks Ngram', d=d, max=max_value, labels=values, dic=od,
                           values=labels, ngrams=ngrams[0], x=id, t=resultantList, corpus=corpus, deb=deb, end=end,
                           desc=desc, img=img, author=author, genre=genre, imdb=imdb)
@app.route('/line3/<string:form>/<string:corpus>/<string:deb>/<string:end>/<string:id>')

def line3(form,corpus,deb,end,id):
    list_date = []
    poster_path = "https://image.tmdb.org/t/p/original/"
    date = "1800-01-15"
    desc = ''
    author = ''
    img = ''
    genre = ''
    d = dict()
    dic = {}
    overview = []
    di = []
    imdb = []
    ch = form.replace(" ", "") + "-" + corpus + "-" + deb + "-" + end + "-3-caseSensitive.csv"
    fin = open(ch, 'r')
    ngrams = fin.readline().strip().split(',')[1:]

    data_vals = [[] for ngram in ngrams]
    years = []
    for line in fin:
        sp = line.strip().split(',')
        years.append(int(sp[0]))
        for i, s in enumerate(sp[1:]):
            data_vals[i].append(float(s) * 100)  # Make percentage
    fin.close()

    values = []
    labels = []
    for i in range(0, len(data_vals[i])):
        values.append(years[i])
        labels.append(data_vals[0][i])

    max_value = None

    for num in labels:
        if (max_value is None or num > max_value):
            max_value = num

    df = pd.read_csv("final.csv")
    ind = 0
    for i in range(len(df)):
        chaine = df.iloc[i, 1][4:]
        d1 = dict()

        if (form.title() == chaine.title()):
            print(form.title(), chaine.title())
            date = df.iloc[i, 2][4:]
            print(date)

            datem = datetime.datetime.strptime(date, "%Y-%m-%d")
            try:
                x = int(values.index(datem.year))
            except:
                x = 0
            print(datem.year, '++++++++++', deb, '+++++++++++', end)
            if (int(datem.year) <= int(end) and int(datem.year) >= int(deb)):
                list_date.append(x)
                print(list_date)
                imdb.append(df.iloc[i, 16][4:])
                di.append(date)
                overview.append(df.iloc[i, 18][4:])
            print("liiiiiiiiiiiiiiiiiiiiiiiiiiiiiiste", di)
            print("liiiiiiiiiiiiiiiiiiiiiiiiiiiiiiste", list_date)

            desc = (df.iloc[i, 14][4:])
            img = (df.iloc[i, 15][4:])
            author = (df.iloc[i, 9][4:])
            genre = (df.iloc[i, 11][4:])

            d1["img"] = img
            d1["genre"] = genre
            d1["author"] = author
            d1["desc"] = desc
            d[ind] = d1
            ind += 1

    for i in range(len(labels)):
        labels[i] = (labels[i] * 100) / max_value
    resultantList = []


    for i in range(len(list_date)):
        dicttt = {}
        if list_date[i] not in resultantList:
            resultantList.append(list_date[i])

            dicttt["imdb"] = imdb[i]
            dicttt["overview"] = overview[i]
            dicttt["date"] = di[i]
            dicttt["x"] =list_date[i]
            dic[list_date[i]] = dicttt


    od = collections.OrderedDict(sorted(dic.items()))

    resultantList.sort()
    print(resultantList)
    return render_template('line_chart3.html', title='Sharbooks Ngram', d=d, max=max_value, labels=values, dic=od,
                           values=labels, ngrams=ngrams[0], x=id, t=resultantList, corpus=corpus, deb=deb, end=end,
                           desc=desc, img=img, author=author, genre=genre, imdb=imdb)


if __name__ == '__main__':
    app.run(port=5555,debug=True)
