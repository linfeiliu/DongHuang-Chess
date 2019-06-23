class Board:
    def __init__(self, m, n):
        self.size = (m, n)
        self.matrix = [[0 for j in range(n)] for i in range(m)]

    def __str__(self):
        mark = {0: "", 1: "✖️", -1: "🔴"}
        board = ""
        board += " \t"
        for j in range(self.size[1]):
            board += str(j) + "\t"
        board += "\n"
        for i in range(self.size[0]):
            board += str(i) + "\t"
            for item in self.matrix[i]:
                board += mark[item] + "\t"
            board += "\n"
        return board

    def update(self, pos, sign):
        i = pos[0]
        j = pos[1]
        if (
            i not in range(0, self.size[0])
            or j not in range(0, self.size[1])
            or sign not in [-1, 0, 1]
        ):
            return False
        if self.matrix[i][j] != 0:
            return False
        else:
            self.matrix[i][j] = sign

    def check(self, target, directions, sign):
        t = self.matrix[target[0]][target[1]]
        if t != sign:
            return False
        for d in directions:
            try:
                if (
                    (target[0] + d[0]) < 0
                    or (target[1] + d[1]) < 0
                    or self.matrix[target[0] + d[0]][target[1] + d[1]] != t
                ):
                    return False
            except:
                return False
        return True

    def copy(self):
        size = self.size
        newboard = Board(size[0], size[1])
        newboard.matrix = [row[:] for row in self.matrix]
        return newboard

    def ifwin(self, sign, pos=None):
        win = [
            [(-1, 1), (-2, 2), (-3, 3)],
            [(0, 1), (0, 2), (0, 3)],
            [(1, 1), (2, 2), (3, 3)],
            [(1, 0), (2, 0), (3, 0)],
        ]
        if pos != None:
            return self.simulate(pos, sign).ifwin(sign)
        else:
            for i in range(self.size[0]):
                for j in range(self.size[1]):
                    for pos in win:
                        if self.check((i, j), pos, sign) == True:
                            return True
        return False

    def iflose(self, sign, pos=None):
        lose = [
            [(-1, 1), (-2, 2)],
            [(0, 1), (0, 2)],
            [(1, 1), (2, 2)],
            [(1, 0), (2, 0)],
        ]
        if pos != None:
            return self.simulate(pos, sign).iflose(sign)
        else:
            for i in range(self.size[0]):
                for j in range(self.size[1]):
                    for pos in lose:
                        if self.check((i, j), pos, sign) == True:
                            return True
        return False

    def evaluate(self):
        if self.ifwin(1) == True:
            return "1win"
        if self.ifwin(-1) == True:
            return "-1win"
        if self.iflose(1) == True:
            return "1lose"
        if self.iflose(-1) == True:
            return "-1lose"
        if self[0] == []:
            return "draw"
        return ""

    def simulate(self, pos, sign):
        newboard = self.copy()
        newboard.update(pos, sign)
        return newboard

    def __getitem__(self, key):
        positions = []
        if type(key) == int:
            sign = key
            for i in range(self.size[0]):
                for j in range(self.size[1]):
                    if self.matrix[i][j] == sign:
                        positions.append((i, j))
        elif type(key) == tuple:
            sign = key[0]
            stat = key[1]
            if stat == "win":
                for pos in self[0]:
                    if self.ifwin(sign, pos) == True:
                        positions.append(pos)
            elif stat == "lose":
                for pos in self[0]:
                    if self.iflose(sign, pos) == True:
                        positions.append(pos)
            elif stat == "av":
                for pos in self[0]:
                    if self.ifwin(sign, pos) == True or self.iflose(sign, pos) == False:
                        positions.append(pos)
        return positions

    def getpattern(self):
        p = ""
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                p += str(self.matrix[i][j])
        return p

    def auto(self, sign):
        import random

        decision = None
        self_win_positions = self[sign, "win"]
        if len(self_win_positions) != 0:
            decision = random.choice(self_win_positions)
            self.update(decision, sign)
            return
        other_win_positions = self[-sign, "win"]
        if len(other_win_positions) != 0:
            decision = random.choice(other_win_positions)
            if decision in self[sign, "av"]:
                self.update(decision, sign)
                return
        normal_positions = self[sign, "av"]
        score = {}
        for pos in normal_positions:
            score[pos] = 0
            sim = self.simulate(pos, sign)
            score[pos] += len(sim[sign, "win"])
            score[pos] += len(sim[sign, "av"]) - len(sim[-sign, "av"])
            score[pos] -= len(sim[sign, "lose"]) - len(sim[-sign, "lose"])
            other_av = sim[-sign, "av"]
            if len(sim[sign, "win"]) > 1:
                score[pos] += 100
            if pos in other_av:
                score[pos] += 1
            for pos2 in sim[-sign, "av"]:
                sim2 = sim.simulate(pos2, -sign)
                o_win = set(sim2[-sign, "win"])
                s_lose = set(sim2[sign, "lose"])
                if len(o_win & s_lose) != 0:
                    score[pos] -= 100
        evaluated_positions = list(score.items())
        evaluated_positions.sort(key=lambda x: x[1], reverse=True)
        if len(evaluated_positions) != 0:
            highest = []
            for p in evaluated_positions:
                if p[1] == evaluated_positions[0][1]:
                    highest.append(p[0])
            decision = random.choice(highest)
        else:
            decision = random.choice(self[0])
        self.update(decision, sign)


if __name__ == "__main__":
    b = Board(5, 5)
    import os

    mark = {0: "", 1: "✖️", -1: "🔴"}
    sign = 1
    os.system("cls")
    print(b)
    while True:
        pos = input("Where? ")
        if pos == "exit":
            exit()
        pos = pos.split()

        if b.update((int(pos[0]), int(pos[1])), sign) == False:
            continue

        # b.auto(sign)

        os.system("cls")
        print(b)
        result_dict = {
            "1win": mark[1] + " win!",
            "-1win": mark[-1] + " win!",
            "1lose": mark[1] + " lose!",
            "-1lose": mark[-1] + " lose!",
            "draw": "Draw!",
        }
        ev = b.evaluate()
        if ev != "":
            input(result_dict[ev])
            break
        os.system("cls")
        b.auto(-sign)
        print(b)
        ev = b.evaluate()
        if ev != "":
            input(result_dict[ev])
            break
        # sign = -sign

