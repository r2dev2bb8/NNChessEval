import torch
from torch.autograd import Variable
from torch.utils.data import Dataset, DataLoader

LETTER_TO_NUMBER = {
        'k' : -4,
        'q' : -9,
        'r' : -5,
        'b' : -3.25,
        'n' : -3,
        'p' : -1,
        'P' : 1,
        'N' : 3,
        'B' : 3.25,
        'R' : 5,
        'Q' : 9,
        'K' : 4
}

# rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2
def fenToInputs(fen):
    output = []
    ranks = fen.split('/')
    last = ranks.pop().split(' ')
    ranks.append(last.pop(0))
    color = last.pop(0)
    for rank in ranks:
        for c in rank:
            if c in LETTER_TO_NUMBER:
                output.append(LETTER_TO_NUMBER[c])
            else:
                for i in range(int(c)): output.append(0)
    output.append(int(color == 'w'))
    return output

# 0 is black win, 4 is white win
def evalSimplify(ipt):
    try:
        e = eval(ipt)
    except:
        if ipt[1] == '-':
            return [1, 0, 0, 0, 0]
        return [0, 0, 0, 0, 1]
    if e <= -1.5 * 100:
        return [1, 0, 0, 0, 0]
    elif -1.5 * 100 < e <= -.75 * 100:
        return [0, 1, 0, 0, 0]
    elif -.75 * 100 < e < .75 * 100:
        return [0, 0, 1, 0, 0]
    elif .75 * 100 <= e < 1.5 * 100:
        return [0, 0, 0, 1, 0]
    else:
        return [0, 0, 0, 0, 1]

class ChessDataset(Dataset):
    def __init__(self, fenfile, evalfile):
        with open(fenfile, 'r') as fin:
            self.x_data = Variable(torch.Tensor([fenToInputs(fen[:-1]) for fen in fin.readlines()]))
        with open(evalfile, 'r') as fin:
            self.y_data = Variable(torch.LongTensor([evalSimplify(e[:-1]).index(1) for e in fin.readlines()]))
            # self.y_data = Variable(torch.Tensor([int(evalSimplify(e[:-1])[2] == 1) for e in fin.readlines()]))
        print(len([i for i in self.y_data if float(i) == 1]))
        print(len(self.y_data))
        self.len = min(len(self.x_data), len(self.y_data))
    
    def __getitem__(self, index):
        return self.x_data[index], self.y_data[index]

    def __len__(self):
        return self.len

def main():
    print(fenToInputs("rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2"))
    d = ChessDataset("data/Tivfentest.txt", "data/fentestout1thread.txt")
    print(d[3])

if __name__ == "__main__":
    main()
