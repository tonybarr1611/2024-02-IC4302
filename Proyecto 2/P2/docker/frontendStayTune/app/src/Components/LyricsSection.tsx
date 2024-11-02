import React, { useState } from "react";
import "./LyricsSection.css";
import { useNavigate } from "react-router-dom";

interface LyricsSectionProps {
  lyrics: string;
  onSelectVerse: (verses: string[]) => void;
}

const LyricsSection: React.FC<LyricsSectionProps> = ({
  lyrics,
  onSelectVerse,
}) => {
  const navigate = useNavigate();
  const [selectedVerses, setSelectedVerses] = useState<string[]>([]);

  const handleVerseClick = (verse: string) => {
    setSelectedVerses((prevSelected) => {
      const updatedSelection = prevSelected.includes(verse)
        ? prevSelected.filter((v) => v !== verse)
        : [...prevSelected, verse];

      onSelectVerse(updatedSelection);
      return updatedSelection;
    });
  };

  const handleSearchClick = () => {
    onSelectVerse(selectedVerses);
    navigate(`/apartments`, { state: { verse: selectedVerses.join(", ") } });
  };

  return (
    <div className="lyrics-section">
      {lyrics.split("\n").map((verse, index) => (
        <p
          key={index}
          className={`verse ${
            selectedVerses.includes(verse) ? "selected" : ""
          }`}
          onClick={() => handleVerseClick(verse)}
        >
          {verse}
        </p>
      ))}
      {selectedVerses.length > 0 && (
        <div className="lyrics-action">
          <button className="btn btn-primary" onClick={handleSearchClick}>
            Search Apartments
          </button>
        </div>
      )}
    </div>
  );
};

export default LyricsSection;
