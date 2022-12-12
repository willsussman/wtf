package main

import (
    "log"
    "net/rpc"
	"os"
)

// rpc client

type Args struct{}
type Reply struct{}

func main() {
	print("Entered main()\n")

    hostname := os.Args[1]
    port := os.Args[2]

    var reply Reply

    args := Args{}

	print("Dialing "+hostname+":"+port+"...\n")
    client, err := rpc.DialHTTP("tcp", hostname+":"+port)
	print("Done dialing!\n")
    if err != nil {
        log.Fatal("dialing: ", err)
    }

    // Call normally takes service name.function name, args and
    // the address of the variable that hold the reply. Here we
    // have no args in the demo therefore we can pass the empty
    // args struct.
	print("Calling CollectServer.Get...\n")
    err = client.Call("CollectServer.Get", args, &reply)
	print("Done calling!\n")
    if err != nil {
        log.Fatal("error", err)
    }

    // log the result
    log.Printf("%s\n", reply)

	print("Exiting main()...\n")
}
