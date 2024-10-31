import React, { useState } from 'react';

interface FilterValues {
  language: string;
  genres: string;
  popularity: number;
}

interface SearchFiltersProps {
  onFilterChange: (filters: FilterValues) => void;
}

const SearchFilters: React.FC<SearchFiltersProps> = ({ onFilterChange }) => {
  const [language, setLanguage] = useState<string>('');
  const [genres, setGenres] = useState<string>('');
  const [popularity, setPopularity] = useState<number>(50);

  const handleInputChange = () => {
    onFilterChange({ language, genres, popularity });
  };

  return (
    <div className="filter-card">
      <h4>Refine Results</h4>

      <div className="filter-group">
        <label htmlFor="language">Language</label>
        <input
          type="text"
          id="language"
          className="form-control"
          placeholder="Enter language"
          value={language}
          onChange={(e) => {
            setLanguage(e.target.value);
            handleInputChange();
          }}
        />
      </div>

      <div className="filter-group">
        <label htmlFor="genres">Genres</label>
        <input
          type="text"
          id="genres"
          className="form-control"
          placeholder="Enter genres (comma-separated)"
          value={genres}
          onChange={(e) => {
            setGenres(e.target.value);
            handleInputChange();
          }}
        />
      </div>

    
      <div className="filter-group">
        <label htmlFor="popularity">Popularity: {popularity}</label>
        <input
          type="number"
          id="popularity"
          className="form-control"
          min="0"
          max="100"
          value={popularity}
          onChange={(e) => {
            setPopularity(parseInt(e.target.value, 10));
            handleInputChange();
          }}
        />
      </div>
    </div>
  );
};

export default SearchFilters;
