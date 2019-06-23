from django.http import JsonResponse
from django.shortcuts import render
from .UDCA import *
import time
import threading

global boards
global playerid
global rowN
global columnN
boards = {}
playerid = 0
rowN = 5
columnN = 5


def aiinit(request):
    global playerid
    global rowN
    global columnN
    response = {}
    response["rowlist"] = list(range(rowN))
    response["columnlist"] = list(range(columnN))
    response["rowN"] = rowN
    response["columnN"] = columnN
    response["auto"] = True
    boards[playerid] = Board(rowN, columnN)
    boards[playerid].sign = 1
    boards[playerid].wait = False
    boards[playerid].time = time.time()
    response["id"] = playerid
    playerid += 1
    return render(request, "DHC.html", response)


def update(request):
    global boards
    id = int(request.POST["id"])
    if id not in boards.keys():
        return JsonResponse({"msg": "refresh"})
    b = boards[id]
    b.time = time.time()
    if b.wait == True:
        return JsonResponse({"msg": "wait"})
    b.wait = True
    row = int(request.POST["position[row]"])
    column = int(request.POST["position[column]"])
    if b.update((row, column), b.sign) == False:
        b.wait = False
        return JsonResponse({"msg": "NO!"})
    else:
        b.sign = -b.sign
        result = b.evaluate()
        mark = {0: "", 1: "✖️", -1: "🔴"}
        result_dict = {
            "1win": mark[1] + " win!",
            "-1win": mark[-1] + " win!",
            "1lose": mark[1] + " lose!",
            "-1lose": mark[-1] + " lose!",
            "draw": "Draw!",
            "": "NA",
        }
        response = {
            "msg": result_dict[result],
            "matrix": [
                [mark[b.matrix[i][j]] for j in range(b.size[1])]
                for i in range(b.size[0])
            ],
        }
        if result != "":
            del boards[id]
        b.wait = False
        return JsonResponse(response)


def auto(request):
    global boards
    id = int(request.POST["id"])
    if id not in boards.keys():
        return JsonResponse({"msg": "refresh"})
    b = boards[id]
    b.time = time.time()
    if b.wait == True:
        return JsonResponse({"msg": "wait"})
    b.wait = True
    b.auto(b.sign)
    b.sign = -b.sign
    result = b.evaluate()
    mark = {0: "", 1: "✖️", -1: "🔴"}
    result_dict = {
        "1win": mark[1] + " win!",
        "-1win": mark[-1] + " win!",
        "1lose": mark[1] + " lose!",
        "-1lose": mark[-1] + " lose!",
        "draw": "Draw!",
        "": "NA",
    }
    response = {
        "msg": result_dict[result],
        "matrix": [
            [mark[b.matrix[i][j]] for j in range(b.size[1])] for i in range(b.size[0])
        ],
    }
    if result != "":
        del boards[id]
    b.wait = False
    return JsonResponse(response)


def clear(request):
    global boards
    global playerid
    i = 0
    for id in list(boards.keys()):
        if boards[id].time < time.time() - 5 * 60:
            del boards[id]
            i += 1
    return render(
        request,
        "clear.html",
        {"current": len(boards), "deleted": i, "playerid": playerid},
    )


def updateboard(request):
    global pvpboards
    id = int(request.POST["id"])
    if id not in pvpboards.keys():
        return JsonResponse({"msg": "refresh"})
    b = pvpboards[id]
    if b.startflag == True and request.POST["sign"] == "1":
        b.startflag = False
        print("game")
        return JsonResponse(
            {
                "msg": "Game start!",
                "matrix": [["" for j in range(b.size[1])] for i in range(b.size[0])],
            }
        )
    result = b.evaluate()
    mark = {0: "", 1: "✖️", -1: "🔴"}
    result_dict = {
        "1win": mark[1] + " win!",
        "-1win": mark[-1] + " win!",
        "1lose": mark[1] + " lose!",
        "-1lose": mark[-1] + " lose!",
        "draw": "Draw!",
        "": "NA",
    }
    response = {
        "msg": result_dict[result],
        "matrix": [
            [mark[b.matrix[i][j]] for j in range(b.size[1])] for i in range(b.size[0])
        ],
    }
    # if result != "":
    #     del pvpboards[id]
    return JsonResponse(response)


global pvpboards
global groupflag
pvpboards = {}
groupflag = 0


def pvpinit(request):
    global playerid
    global rowN
    global columnN
    global groupflag
    if groupflag == 0:
        response = {}
        response["rowlist"] = list(range(rowN))
        response["columnlist"] = list(range(columnN))
        response["rowN"] = rowN
        response["columnN"] = columnN
        response["auto"] = False
        response["sign"] = 1
        pvpboards[playerid] = Board(rowN, columnN)
        pvpboards[playerid].sign = 1
        pvpboards[playerid].wait = True
        pvpboards[playerid].time = time.time()
        pvpboards[playerid].startflag = False
        response["id"] = playerid
        playerid += 1
        groupflag = 1
    else:
        response = {}
        response["rowlist"] = list(range(rowN))
        response["columnlist"] = list(range(columnN))
        response["rowN"] = rowN
        response["columnN"] = columnN
        response["auto"] = False
        response["sign"] = -1
        lastid = list(pvpboards.keys())[-1]
        pvpboards[lastid].wait = False
        pvpboards[lastid].time = time.time()
        pvpboards[lastid].startflag = True
        response["id"] = lastid
        playerid += 1
        groupflag = 0
    return render(request, "DHC.html", response)


def pvpupdate(request):
    global pvpboards
    id = int(request.POST["id"])
    if id not in pvpboards.keys():
        return JsonResponse({"msg": "refresh"})
    b = pvpboards[id]
    if b.evaluate() != "":
        return JsonResponse({"msg": "refresh"})
    b.time = time.time()
    if b.wait == True or int(request.POST["sign"]) != b.sign:
        return JsonResponse({"msg": "wait"})
    b.wait = True
    row = int(request.POST["position[row]"])
    column = int(request.POST["position[column]"])
    if b.update((row, column), b.sign) == False:
        b.wait = False
        return JsonResponse({"msg": "NO!"})
    else:
        b.sign = -b.sign
        result = b.evaluate()
        mark = {0: "", 1: "✖️", -1: "🔴"}
        result_dict = {
            "1win": mark[1] + " win!",
            "-1win": mark[-1] + " win!",
            "1lose": mark[1] + " lose!",
            "-1lose": mark[-1] + " lose!",
            "draw": "Draw!",
            "": "NA",
        }
        response = {
            "msg": result_dict[result],
            "matrix": [
                [mark[b.matrix[i][j]] for j in range(b.size[1])]
                for i in range(b.size[0])
            ],
        }
        # if result != "":
        #     del pvpboards[id]
        b.wait = False
        return JsonResponse(response)
