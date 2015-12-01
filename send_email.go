package main

/* Copyright 2015 Joseph Lewis III <joseph@josephlewis.net>
Licensed under the MIT License

Sends an email from go

*/

import (
	"fmt"
	"net"
	"net/smtp"
	"strings"
)

func main() {
	mx, err := net.LookupMX("bar.edu")
	if err != nil {
		panic(err)
	}
	fmt.Println(len(mx))

	fmt.Println(mx[0])
	mhost := strings.Trim(mx[0].Host, ".")
	fmt.Println(mhost)
	err = smtp.SendMail(mhost+":25", nil, "president@whitehouse.gov", []string{"foo@bar.edu"}, []byte("test"))
	if err != nil {
		fmt.println("error")
		fmt.Println(err)
	}
}
