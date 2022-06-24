const mongoose = require("mongoose");

const execiseSchema = new mongoose.Schema({
  ExerciseName:{ type: String },
  links:{ type: String },
  catagories:{ type: String },
  successRatio: { type: Number},
});



module.exports = mongoose.model("exercise", execiseSchema);