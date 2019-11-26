for i in range(0,10):
    fin = 'test' + str(i) + '.txt'
    fout = 'testu'+ str(i) + '.txt'
    with open(fin, 'r') as fi:
        with open(fout, 'w') as fo:
            for line in fi:

                lowercase_line = line.lower()
                fo.write(lowercase_line)
