import { useEffect, useState } from "react";
import Header from "../Components/Header";
import { Table, Button } from "react-bootstrap";
import ApartmentInfo from "./ApartmentInfo";
import { FaEye } from "react-icons/fa";
import { useLocation } from "react-router-dom";
import { Apartment } from "../Commons/Requests";

const ApartmentList: React.FC = () => {
  const location = useLocation();
  const verse = location.state?.verse || "";
  console.log(verse);

  const [selectedApartment, setSelectedApartment] = useState<Apartment | null>(
    null
  );
  const [showApartmentModal, setShowApartmentModal] = useState(false);

  const [apartments, setApartments] = useState<Apartment[]>([]);

  useEffect(() => {
    const sampleApartments = [
      {
        id: 1,
        name: "Modern Studio Apartment",
        summary: "A sleek, stylish studio in the heart of downtown.",
        description:
          "This studio apartment features an open-concept layout with state-of-the-art appliances, including a refrigerator, microwave, and washer-dryer combo. With floor-to-ceiling windows, you'll enjoy incredible views of the city skyline. The apartment is just steps away from restaurants, shopping, and public transportation, making it the perfect place to experience city life at its best. Amenities include a 24-hour gym, a rooftop pool, and a resident lounge. This description is deliberately long to test how overflow management handles text wrapping and scrolling within the table layout. It should be long enough to require scrolling to view the entire description. The description goes on to add more details, providing a comprehensive overview of the amenities, layout, and location to give potential renters all the information they need to make an informed decision. The description goes on to add more details, providing a comprehensive overview of the amenities, layout, and location to give potential renters all the information they need to make an informed decision. The description goes on to add more details, providing a comprehensive overview of the amenities, layout, and location to give potential renters all the information they need to make an informed decision. The description goes on to add more details, providing a comprehensive overview of the amenities, layout, and location to give potential renters all the information they need to make an informed decision.", 
        reviews: "No reviews yet",
      },
      {
        id: 2,
        name: "Cozy Suburban Home",
        summary: "A spacious home perfect for families.",
        description:
          "This charming three-bedroom, two-bathroom home is nestled in a quiet suburban neighborhood known for its excellent schools and family-friendly atmosphere. It features a large backyard with a deck, perfect for barbecues and gatherings. Inside, you'll find a fully equipped kitchen with stainless steel appliances, a cozy living room with a fireplace, and a master suite with a walk-in closet. This property is conveniently located near parks, grocery stores, and local restaurants. The description goes on to add more details, providing a comprehensive overview of the amenities, layout, and location to give potential renters all the information they need to make an informed decision.",
        reviews: "No reviews yet",
      },
      {
        id: 3,
        name: "Luxury Downtown Penthouse",
        summary: "An upscale penthouse with panoramic city views.",
        description:
          "This breathtaking penthouse is designed for those with exquisite taste. Boasting three spacious bedrooms, each with en-suite bathrooms, and an expansive living area that opens up to a private balcony, this property offers unparalleled luxury. From the marble countertops in the gourmet kitchen to the high-end finishes throughout, every detail has been thoughtfully considered. The apartment includes access to a 24-hour concierge, private parking, and a rooftop garden exclusive to residents. This luxurious property allows you to enjoy a vibrant downtown lifestyle while retreating to an elegant, peaceful home. This description is also very long and intended to test overflow handling within the table view.",
        reviews: "No reviews yet",
      },
    ];
  
    setApartments(sampleApartments);
  }, []);

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
              {apartments.map((apartment) => (
                <tr key={Math.random() * 1534}>
                  <td className="text-wrapper">{apartment.name}</td>
                  <td className="text-wrapper">
                  {apartment.summary}</td>
                  <td className="text-wrapper">{apartment.description}</td>
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
