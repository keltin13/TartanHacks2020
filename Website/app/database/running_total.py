# This method is meant to add up the running total for a player

# userID is a string to access the database
# database is dictionary, userID is the user's ID
from app.database.main import *
import matplotlib.pyplot as plt

def running_total(user_id):
    bet_history = [(1581685537.545163,100, -1)]
    bankroll = 100
    bets = get_user_bets(user_id, 'C://Users/kelti/Documents/GitHub/TartanHacks2020/website/app/database/data.json')
    if bets == None:
        return None
    for i in range(len(bets)):
        winnings = bets[i]["net"]
        curr_id = bets[i]["bet_id"]
        time = bets[i]["timestamp"]
        bankroll += winnings
        bet_history.append((time, bankroll, curr_id))
    data = []
    for j in range(len(bet_history)):
        data.append(bet_history[j][0])
    #print(data)
    #print(bet_history)
    mergeSort(data, bet_history)
    #print(data)
    #print(bet_history)
    return bet_history
    #returns a list of (time, total, betid)


    # from https://www.cs.cmu.edu/~112/notes/notes-efficiency.html
def merge(a, b, start1, start2, end):
    index1 = start1
    index2 = start2
    length = end - start1
    aux = [None] * length
    aux2 = [None] * length
    for i in range(length):
        if ((index1 == start2) or
            ((index2 != end) and (a[index1] > a[index2]))):
            aux[i] = a[index2]
            aux2[i] = b[index2]
            index2 += 1
        else:
            aux[i] = a[index1]
            aux2[i]= b[index1]
            index1 += 1
    for i in range(start1, end):
        a[i] = aux[i - start1]
        b[i] = aux2[i - start1]

def mergeSort(a, b):
    n = len(a)
    step = 1
    while (step < n):
        for start1 in range(0, n, 2*step):
            start2 = min(start1 + step, n)
            end = min(start1 + 2*step, n)
            merge(a, b, start1, start2, end)
        step *= 2

def visualize(bet_history, user_id):
    if bet_history == None:
        return None
    username = get_user_by_id(user_id, 'C://Users/kelti/Documents/GitHub/TartanHacks2020/website/app/database/data.json')["username"]
    time = []
    money = []
    tracker = []
    for i in range(len(bet_history)):
        time.append(bet_history[i][0])
        money.append(bet_history[i][1])
        tracker.append(bet_history[i][2])
        print(time)
        #print(money)
    plt.plot(time, money, color = 'r')
    plt.xlabel("TIME")
    plt.ylabel("WINNINGS")
    plt.title(f"{username} WINNINGS")
    maxTime = time[len(time) - 1]
    maxMoney = max(money) * 1.1
    #plt.axis([1581585537.545163, maxTime, 0, maxMoney])
    return plt

'''
import io
import random
from flask import Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

@app.route('/plot.png')
def plot_png():
    fig = create_figure()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

def create_figure():
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    xs = range(100)
    ys = [random.randint(1, 50) for x in xs]
    axis.plot(xs, ys)
    return fig


running_total("000001")
visualize(running_total("000001"), "000001")
'''
