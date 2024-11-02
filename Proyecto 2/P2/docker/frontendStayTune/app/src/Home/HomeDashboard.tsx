import React from 'react';
import { useNavigate } from 'react-router-dom';
import { BiLogoPostgresql, BiLogoMongodb } from "react-icons/bi";

interface HomeDashboardProps {
  setSearchEngine: (engine: 'postgresql' | 'mongodb') => void;
}

const HomeDashboard: React.FC<HomeDashboardProps> = ({ setSearchEngine }) => {
  const navigate = useNavigate();

  const handleSelection = (engine: 'postgresql' | 'mongodb') => {
    setSearchEngine(engine);
    navigate('/search');
  };

  return (
    <div className="container text-center mt-5">
      <h1 className="mb-4">Welcome to TuneStay</h1>
      <p className="mb-5">
        Select a search engine to start exploring songs and finding your dream apartment. We will do our best to help you find the perfect match!
      </p>

      <div className="row justify-content-center">
        <div className="col-md-4 mb-4">
          <div className="card" onClick={() => handleSelection('postgresql')} style={{ cursor: 'pointer', width: '18rem' }}>
            <div className="card-body">
              <BiLogoPostgresql size={80} style={{ marginBottom: '10px' }} />
              <h5 className="card-title">Use PostgreSQL</h5>
              <p className="card-text">
                Perform text searches in lyrics and artist fields using our relational PostgreSQL database.
              </p>
            </div>
          </div>
        </div>

        <div className="col-md-4 mb-4">
          <div className="card" onClick={() => handleSelection('mongodb')} style={{ cursor: 'pointer', width: '18rem' }}>
            <div className="card-body">
              <BiLogoMongodb size={80} style={{ marginBottom: '10px' }} />
              <h5 className="card-title">Use MongoDB Atlas</h5>
              <p className="card-text">
                Perform full-text searches across all document fields using MongoDB Atlas.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default HomeDashboard;
