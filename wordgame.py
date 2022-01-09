import random

class Wordle:
    def __init__(self):
        self.acceptable_words=[]
        with open("words.txt","r") as inf:
            for line in inf:
                self.acceptable_words.append(line.strip())
        self.solutions=[]
        cutoff=18
        with open("solutions.txt","r") as inf:
            for line in inf:
                if int(line.split()[1].strip())<=cutoff:
                    self.solutions.append(line.split()[0])
        self.solution = random.choice(self.solutions)
        self.guesses=[]
        self.blocks=[]
        self.solved=False

    def play(self):
        while not self.solved and len(self.guesses) <6:
            word = self.make_guess()
            self.guesses.append(word)
            block=self.check(word)
            self.blocks.append(block)
            print(block)
            if word.upper()==self.solution:
                print("GEWONNNEN!")
                self.solved=True
        if len(self.guesses)==6 and not self.solved:
            print("VERLOREN!")
            print("Das Wort war: "+self.solution)
        print("\n".join(self.blocks))
        return block

    def play2(self, word):
        self.guesses.append(word)
        block=self.check(word)
        print(word)
        print(block)
        self.blocks.append(block)
        if word.upper()==self.solution:
            print("GEWONNNEN!")
            self.solved=True
            print("\n".join(self.blocks))
        if len(self.guesses)==6 and not self.solved:
            print("VERLOREN!")
            print("Das Wort war: "+self.solution)
            print("\n".join(self.blocks))
        return block

    def check(self,word):
        output=""
        for i,letter in enumerate(word):
            c="🔲"
            if letter in self.solution:
                c="🟨"
            if self.solution[i]==letter:
                c="🟩"
            output+=c
        return output

    def make_guess(self):
        word="X"
        while word.upper() not in self.acceptable_words:
            print("Eingabe:")
            word=input()
            if word.upper() not in self.acceptable_words:
                print("Wort nicht zulässig.")
        return word


class Solver:
    def __init__(self):        
        self.characters="ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜ"
        self.acceptable_words=[]
        with open("words.txt","r") as inf:
            for line in inf:
                self.acceptable_words.append(line.strip())
        self.solutions=[]
        cutoff=18
        with open("solutions.txt","r") as inf:
            for line in inf:
                if int(line.split()[1].strip())<=cutoff:
                    self.solutions.append(line.split()[0])
        self.guesses=[]
        self.blocks=[]

    def possible_solutions(self):
        poss_chars=[set(c for c in self.characters) for i in range(5)]
        in_chars=set()
        out_chars=set()
        for i in range(len(self.guesses)):
            g = self.guesses[i]
            b = self.blocks[i]
            for j in range(5):
                if b[j]=="🔲":
                    for k in range(5):
                        poss_chars[k].discard(g[j])
                    out_chars.add(g[j])
                if b[j]=="🟩":
                    for k in range(5):
                        if k!=j:
                            poss_chars[k].discard(g[j])
                        else:
                            poss_chars[k]=set(g[j])
                    in_chars.add(g[j])
                if b[j]=="🟨":
                    poss_chars[j].discard(g[j])
                    in_chars.add(g[j])
        sol=[]
        for s in self.solutions:
            possible=True
            for i,c in enumerate(s):
                if c not in poss_chars[i]:
                    possible = False
            for c in in_chars:
                if c not in s:
                    possible = False
            if possible:
                sol.append(s)
        return sol, in_chars, out_chars

    def play(self):
        W = Wordle()
        firstguess=random.choice(self.solutions)
        self.guesses.append(firstguess)
        block = W.play2(firstguess)
        self.blocks.append(block)
        while len(W.guesses)<6 and not W.solved:
            sol, in_chars, out_chars = self.possible_solutions()
            #print(len(sol))
            nextguess=""
            if len(sol)<=(6-len(W.guesses)):
                nextguess = random.choice(sol)
            else:
                if len(in_chars)<4:
                    m=0
                    nextguess=self.acceptable_words[0]
                    for word in self.acceptable_words:
                        newletters=set([c for c in word if c not in in_chars and c not in out_chars])
                        if len(newletters)>m:
                            m=len(newletters)
                            nextguess=word
                else:
                    #print("X")
                    nextguess = random.choice(sol)
                    #TODO optimize this step
            self.guesses.append(nextguess)
            block = W.play2(nextguess)
            self.blocks.append(block)


        # Guess random word that is a solution
        # WHILE NOT SOLVED:
        #   Calculate list of possible solutions
        #   IF len(poss_solutions)<remaining_guesses: Try all answers
        #   ELSE:
        #     IF correct letters <4: Guess word with as many different letters as possible
        #       ELSE:
        #        try random word with letters available   


if __name__=="__main__":
    S = Solver()
    S.play()