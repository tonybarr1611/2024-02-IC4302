import { useEffect, useState } from "react";
import Header from "../Components/Header";
import { Table, Button } from "react-bootstrap";
import ApartmentInfo from "./ApartmentInfo";
import { FaEye } from "react-icons/fa";
import { useLocation } from "react-router-dom";
import { Apartment , getApartments} from "../Commons/Requests";

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
    const fetchData = async () => {
      const response = await getApartments(verse);
      console.log(response);
      setApartments(response);
    };
    fetchData();
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
