import './bootstrap/bootstrap.min.css'
import './App.css'
import './Components/MainScreen.css'
import './Components/Modal.css'
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom'
import { useState } from 'react';
import HomeDashboard from './Home/HomeDashboard';
import SearchPage from './Search/SearchPage';
import ApartmentList from './Apartments/ApartmentList';


function App() {

  const [searchEngine, setSearchEngine] = useState<'postgresql' | 'mongodb' | null>(null);

  return (
    <div className="App"> 
      <Router>
        <Routes>
          <Route path="/" element={<HomeDashboard setSearchEngine={(engine) => setSearchEngine(engine)} />} />
          <Route path="/search" element={
            searchEngine ? (
              <SearchPage searchEngine={searchEngine} />
            ) : (
              <p>Please select a search engine from the Home page.</p>
            )
          } />
          <Route path="/apartments" element={<ApartmentList />} />
      </Routes>
    </Router>
  </div>
);
}
        
export default App
