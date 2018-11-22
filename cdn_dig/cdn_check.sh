#!/bin/bash

echo -n "Please enter the domain: " 
read domain
echo -n "Please enter the isp: " 
read isp

if [ -z "$domain" ] || [ -z "$isp" ]; then
    echo "enter the args."
    exit 0
fi

#echo $domain
#echo $isp

port=80
count=0

echo "[`date`] task begin..."
echo "[`date`] get cdn nodes ip list..."

while true
do
    if [ "x$isp" == "xall" ]; then
        tmp=$(/usr/bin/python /usr/local/cdn_dig/cdig.py --domain=$domain --isp=ctl,cmb,cer,cnc | grep "/tmp/dig/node_" | awk '{print $4}')
    else
        tmp=$(/usr/bin/python /usr/local/cdn_dig/cdig.py --domain=$domain --isp=$isp | grep "/tmp/dig/node_" | awk '{print $4}')
    fi
    
    if [ -n "$tmp" ]; then
        break
    else
        count=$(echo "$count + 1"|bc)
        if [ $count -gt 5 ]; then
            echo "[`date`] The domain maybe error.Please to check args and run this shell again!!!"
            exit 0
        else
           continue
        fi
    fi
done

echo "[`date`] update the ip list file..."
grep -vE "^$" /tmp/dig/node_* > /usr/local/cdn_dig/tmp_ip.list

echo "[`date`] begin to check cdn nodes status,Please wait ..."
/usr/bin/python /usr/local/cdn_dig/web_cdn_monitor.py /usr/local/cdn_dig/tmp_ip.list $domain $port > /usr/local/cdn_dig/results.txt
sleep 1
/usr/bin/python /usr/local/cdn_dig/web_cdn_monitor.py /usr/local/cdn_dig/tmp_ip.list $domain $port > /usr/local/cdn_dig/results.txt
cat /usr/local/cdn_dig/results.txt

rm -f /tmp/dig/* /usr/local/cdn_dig/content.txt

echo "[`date`] task end! Please to read the file results.txt for the results."
