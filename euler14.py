i = 2
a = [0 for x in range(1000)]


while (i<10){
    var start=i;
    var cnt=1;
    while (start!=1){
        if (start<1000){
            if(a[start]!=0){
                cnt=cnt+a[int(start)]-1
                start=1
            }
            else{
                if (start%2==0){
                    start=start/2
                }
                else{
                    start=3*start+1
                }
                cnt=cnt+1
            }
        }
        else{
            if (start%2==0){
                start=start/2;
            }
            else{
                start=3*start+1;
            }
            cnt=cnt+1;
        }

    a[i] = cnt;
    print i, cnt;
    i=i+1;
}
