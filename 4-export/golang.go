package main

import (
	"log"
	"net/http"
	"github.com/prometheus/client_golang/prometheus"
	"github.com/prometheus/client_golang/prometheus/promauto"
	"github.com/prometheus/client_golang/prometheus/promhttp"
	)
var (
		requests = promauto.NewCounter(
			prometheus.CounterOpts{
			Name: "hello_worlds_golang_total",
			Help: "Hello Worlds from golangrequested.",
			})
		)

func handler(w http.ResponseWriter, r *http.Request) {
			requests.Inc()
			w.Write([]byte("Hello World from golang"))
			}

func main() {
			http.HandleFunc("/", handler)
			http.Handle("/metrics", promhttp.Handler())
			log.Fatal(http.ListenAndServe(":8000", nil))
			}