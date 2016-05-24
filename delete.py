import random

def rec():
    with open('toMonk','a+') as f:
        first_line = f.readline()
        list_recordings = []
        
        i = 0
        # Goes through each line
        for i, line in enumerate(f):
            if 'r' in line:
                rec_num = line[1:-1]
                list_recordings.append(int(rec_num))

        # Writes first line
        if i == 0 and 'r' not in first_line:
            f.write('r1\n')
            f.write('x {0} y {1}'.format(random.randint(1,1000), random.randint(1,1000)))
            #write coords here
            return 1
        try:
            max_num = int(max(list_recordings))
        except:
            max_num = 1

        # recordings go here
        f.write('\nr{}\n'.format(max_num+1))
        f.write('x {0} y {1}'.format(random.randint(1,1000), random.randint(1,1000)))
    #print(list_recordings)
    return max_num 

def play(nameOfFile, max_num):
    #will get a random recording
    ran_rec = random.randint(1,max_num+1)
    print("max",max_num)
    print("ran",ran_rec)

    with open(nameOfFile,'r') as f:
        for i,line in enumerate(f):
            if 'r{0}'.format(ran_rec) in line:
                print('Found at',i)
                print(line)
                print(f.next())
        for line in f:
            f = line.find("x")+1
            s = line.find("y")
            x = int(line[f:s])
            y = int(line[s+2:])

            autopy.mouse.move(x,y)
            time.sleep(.0008)

num = rec()
play('toMonk',num)
