import React, { useState } from 'react';

interface LyricsSectionProps {
  lyrics: string;
  onSelectVerse: (verse: string) => void;
}

const LyricsSection: React.FC<LyricsSectionProps> = ({ lyrics, onSelectVerse }) => {
  const [selectedVerse, setSelectedVerse] = useState<string | null>(null);

  const handleVerseClick = (verse: string) => {
    setSelectedVerse(verse);
    onSelectVerse(verse);
  };

  return (
    <div className="lyrics-section">
      {lyrics.split('\n').map((verse, index) => (
        <p
          key={index}
          className={`verse ${selectedVerse === verse ? 'selected' : ''}`}
          onClick={() => handleVerseClick(verse)}
        >
          {verse}
        </p>
      ))}
      {selectedVerse && (
        <div className="lyrics-action">
          <button
            className="btn btn-primary"
            onClick={() => alert(`Searching apartments for: "${selectedVerse}"`)}
          >
            Search Apartments
          </button>
        </div>
      )}
    </div>
  );
};

export default LyricsSection;
