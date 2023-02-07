import React, { useState, useEffect } from "react";
import { Navbar, Nav, Container, Form, Button, Dropdown, ListGroup } from "react-bootstrap";
import { client } from '../utils/axios.util'
import { useHistory, Link } from 'react-router-dom';


function CategoryDropdown(){
    console.log("in category dropdown")
    const [catLevelNames, setCatLevelNames] = useState({});
    const [products, setProducts]= useState('');
    const [error, setError] = useState('');
    const history = useHistory(); 

    
    useEffect(() => {
      const fetchLevelNames = async () => { 
        try {
          const res = await client.get("/get_category");
          setCatLevelNames(res.data);
        } catch (err) {
          setError(err.toString());
        }
      }
      fetchLevelNames();
    }, []);

    const handleClick = (catlevel1, catlevel2) => {
        console.log(catlevel1, catlevel2)
        history.push(`/category/${catlevel1}/${catlevel2}`);
    }
  
    const render = () => {
      if (error) return <p>{error}</p>;
      if (!catLevelNames || !catLevelNames.cat_headers || !catLevelNames.cat_headers.length) return null;
      
      const menuItems = [];
      const {cat_headers, sub_cats} = catLevelNames;
  
      for (const catlevel1 of cat_headers) {
        const subCategories = sub_cats[catlevel1];
        if (!subCategories || !subCategories.length) continue;
        const subCategoryItems = subCategories.map((catlevel2) => (
            //<Link to= {{pathname: "/HomeScreen", state: products}}>
                <ListGroup.Item key={catlevel2} onClick={() => handleClick(catlevel1, catlevel2)}>{catlevel2}</ListGroup.Item>
            //</Link>

        ));
  
        menuItems.push(
          <Nav.Item key={catlevel1}>
            <Dropdown>
              <Dropdown.Toggle variant="dark" bg="dark" expand="lg" id={catlevel1}>
                {catlevel1}
              </Dropdown.Toggle>
              <Dropdown.Menu>
                <ListGroup>
                  {subCategoryItems}
                </ListGroup>
              </Dropdown.Menu>
            </Dropdown>
          </Nav.Item>
        );
      }
  
      return menuItems;
    };
      
      
    
      

      return(
        <Nav className="me-auto">
            {render()}
        </Nav>
      )

}

export default CategoryDropdown;











