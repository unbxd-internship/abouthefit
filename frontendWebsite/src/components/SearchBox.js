import React, { useState } from 'react'
import { Button, Form } from 'react-bootstrap'
import { useHistory } from 'react-router-dom'

function SearchBox(props) {
    const [query, setQuery] = useState('')
    let history = useHistory()
    const refresh = () => window.location.reload(true);

    const submitHandler = (e) => {
        e.preventDefault()
        if (query) {
            console.log("hi")
            console.log(query)
            history.push(`/search?q=${query}`)
            
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