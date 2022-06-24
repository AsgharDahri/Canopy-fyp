const mongoose = require("mongoose");

const questionSchema = new mongoose.Schema({
  user:{ type: String },
  Q1:{ type: String },
  Q2:{ type: String },
  Q3:{ type: String },
  Q4: { type: String},
});



module.exports = mongoose.model("question", questionSchema);