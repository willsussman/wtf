package main

import (
    "log"
    "net"
    "net/http"
    "net/rpc"
	"os"
)

// an RPC server in Go

type Args struct{}
type Reply struct{}

type CollectServer string

func (t *CollectServer) Get(args *Args, reply *Reply) error {
	print("Entered Get()\n")
    *reply = "This is a message from the RPC server"
	print("Returning from Get()\n")
    return nil
}

func main() {
	print("Entered main()\n")

    // create and register the rpc
    collecter := new(CollectServer)
	print("Registering collecter...\n")
    rpc.Register(collecter)
	print("Handling HTTP...\n")
    rpc.HandleHTTP()

    // set a port for the server
    port := os.Args[1]

    // listen for requests on 1122
	print("Listening on port "+port+"...\n")
    listener, err := net.Listen("tcp", ":"+port)
	print("Done listening!\n")
    if err != nil {
        log.Fatal("listen error: ", err)
    }

	print("Serving listener...\n")
    http.Serve(listener, nil)
	print("Done serving!\n")

	print("Exiting main()...\n")
}
