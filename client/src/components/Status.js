import React, {useState, useEffect} from 'react'
import axios from 'axios'
const baseUrl = 'https://resp-angelhack.herokuapp.com/api/survivors'

const Status = () => {
    const [survivors, setSurvivors] = useState([])
    useEffect( () => {
        axios.get(baseUrl).then(response => setSurvivors(response.data))}, []
    )

    const survivorCards = () => {
        return(
            survivors.map( (survivor) => 
            <div class="card">
            <div class="card-body">
                <h4 class="card-title">{survivor.first_name} {survivor.family_name}</h4>
                <h6 class="card-subtitle mb-2 text-muted">Age: {survivor.age} Years</h6>
                <p class="card-text">Needed Services: {survivor.needed_services}</p>
            </div>
            </div>
        )
        )
    }
    console.log(survivors)

    return(
        <div className='survivors'>
            <div className='col'>
            {survivorCards()}
            </div>  
            </div>
    )
}

export default Status;