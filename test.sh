#!/bin/sh

PATH=${PATH}:/sbin:/usr/sbin:/bin:/usr/bin:/usr/pkg/bin

name="test"
target="dyndns.localdomain"
domain="dyndns.localdomain"
fqdn="${name}.${domain}"
user="dyndns"
pass="dyndns"
auth="${user}:${pass}"
email="hostmaster@${domain}"

# Retrieve public ip
curip=$(curl -u ${auth} -s -o- https://${target}/dyndns/get_my_ip)

# fetch recorded IP address
homeip=$(curl -u ${auth} -s -o- https://${target}/dyndns/query/a/${fqdn})

if [ "${curip}" != "${homeip}" ]; then
        warnmsg="/!\\ home IP changed to ${curip} /!\\"

        #echo "${warnmsg}"|mail -s "${warnmsg}" ${email}

        curl -u ${auth} \
             -X POST https://${target}/dyndns/update/${domain}/${name}/${curip}
fi
