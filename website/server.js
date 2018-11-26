var express = require("express");
var app = express();

var port = process.env.PORT || 8080;

app.use(express.static(__dirname + "/public"));

app.get("/", function(req, res) {
  res.render("index");
});

app.use(function(req, res) {
  res.sendFile(__dirname + "/public/error.html");
});

app.listen(port, function() {
  console.log("Server listening on port " + port);
});

// TODO: Check if all error pages actually work or not
// TODO: Try to sort out new address
