require('dotenv').config()
const express = require('express')
const app = express()
const cors = require('cors')
const bodyParsers = require('body-parser')

app.use(cors())
app.use(bodyParsers.json())

const Survivor = require('./models/survivor')

app.get('/api/survivors', (req, res) =>
	{Survivor.find({}).then(survivors => {
	    console.log(survivors);
	    res.json(survivors.map(survivor => survivor.toJSON()))
	});
	});


app.post('/api/survivors', (req, res) =>
	 {
	  const survey_answers = req.body.form_response.answers
	  const survivor = new Survivor({
		first_name: survey_answers[0].text,
                family_name: survey_answers[1].text,
		age: survey_answers[2].number,
                recent_experience: survey_answers[3].text,
                needed_services: survey_answers[4].text,
                well_being: survey_answers[5].text,
		friends_relatives: survey_answers[6].text,})

	  survivor.save().then(savedSurvivor => {
	      res.json(savedSurvivor.toJSON())
	  })
	 })
	
const PORT = process.env.PORT
app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`)
})
