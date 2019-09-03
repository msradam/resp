import React, {useState, useEffect} from 'react'
import axios from 'axios'
const baseUrl = 'https://resp-angelhack.herokuapp.com/api/services'

const Services = () => {
    const [services, setServices] = useState([])
    useEffect( () => {
        axios.get(baseUrl, { params:  {'location': 'Phillipines' }}).then(response => setServices(response.data))}, []
    )

    const servicesCards = () => {
        return(
            services.map( (service) => 
            <div class="card">
            <div class="card-body">
                <h4 class="card-title">{services.name}</h4>
                <h6 class="card-subtitle mb-2 text-muted">Facility Type: {services.type} </h6>
            </div>
            </div>
        )
        )
    }

    return(
        <div className='services'>
            <div className='col'>
            {servicesCards()}
            </div>  
            </div>
    )
}

export default Services