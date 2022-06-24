const mongoose = require("mongoose");

const userSchema = new mongoose.Schema({
  firstName:{ type: String },
  lastName:{ type: String },
  dob:{ type: String },
  desease:{ type: String },
  email: { type: String, unique: true },
  policy: { type: String },
  password: { type: String },
 
});



module.exports = mongoose.model("user", userSchema);