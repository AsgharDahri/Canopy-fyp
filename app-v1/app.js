require("./config/database").connect();
const express = require("express");
const path=require('path')
const app = express();
const bcrypt=require('bcrypt')
const cookieParser=require('cookie-parser');
const User = require("./model/user");
const bodyParser = require('body-parser');
const user = require("./model/user");
const Exercise=require('./model/exercise')
const jwt=require('jsonwebtoken');
const async = require("hbs/lib/async");
const Auth=require('./middleware/auth')
const Question=require('./model/Qeustions')
//middlewares
app.use(express.json());
const PublicPath=path.join(__dirname,'/Public')
const viewsPath=path.join(__dirname,'/template/views')
app.set('view engine','hbs')
// app.use(express.static(partialPath))
app.set('views',viewsPath)
app.use(bodyParser.urlencoded({extended:true}))
app.set('public',PublicPath)
app.use(cookieParser())
app.use(express.static(__dirname+'/Public/img'));
console.log(__dirname+'/Public')
app.get("/", (req, res) => {
    res.render('Home.hbs')
});

app.get("/login", (req, res) => {
        res.render('login.hbs')
});
    
app.get("/Register", (req, res) => {
        res.render('Register.hbs')
});


app.post("/Register",  async(req, res) => {
    const {firstName,lastName,dob,desease, email,policy,password}=req.body
    console.log(req.body);
// const date2 = new Date();

    if(firstName && lastName && dob && desease &&  email && policy && password){
        // console.log('');
        try{
            // const pass=await bcrypt.hash(password,10);
            // console.log(pass);
            const userExistance=await User.create({firstName,lastName,dob,desease, email,policy,password})
           console.log(userExistance._id);
           const id=userExistance._id
           if(userExistance)
           {
            const token=jwt.sign({id},'Asghar',{expiresIn:3*24*60*60})
            res.cookie('jwt',token,{httpOnly:true, maxAge:3*24*60*60*1000})

           res.redirect('/')
           }
         
        }catch(err)
        {
            // if(err.code===11000)
            // {
            //     console.log('user Already exists');
            //     res.redirect('/login')
            // }
            res.redirect('/Register')
        }
      
    }
    else
    {
        res.send('Please fill the form again!')
        console.log('Email or password is missing');
    }

});
 
app.post('/login',async (req,res)=>{
    const {email,password}=req.body
    console.log(req.body.password);
    if( !email && !password)
    {
        res.send('Wrong Password or Email!')

        res.redirect('login')
    }
    else( email && password)
    {
        const userExistance = await User.findOne({ email,password });
        if(userExistance)
        {
            const id=userExistance._id
            const token=jwt.sign({id},'Asghar',{expiresIn:3*24*60*60})
            res.cookie('jwt',token,{httpOnly:true, maxAge:3*24*60*60*1000})
            res.redirect('/')
        }
        else
        {
            res.send('User Not exists or password wrong!')

        }
    // else {
    //     console.log('error occured');
    //     res.send('Please fill the form again! Email already exist')

    //     res.redirect('login')
    // }

    }
    // else
    // {
    //      res.send('Wrong Password or Email!')

    //     res.redirect('login')

    // }
    // const user=await User.findOne()

    // console.log(userExistance.pass);
   
    // console.log( bcrypt.compare(password, userExistance.pass));
    
    
    // console.log(userExistance);

})
app.get('/logout',(req,res)=>{
    res.cookie('jwt','',{maxAge:1})
    res.redirect('/')
})


app.get('/Exercise',Auth,(req,res)=>{
    res.render('Exercise')
})

app.get('/Questions',Auth,(req,res)=>{
    res.render('Questions')
})
app.get('/ExerciseDashboard',Auth,(req,res)=>{
    res.render('ExerciseDashboard')
})

app.post('/countExercies',Auth,async(req,res)=>{
    const count=req.body.countExercies;
    if(count)
    {
        // const counted=await Exercise.create({''})
    }
})
app.get('/hips',Auth,(req,res)=>{
    res.render('Hips')
})

app.get('/legs',Auth,(req,res)=>{
    res.render('legs')
})

app.get('/abdominal',Auth,(req,res)=>{
    res.render('abdominal')
})

app.post('/question',Auth,async(req,res)=>{
    const {Q1,Q2,Q3,Q4}=req.body;
    console.log(Q1,Q2,Q3,Q4);

    if(Q1 && Q2 && Q3 && Q4)
    {
        const submitted=await Question.create({Q1,Q2,Q3,Q4})
        if(submitted)
        {
            console.log('Yes')
             res.redirect('/')

        }
        
    }
   
  
})

app.get('/policy',(req,res)=>{
    res.render('policy.hbs')
})

app.get('/BentOver',(req,res)=>{
    res.render('BentOver.hbs')
})
app.get('/bHips',(req,res)=>{
    res.render('bHips.hbs')
})

app.get('/CLegs',(req,res)=>{
    res.render('cLegs.hbs')
})
app.get('/lRoman',(req,res)=>{
    res.render('lRoman.hbs')
})

app.get('/rTwist',(req,res)=>{
    res.render('rTwist.hbs')
})
module.exports = app;

