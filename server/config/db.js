const mongoose = require("mongoose");

// Function for Setting Connection to Mongodb
const connectDB = async () => {
    try {
        const conn = await mongoose.connect(process.env.MONGO_URI, {
            useNewUrlParser: true,
            useUnifiedTopology: true,
        })

        console.log(`MongoDB connected: ${conn.connection.host}`);
    } catch (error) {
        console.log('Mongodb Error', error);
        process.exit(1);
    }
}

module.exports = connectDB;
