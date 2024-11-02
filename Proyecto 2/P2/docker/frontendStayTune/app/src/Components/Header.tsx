import React from 'react';
import { Navbar, Container } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';
import { IoMusicalNotesSharp } from "react-icons/io5";

interface HeaderProps {}



const Header: React.FC<HeaderProps> = ({ }) => {
  const navigate = useNavigate();

  const handleHomeClick = () => {
    
    navigate('/');
  };

  return (
    <Navbar fixed='top' className="w-100">
      <Container>
        <Navbar.Brand 
          onClick={handleHomeClick} 
          style={{ cursor: 'pointer', display: 'flex', alignItems: 'center', color: '#fff' }}
        >
          <IoMusicalNotesSharp style={{ marginRight: '8px' }} />
          TuneStay 
        </Navbar.Brand>
      </Container>
    </Navbar>
  );
};

export default Header;
