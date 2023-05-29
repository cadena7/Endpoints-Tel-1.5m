#!/bin/bash

prende_consola() {

(
    sleep 3
    echo admin
    sleep 1
    echo admin
    sleep 2
    echo "set outlet 1 on "
    sleep 1
    echo "logout"
    sleep 3
    ) | telnet -4 -l control 192.168.0.252
}


apaga_consola() {

(
    sleep 3
    echo admin
    sleep 1
    echo admin
    sleep 2
    echo "set outlet 1 off "
    sleep 1
    echo "logout"
    sleep 3
    ) | telnet -4 -l control 192.168.0.252
}



case "$1" in
    prende)
        prende_consola
        exit 0
        ;;
    apaga)
        apaga_consola
        exit 0
        ;;
    *)
        echo "Uso: $0 {prende/apaga}"
        exit 1
        ;;
esac


