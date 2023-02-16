import React, { useState, useEffect } from "react";
import { Navbar, Nav, Container, Form, Button, Dropdown, ListGroup } from "react-bootstrap";
import { client } from '../utils/axios.util'
import { useHistory, Link } from 'react-router-dom';

//to call API to get categories, display categories in 
//dropdown and link to categories and subcategories on click


function CategoryDropdown(){
    const [catLevelNames, setCatLevelNames] = useState({}); // to get category levels from API
    const [products, setProducts]= useState('');
    const [error, setError] = useState('');
    const history = useHistory(); 
    const refresh = () => window.location.reload(true); 
    const [showDropdown, setShowDropdown] = useState(false);

    
    useEffect(() => {
      const fetchLevelNames = async () => { 
        try {
          const res = await client.get("/get_category"); //api call to get categories
          setCatLevelNames(res.data);
        } catch (err) {
          setError(err.toString());
        }
      }
      fetchLevelNames();
    }, []);

    const handleClick = (catlevel1, catlevel2) => {
        history.push(`/category/${catlevel1}/${catlevel2}/`);
        refresh();
    }
    const handleClickOne = (catlevel1) => {
      history.push(`/category/${catlevel1}/`);
      
  }

    const render = () => {
      if (error) return <p>{error}</p>;
      if (!catLevelNames || !catLevelNames.cat_headers || !catLevelNames.cat_headers.length) return null;
      
      const menuItems = [];
      const {cat_headers, sub_cats} = catLevelNames;
  
      for (const catlevel1 of cat_headers) {
        const subCategories = sub_cats[catlevel1];
        if (!subCategories || !subCategories.length) continue;
        const subCategoryItems = subCategories.map((catlevel2) => ( //to print subcategories in dropdown
              <ListGroup.Item key={catlevel2} onClick={() => handleClick(catlevel1, catlevel2)}>{catlevel2}</ListGroup.Item>
        ));
  
        menuItems.push(
          <Nav.Item key={catlevel1}>
            <Dropdown 
            onMouseLeave={() => setShowDropdown(false)}
            onMouseOver={() => setShowDropdown(true)}
            >
              <Dropdown.Toggle variant="dark" bg="dark" expand="lg" id={catlevel1} onClick={()=>handleClickOne(catlevel1)}>
                {catlevel1}
              </Dropdown.Toggle>
              <Dropdown.Menu show={showDropdown}>
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











