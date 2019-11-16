#以一定粒度切割弹幕文件
def splitDanmu(original,output,grain):

    input=open(original,encoding='utf-8')
    original=input.readlines()
    outputfile=open(output,'w',encoding='utf-8')


    startTime=0
    endTime=startTime+grain
    maxTime=0

    for danmu in original:
        time=float(danmu.split('\t')[1])
        if time>maxTime:
            maxTime=time

    while startTime<=maxTime:
        temp=[]
        for danmu in original:
            time=float(danmu.split('\t')[1])

            if time>=startTime and time <endTime:
                temp.append(danmu.split('\t')[0])

        outputfile.write('\t'.join(temp)+'\n')

        startTime=startTime+grain
        endTime=endTime+grain

    outputfile.close()
    input.close()

    print("以{}秒为间隔分割的弹幕文件已写入{}".format(grain,output))