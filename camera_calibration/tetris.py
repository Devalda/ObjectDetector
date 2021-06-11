import random, replit
import time
import threading
import queue

q = queue.Queue(1)

state = "start"
lastUpdate = 0
updateDelay = .5  # .5
board = [[0 for x in range(10)] for y in range(22)]
tempBoard = [[0 for x in range(10)] for y in range(22)]
barrier = ""
for i in range(25):
    barrier += "#"
score = 0
msg = ""
multiplier = 1
lastScore = 0
combo = 0
lastTetris = 0
pieceKeys = ["O", "T", "L", "J", "S", "I", "Z"]
pieceQueue = []
random.shuffle(pieceKeys)
while pieceKeys[0] == "Z" or pieceKeys[0] == "S":
    random.shuffle(pieceKeys)
for i in pieceKeys:
    pieceQueue.append(i)
pieces = {
    "I": {
        0: [[0, 0, 0, 0], [1, 1, 1, 1], [0, 0, 0, 0], [0, 0, 0, 0]],
        1: [[0, 0, 1, 0], [0, 0, 1, 0], [0, 0, 1, 0], [0, 0, 1, 0]],
        2: [[0, 0, 0, 0], [0, 0, 0, 0], [1, 1, 1, 1], [0, 0, 0, 0]],
        3: [[0, 1, 0, 0], [0, 1, 0, 0], [0, 1, 0, 0], [0, 1, 0, 0]]
    },
    "J": {
        0: [[1, 0, 0], [1, 1, 1], [0, 0, 0]],
        1: [[0, 1, 1], [0, 1, 0], [0, 1, 0]],
        2: [[0, 0, 0], [1, 1, 1], [0, 0, 1]],
        3: [[0, 1, 0], [0, 1, 0], [1, 1, 0]]
    },
    "L": {
        0: [[0, 0, 1], [1, 1, 1], [0, 0, 0]],
        1: [[0, 1, 0], [0, 1, 0], [0, 1, 1]],
        2: [[0, 0, 0], [1, 1, 1], [1, 0, 0]],
        3: [[1, 1, 0], [0, 1, 0], [0, 1, 0]]
    },
    "O": {
        0: [[0, 1, 1, 0], [0, 1, 1, 0], [0, 0, 0, 0]],
        1: [[0, 1, 1, 0], [0, 1, 1, 0], [0, 0, 0, 0]],
        2: [[0, 1, 1, 0], [0, 1, 1, 0], [0, 0, 0, 0]],
        3: [[0, 1, 1, 0], [0, 1, 1, 0], [0, 0, 0, 0]]
    },
    "S": {
        0: [[0, 1, 1], [1, 1, 0], [0, 0, 0]],
        1: [[0, 1, 0], [0, 1, 1], [0, 0, 1]],
        2: [[0, 0, 0], [0, 1, 1], [1, 1, 0]],
        3: [[1, 0, 0], [1, 1, 0], [0, 1, 0]]
    },
    "T": {
        0: [[0, 1, 0], [1, 1, 1], [0, 0, 0]],
        1: [[0, 1, 0], [0, 1, 1], [0, 1, 0]],
        2: [[0, 0, 0], [1, 1, 1], [0, 1, 0]],
        3: [[0, 1, 0], [1, 1, 0], [0, 1, 0]]
    },
    "Z": {
        0: [[1, 1, 0], [0, 1, 1], [0, 0, 0]],
        1: [[0, 0, 1], [0, 1, 1], [0, 1, 0]],
        2: [[0, 0, 0], [1, 1, 0], [0, 1, 1]],
        3: [[0, 1, 0], [1, 1, 0], [1, 0, 0]]
    }
}

hp = {}
tempPop = pieceQueue.pop(0)
cp = {
    "shapeName": tempPop,
    "shape": pieces[tempPop],
    "rot": 0,
    "grounded": False,
    "groundCount": 0,
    "groundMax": 3,
    "done": False,
    "x": 3,
    "y": 0}  # pieces, rotation, x, y


def getInput():
    while True:
        command = input()
        q.put(command)


gi = threading.Thread(target=getInput)
gi.daemon = True
gi.start()

running = True
while running:
    if state == "start":
        if not q.empty():
            j = q.get().upper()
            if j == "S":
                state = "game"
            elif j == "C":
                state = "controls"
        if time.perf_counter() > lastUpdate + updateDelay:
            lastUpdate = time.perf_counter()
            replit.clear()
            toPrint = ""
            for i in range(28):
                toPrint += "_"
            print("████████████████████████████")
            print("█                          █")
            print("█       TERMINAL           █")
            print("█                          █")
            print("████████           █████████")
            print("       █           █ ████████████████")
            print("       █           █ █   TETRIS     █")
            print("       █           █ █████      █████")
            print("       █           █     █      █")
            print("       █████████████     █      █")
            print(" TYPE \"S\" TO START,      ████████")
            print("    \"C\" FOR CONTROLS")
    elif state == "controls":
        if not q.empty():
            j = q.get().upper()
            if j == "S":
                state = "game"
        if time.perf_counter() > lastUpdate + updateDelay:
            lastUpdate = time.perf_counter()
            replit.clear()
            print("####################################")
            print("##############CONTROLS##############")
            print("")
            print("            W: HOLD PIECE")
            print("            S: HARD DROP")
            print("            X: INSTANT SOFT DROP")
            print("")
            print("            A, D: MOVE")
            print("            Q, E: ROTATE")
            print("")
            print("######TYPE \"S\" TO START###########")
            print("####################################")
    elif state == "pause":
        if not q.empty():
            j = q.get().upper()
            if j == "P":
                state = "game"
        if time.perf_counter() > lastUpdate + updateDelay:
            lastUpdate = time.perf_counter()
            replit.clear()
            print("████████████████████████████████████")
            for i in range(10):
                print("█                                  █")
            print("█            PAUSED                █")
            for i in range(11):
                print("█                                  █")
            print("████████████████████████████████████")
    elif state == "gameOver":
        if not q.empty():
            j = q.get().upper()
        if time.perf_counter() > lastUpdate + updateDelay:
            lastUpdate = time.perf_counter()
            replit.clear()
            print("████████████████████████████████████")
            for i in range(10):
                print("█                                  █")
            print("█            GAME OVER             █")  # 36 long
            toDraw = ""
            drawAmt = 16
            for i in range(len(str(score))):
                drawAmt -= 1
            for i in range(drawAmt):
                toDraw += " "
            toDraw += "█"
            print("█           SCORE: " + str(score) + toDraw)
            print("█            CONGRATS!             █")
            for i in range(10):
                print("█                                  █")
            print("████████████████████████████████████")
    elif state == "game":
        # input
        if not q.empty():
            j = q.get().lower()
            for i in range(len(j)):
                if j[i] == "d":
                    blocked = False
                    for indy, y in enumerate(cp["shape"][cp["rot"]]):
                        for indx, x in enumerate(y):
                            if cp["shape"][cp["rot"]][indy][indx] == 1:
                                if cp["x"] + indx + 1 > 9 or board[cp["y"] + indy][cp["x"] + indx + 1] == 1:
                                    blocked = True
                                    break
                    if not blocked:
                        cp["x"] = cp["x"] + 1
                elif j[i] == "a":
                    blocked = False
                    for indy, y in enumerate(cp["shape"][cp["rot"]]):
                        for indx, x in enumerate(y):
                            if cp["shape"][cp["rot"]][indy][indx] == 1:
                                if cp["x"] + indx - 1 < 0 or board[cp["y"] + indy][cp["x"] + indx - 1] == 1:
                                    blocked = True
                                    break
                    if not blocked:
                        cp["x"] = cp["x"] - 1
                elif j[i] == "q":
                    blocked = False
                    if cp["rot"] == 0:
                        cp["rot"] = 3
                    else:
                        cp["rot"] -= 1
                    if cp["rot"] == 3 and cp["grounded"]:
                        cp["y"] -= 1
                    for indy, y in enumerate(cp["shape"][cp["rot"]]):
                        for indx, x in enumerate(y):
                            if cp["shape"][cp["rot"]][indy][indx] == 1:
                                if cp["x"] + indx < 0 or cp["x"] + indx > 9 or board[cp["y"] + indy][
                                    cp["x"] + indx] == 1:
                                    blocked = True
                                    break
                    if blocked:
                        if cp["rot"] == 3 and cp["grounded"]:
                            cp["y"] += 1
                        print("cant Rotate")
                        if cp["rot"] == 3:
                            cp["rot"] = 0
                        else:
                            cp["rot"] += 1

                elif j[i] == "e":
                    blocked = False
                    if cp["rot"] == 3:
                        cp["rot"] = 0
                    else:
                        cp["rot"] += 1
                    if cp["rot"] == 1 and cp["grounded"]:  # may have to hard code this per piece later
                        cp["y"] -= 1
                    for indy, y in enumerate(cp["shape"][cp["rot"]]):
                        for indx, x in enumerate(y):
                            if cp["shape"][cp["rot"]][indy][indx] == 1:
                                if cp["x"] + indx < 0 or cp["x"] + indx > 9 or board[cp["y"] + indy][
                                    cp["x"] + indx] == 1:
                                    blocked = True
                                    break
                    if blocked:
                        if cp["rot"] == 1 and cp["grounded"]:
                            cp["y"] += 1
                        print("cant Rotate")
                        if cp["rot"] == 0:
                            cp["rot"] = 3
                        else:
                            cp["rot"] -= 1
                elif j[i] == "w":
                    if hp == {}:
                        hp = {
                            "shapeName": cp["shapeName"],
                            "shape": cp["shape"],
                            "rot": 0,
                            "grounded": False,
                            "groundCount": 0,
                            "groundMax": 3,
                            "done": False,
                            "x": 3,
                            "y": 0
                        }
                        if len(pieceQueue) < 3:
                            random.shuffle(pieceKeys)
                            for i in pieceKeys:
                                pieceQueue.append(i)
                        tempPop = pieceQueue.pop(0)
                        cp = {
                            "shapeName": tempPop,
                            "shape": pieces[tempPop],
                            "rot": 0,
                            "grounded": False,
                            "groundCount": 0,
                            "groundMax": 3,
                            "done": False,
                            "x": 3,
                            "y": 0}
                    else:
                        tempShapeHolder = cp["shapeName"]
                        cp = hp
                        hp = {
                            "shapeName": tempShapeHolder,
                            "shape": pieces[tempShapeHolder],
                            "rot": 0,
                            "grounded": False,
                            "groundCount": 0,
                            "groundMax": 3,
                            "done": False,
                            "x": 3,
                            "y": 0
                        }
                elif j[i] == "s":
                    if cp["grounded"]:
                        cp["groundCount"] = cp["groundMax"]
                    else:
                        while not cp["grounded"]:
                            cp["y"] += 1
                            for indy, y in enumerate(cp["shape"][cp["rot"]]):
                                for indx, x in enumerate(y):
                                    if cp["shape"][cp["rot"]][indy][indx] == 1:
                                        if cp["y"] + indy + 1 > 21 or board[cp["y"] + indy + 1][cp["x"] + indx] == 1:
                                            cp["grounded"] = True
                                            tempBoard[cp["y"] + indy][cp["x"] + indx] = cp["shape"][cp["rot"]][indy][
                                                indx]
                                            cp["groundCount"] = cp["groundMax"]
                elif j[i] == "x":
                    while not cp["grounded"]:
                        cp["y"] += 1
                        for indy, y in enumerate(cp["shape"][cp["rot"]]):
                            for indx, x in enumerate(y):
                                if cp["shape"][cp["rot"]][indy][indx] == 1:
                                    if cp["y"] + indy + 1 > 21 or board[cp["y"] + indy + 1][cp["x"] + indx] == 1:
                                        cp["grounded"] = True
                                        tempBoard[cp["y"] + indy][cp["x"] + indx] = cp["shape"][cp["rot"]][indy][indx]
                elif j[i] == "p":
                    state = "pause"

        # update
        if time.perf_counter() > lastUpdate + updateDelay:
            lastUpdate = time.perf_counter()
            tempBoard = [[0 for x in range(10)] for y in range(22)]
            cp["grounded"] = False
            for indy, y in enumerate(cp["shape"][cp["rot"]]):
                for indx, x in enumerate(y):
                    if cp["shape"][cp["rot"]][indy][indx] == 1:
                        if cp["y"] + indy + 1 > 21 or board[cp["y"] + indy + 1][cp["x"] + indx] == 1:
                            cp["grounded"] = True
                            tempBoard[cp["y"] + indy][cp["x"] + indx] = cp["shape"][cp["rot"]][indy][indx]
                        else:
                            tempBoard[cp["y"] + indy][cp["x"] + indx] = cp["shape"][cp["rot"]][indy][indx]
            if not cp["grounded"] and cp["groundCount"] < cp["groundMax"]:
                cp["y"] += 1
            else:
                cp["groundCount"] += 1
                if cp["groundCount"] >= cp["groundMax"]:
                    for indy, y in enumerate(cp["shape"][cp["rot"]]):
                        for indx, x in enumerate(y):
                            if cp["shape"][cp["rot"]][indy][indx] == 1:
                                board[cp["y"] + indy][cp["x"] + indx] = 1
                    if len(pieceQueue) < 3:
                        random.shuffle(pieceKeys)
                        for i in pieceKeys:
                            pieceQueue.append(i)
                    tempPop = pieceQueue.pop(0)
                    cp = {
                        "shapeName": tempPop,
                        "shape": pieces[tempPop],
                        "rot": 0,
                        "grounded": False,
                        "groundCount": 0,
                        "groundMax": 3,
                        "done": False,
                        "x": 3,
                        "y": 0}  # pieces, rotation, x, y
                # check for cleared lines
                tlc = 0

                if board[1][5] == 1 or board[1][6] == 1:
                    state = "gameOver"
                for indy, y in enumerate(board):
                    if y == [1 for i in range(10)]:
                        tlc += 1
                        board.pop(indy)
                        board.insert(0, [0 for x in range(10)])
                lastTetris -= 1
                if tlc > 0:
                    combo += 1
                    if tlc == 1:
                        score += 100
                        msg = "SINGLE"
                    elif tlc == 2:
                        score += 300
                        msg = "DOUBLE!#"
                    elif tlc == 3:
                        score += 500
                        msg = "TRIPLE!#"
                    elif tlc == 4:
                        if lastTetris > 0:
                            score += 1200
                            msg = "B2B#TETRIS!!"
                            multiplier += .5
                        score += 800
                        msg = "TETRIS!!"
                        lastTetris = 3
                else:
                    if combo > 1:
                        score += combo * 50
                        msg = str(combo) + " COMBO!!"
                        combo = 0

            # render
            # Drawing
            replit.clear()
            toDraw = "  "
            if not hp == {}:
                print("######HELDPIECE=\"" + str(hp["shapeName"]) + "\"######")
            else:
                print(barrier)
            print("######NEXTPIECE=\"" + str(pieceQueue[0]) + "\"######")
            for indy, y in enumerate(board):
                for indx, x in enumerate(y):
                    if tempBoard[indy][indx] == 1:
                        toDraw += " █"
                    elif x == 0:
                        toDraw += " ."
                    elif x == 1:
                        toDraw += " █"
                toDraw += "  "
                print(toDraw)
                toDraw = "  "
            toDraw = 10
            for i in range(len(str(score))):
                toDraw -= 1
            draw = ""
            for i in range(toDraw):
                draw += "#"
            print("#########SCORE:" + str(score) + draw)  # + "#" for i in range(toDraw))
            if msg == "":
                print(barrier)
            else:
                toPrint = ""
                printAdd = 17
                for i in range(len(msg)):
                    printAdd -= 1
                for i in range(printAdd):
                    toPrint += "#"
                print("########" + msg + toPrint)
                msg = ""