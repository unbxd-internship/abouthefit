import React, { useState } from 'react'
import { Button, Form } from 'react-bootstrap'
import { useHistory } from 'react-router-dom'

//to display a searchbox in the header, handle 
//queries sent in the form and push to new url endpoint

function SearchBox(props) {
    const [query, setQuery] = useState('') //state variable to get query from searchbox
    let history = useHistory()
    const refresh = () => window.location.reload(true);

    const submitHandler = (e) => { //search form handler to get query from form and push endpoint
        e.preventDefault()
        if (query) {
            history.push(`/search?q=${query}`)
            refresh();
        } 
    }
    return (
        <Form className="d-flex" onSubmit={submitHandler} inline>
            <Form.Control
              type="query"
              placeholder="Search"
              name='query'
              className="me-2"
              aria-label="query"
              onChange={(e) => setQuery(e.target.value)}
            />
            <Button name='query' type="submit" variant="outline-success">Search</Button>
          </Form>
        
    )
}

export default SearchBox