#! /bin/bash


#Calculate the mean value of source coords
n=0
mean_x=0
mean_y=0
mean_r=0
while read -r coord; do
    n=$(($n+1))  
    IFS=','
    arr=${coord#ellipse(} && arr=${arr%)}
    arr=($arr)
    x=${arr[0]};x=${x%.*}
    y=${arr[1]};y=${y%.*}
    r=${arr[2]};r=${r%.*}
    mean_x=$(($mean_x+$x))
    mean_y=$(($mean_y+$y))
    mean_r=$(($mean_r+$r))
done < all_src.reg
mean_x=$(($mean_x/$n))
mean_y=$(($mean_y/$n))
mean_r=$(($mean_r/$n))

#Build the region of background
touch bg.reg
echo "circle($mean_x,$mean_y,$(($mean_r*100)))" > bg.reg
while read -r coord; do
    echo "-$coord" >> bg.reg
done < all_src.reg

echo "Output: bg.reg"
