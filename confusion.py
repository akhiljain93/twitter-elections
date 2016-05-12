import sys

def everything(filename):
    if('rep' in filename):
        lenn = 4
    else:
        lenn = 2
    f = open(filename, 'r')

    mat = [[0 for i in range(lenn)] for j in range(lenn)]
    precision = [0. for i in range(lenn)]
    recall = [0. for i in range(lenn)]
    sum_cols = [0 for i in range(lenn)]
    sum_rows = [0 for i in range(lenn)]


    for line in f:
        fields = line.strip().split(',')
        mat[int(fields[1])-1][int(fields[0])-1]+=1

    for i in range(lenn):
        precision[i] = mat[i][i]
        recall[i] = mat[i][i]
        sum_rows[i] = sum(mat[i])
        for j in range(lenn):
            sum_cols[i] += mat[j][i]

    correctt = sum(precision)
    totall = sum(sum_rows)
    new_p = []
    new_r = []
    new_p_total = []
    new_r_total = []
    for i in range(lenn):
        if(sum_cols[i]!=0):
            new_p.append(precision[i]*1.0/sum_cols[i])
            new_p_total.append(precision[i]*1.0/sum_cols[i])
        else:
            new_p_total.append(-1)
        if(sum_rows[i]!=0):
            new_r.append(recall[i]*1.0/sum_rows[i])
            new_r_total.append(recall[i]*1.0/sum_rows[i])
        else:
            new_r_total.append(-1)

    avg_precision = sum(new_p)/len(new_p)
    avg_recall = sum(new_r)/len(new_r)


    macro_score = avg_precision*avg_recall*2/(avg_precision+avg_recall)
    accuracy = correctt*1.0/totall
    print "Average precision: " + str(avg_precision)
    print "Average recall: " + str(avg_recall)
    print "Macro F score: " + str(macro_score)
    print "Accuracy: " + str(accuracy)
    for i in mat:
        for j in i:
            sys.stdout.write(str(j) + ' ')
        sys.stdout.write('\n')


print "Normal"

everything('rep_results.txt')
everything('dem_results.txt')
