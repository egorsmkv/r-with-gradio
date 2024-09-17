library(syuzhet)

#* Log some information about the incoming request
#* @filter logger
function(req){
  cat(as.character(Sys.time()), "-",
    req$REQUEST_METHOD, req$PATH_INFO, "-",
    req$HTTP_USER_AGENT, "@", req$REMOTE_ADDR, "\n")
  plumber::forward()
}


#* Normalize the input
#* @param text The message to normalize
#* @get /normalize
function(text="") {
  result <- paste0("Normalized text: '", text, "'")

  list(normalized_text = result)
}


#* Return the plot of the sentiment of the input text
#* @param text The text to analyze
#* @serializer png
#* @post /sentiment-plot
function(text) {
  s_v <- get_sentences(text)
  s_v_sentiment <- get_sentiment(s_v)

  plot(
    s_v_sentiment, 
    type="l", 
    main="Example Plot Trajectory", 
    xlab = "Narrative Time", 
    ylab= "Emotional Valence"
  )
}
