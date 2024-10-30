import { useState } from 'react';
import Header from '../Components/Header'
import { Table, Button } from 'react-bootstrap';
import ApartmentInfo from './ApartmentInfo';
import { FaEye } from 'react-icons/fa';
import { useLocation } from 'react-router-dom';

interface Apartment {
  id: string;
  name: string;
  summary: string;
  description: string;
  reviews: string[];
}

const ApartmentList: React.FC = () => {
  const location = useLocation();
  const verse = location.state?.verse || ''; 
  console.log(verse);

  const [selectedApartment, setSelectedApartment] = useState<Apartment | null>(null);
  const [showApartmentModal, setShowApartmentModal] = useState(false);

  const apartments: Apartment[] = [
    {
      id: '1',
      name: 'Ocean View Apartment',
      summary: 'A cozy 2-bedroom apartment with ocean views.',
      description: 'Located by the beach, this apartment offers stunning ocean views, fully furnished...',
      reviews: ['Great location, friendly host.', 'Beautiful views, clean and spacious.']
    },
    {
      id: '2',
      name: 'City Center Studio',
      summary: 'Compact studio in the heart of the city.',
      description: 'Perfect for city lovers, this studio offers close proximity to major landmarks...',
      reviews: ['Convenient location, modern amenities.', 'Comfortable stay, would recommend.']
    },
    {
      id: '3',
      name: 'Suburban Family Home',
      summary: 'Spacious home ideal for families.',
      description: 'Located in a peaceful suburb, this home features 3 bedrooms, a large backyard...',
      reviews: ['Great for families, quiet neighborhood.', 'Clean and well-maintained property.']
    }
  ];

  const handleViewApartment = (apartment: Apartment) => {
    setSelectedApartment(apartment);
    setShowApartmentModal(true);
  };

  const handleCloseApartmentModal = () => {
    setShowApartmentModal(false);
    setSelectedApartment(null);
  };

  return (
    <div className="main-screen-container">
      <Header />
      <div className="main-screen-background">
        <div className="main-screen-header">
          <h1 className="h1 main-screen-title">APARTMENT LISTINGS</h1>
        </div>

        <div className="main-screen-content">
          <Table className="main-screen-table">
            <thead>
              <tr>
                <th scope="col">Name</th>
                <th scope="col">Summary</th>
                <th scope="col">Description</th>
                <th scope="col">Actions</th>
              </tr>
            </thead>
            <tbody>
              {apartments.map(apartment => (
                <tr key={apartment.id}>
                  <td>{apartment.name}</td>
                  <td>{apartment.summary}</td>
                  <td>{apartment.description}</td>
                  <td>
                    <Button
                      className="btn btn-outline-primary btn-sm main-screen-small-btn main-screen-info-btn"
                      onClick={() => handleViewApartment(apartment)}
                    >
                      <FaEye />
                    </Button>
                  </td>
                </tr>
              ))}
            </tbody>
          </Table>
        </div>

        {selectedApartment && (
          <ApartmentInfo 
            apartment={selectedApartment} 
            show={showApartmentModal} 
            onHide={handleCloseApartmentModal} 
          />
        )}
      </div>
    </div>
  );
};

export default ApartmentList;
