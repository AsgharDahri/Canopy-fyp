const mongoose = require("mongoose");

const { MONGO_URI } = 'mongodb://localhost:27017/Auth-jwt-myversion';

exports.connect = () => {
  // Connecting to the database
  mongoose
    .connect('mongodb://localhost:27017/Auth-jwt-myversion', {
      useNewUrlParser: true,
      useUnifiedTopology: true,
    //   useCreateIndex: true,
    //   useFindAndModify: false,
    })
    .then(() => {
      console.log("Successfully connected to database");
    })
    .catch((error) => {
      console.log("database connection failed. exiting now...");
      console.error(error);
      process.exit(1);
    });
};