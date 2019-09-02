import React, {useState, useEffect} from 'react'
import axios from 'axios'
const healthsites_url = 'https://healthsites.io/api/v1/healthsites/search?search_type=facility&name=bandung&format=json'


const Services = () => {
    const [services, setServices] = useState([])
    console.log(axios.get(healthsites_url))
    // useEffect( () => {
    //     axios.get(baseUrl).then(response.data => setSurvivors(response.data))}, []
    // )

    return(
       services.map( (service) => <div className='card'> service </div>)
    )
}

export default Services;