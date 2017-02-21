(ns async-tea-party.core
  (:gen-class)
  (:require [clojure.core.async
            :refer [>! <! >!! <!! chan close! go go-loop alts!]]))

(def google-tea-service-chan (chan 10))
(def yahoo-tea-service-chan (chan 10))
(def result-chan (chan 10))

(defn random-add []
  (reduce + (repeat (rand-int 100) 1)))

(defn request-google-tea-service []
  (go
    (random-add)
    (>! google-tea-service-chan
        "tea compliments of google")))

(defn request-yahoo-tea-service []
  (go
    (random-add)
    (>! yahoo-tea-service-chan
        "tea compliments of yahoo")))

(defn request-tea []
  (request-google-tea-service) ;
  (request-yahoo-tea-service) ;
  (go (let [[v] (alts! ;
                  [google-tea-service-chan
                   yahoo-tea-service-chan])]
        (>! result-chan v))))

(defn -main [& args]
  (println "Requesting tea!")
  (request-tea)
  (println (<!! result-chan)))
