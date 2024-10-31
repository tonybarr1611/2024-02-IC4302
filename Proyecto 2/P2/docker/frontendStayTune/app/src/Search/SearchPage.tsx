
import { useState } from 'react';
import Header from '../Components/Header';
import { Table, Button } from 'react-bootstrap';
import { FaEye } from 'react-icons/fa';
import { MdOutlineLyrics } from "react-icons/md";
import SongInfo from './SongInfo';
import LyricsSection from '../Components/LyricsSection';
import SearchFilters from '../Components/SearchFilters';
import { useNavigate } from 'react-router-dom';
import React from 'react';

interface Song {
  id: string;
  name: string;
  artist: string;
  language: string;
  popularity: number;
  genres: string;
  artistSongs: string;
  link: string;
  artistLink: string;
  lyrics: string;  
}

interface SearchPageProps {
  searchEngine: 'postgresql' | 'mongodb';
}

const SearchPage: React.FC<SearchPageProps> = ({ searchEngine}) => {
  const navigate = useNavigate();
  const [expandedSongId, setExpandedSongId] = useState<string | null>(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [showViewSongModal, setViewSongModal] = useState(false);
  const [selectedSong, setSelectedSong] = useState<Song | null>(null);
  const [filters, setFilters] = useState({
    language: '',
    genres: '',
    popularity: 50,
  });

  const songs: Song[] = [
    {
      id: '1',
      name: 'Blinding Lights',
      artist: 'The Weeknd',
      language: 'English',
      popularity: 90,
      genres: 'Pop, R&B',
      artistSongs: 'Heartless, Save Your Tears, In Your Eyes',
      link: 'https://www.example.com/blinding-lights',
      artistLink: 'https://www.example.com/the-weeknd',
      lyrics: `Yeah\nI've been tryna call\nI've been on my own for long enough\nMaybe you can show me how to love, maybe\nI'm going through withdrawals\nYou don't even have to do too much\nYou can turn me on with just a touch, baby\n`
    },
    {
      id: '2',
      name: 'Despacito',
      artist: 'Luis Fonsi',
      language: 'Spanish',
      popularity: 95,
      genres: 'Pop, Reggaeton',
      artistSongs: 'Échame la Culpa, Calypso',
      link: 'https://www.example.com/despacito',
      artistLink: 'https://www.example.com/luis-fonsi',
      lyrics: `Ay\nFonsi\nDY\nOh\nOh no, oh no\nOh yeah\nDiridiri, dirididi Daddy\nGo\nSí, sabes que ya llevo un rato mirándote\nTengo que bailar contigo hoy (DY)\nVi que tu mirada ya estaba llamándome\nMuéstrame el camino que yo voy (Oh)\n`
    },
    {
      id: '3',
      name: 'Shape of You',
      artist: 'Ed Sheeran',
      language: 'English',
      popularity: 85,
      genres: 'Pop, Dancehall',
      artistSongs: 'Perfect, Castle on the Hill',
      link: 'https://www.example.com/shape-of-you',
      artistLink: 'https://www.example.com/ed-sheeran',
      lyrics: `The club isn't the best place to find a lover\nSo the bar is where I go (mmmm)\nMe and my friends at the table doing shots\nDrinking fast, and then we talk slow (mmmm)\nYou come over and start up a conversation with just me\nAnd trust me, I'll give it a chance now (mmmm)\n`
    },
    {
      id: '4',
      name: 'Bailando',
      artist: 'Enrique Iglesias',
      language: 'Spanish',
      popularity: 88,
      genres: 'Pop, Latin',
      artistSongs: 'El Perdón, Duele El Corazón',
      link: 'https://www.example.com/bailando',
      artistLink: 'https://www.example.com/enrique-iglesias',
      lyrics: `Enrique Iglesias\nGente de Zona\nDescemer\nYo te miro`
    },
    {
      id: '5',
      name: 'Someone You Loved',
      artist: 'Lewis Capaldi',
      language: 'English',
      popularity: 80,
      genres: 'Pop, Indie',
      artistSongs: 'Before You Go, Bruises',
      link: 'https://www.example.com/someone-you-loved',
      artistLink: 'https://www.example.com/lewis-capaldi',
      lyrics: `I'm going under and this time I fear there's no one to save me\nThis all or nothing really got a way of driving me crazy\nI need somebody to heal, somebody to know\nSomebody to have, somebody to hold\nIt's easy to say, but it's never the same\nI guess I kinda liked the way you numbed all the pain\n`
    }
  ];

  const handleViewSong = (song: Song) => {
    setSelectedSong(song);
    setViewSongModal(true);
  };

  const handleCloseSongInfoModal = () => {
    setViewSongModal(false);
    setSelectedSong(null); 
  };

  const toggleLyrics = (songId: string) => {
    setExpandedSongId(expandedSongId === songId ? null : songId);
  };

  const handleSelectVerse = (verse: string) => {
    console.log(`Selected verse: "${verse}"`);
    navigate(`/apartments`, { state: { verse } });
  };

  const handleFilterChange = (newFilters: any) => {
    setFilters(newFilters);
  };

  const filteredSongs = songs.filter((song) => {
    const matchesLanguage = !filters.language || song.language.includes(filters.language);
    const matchesGenres =
      !filters.genres ||
      filters.genres.split(',').some((genre) => song.genres.includes(genre.trim()));
    const matchesPopularity = song.popularity >= filters.popularity;
    return matchesLanguage && matchesGenres && matchesPopularity;
  });

  
  return (
    <div className="main-screen-container">
      <Header />
      <div className="main-screen-background">
        <nav className="top-menu-container">
          <div className="main-screen-header">
            <h1 className="h1 main-screen-title">SEARCH SONGS</h1>
          </div>
          <div className="main-screen-search-section">
            <h2 className="h4 main-screen-subtitle">
              Selected Search Engine: {searchEngine.toUpperCase()}
            </h2>
            <div className="main-screen-search-bar-wrapper">
              <div className="main-screen-search-bar">
                <div className="input-group">
                  <input
                    type="text"
                    className="form-control"
                    placeholder="Search for a song"
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                  />
                </div>
              </div>
            </div>
          </div>
        </nav>
      
    
    <div className="main-screen-content">
      
      <div className="main-screen-table-container">
        <Table className="main-screen-table">
          <thead>
            <tr>
              <th scope="col">Name</th>
              <th scope="col">Artist Name</th>
              <th scope="col">Language</th>
              <th scope="col">Artist Popularity</th>
              <th scope="col">Actions</th>
            </tr>
          </thead>
          <tbody>
            {filteredSongs.map(song => (
              <React.Fragment key={song.id}>
                <tr>
                  <td>{song.name}</td>
                  <td>{song.artist}</td>
                  <td>{song.language}</td>
                  <td>{song.popularity}</td>
                  <td className="main-screen-multiple-action-btns text-center">
                    <Button
                      className="btn btn-outline-primary btn-sm main-screen-small-btn main-screen-info-btn"
                      onClick={() => handleViewSong(song)}
                    >
                      <FaEye />
                    </Button>{' '}
                    <Button
                      className="btn btn-success btn-sm"
                      onClick={() => toggleLyrics(song.id)}
                    >
                      <MdOutlineLyrics />
                    </Button>
                  </td>
                </tr>
                {expandedSongId === song.id && (
                  <tr>
                    <td colSpan={5}>
                      <LyricsSection lyrics={song.lyrics} onSelectVerse={handleSelectVerse} />
                    </td>
                  </tr>
                )}
              </React.Fragment>
            ))}
          </tbody>
        </Table>
      </div>

      
      <div className="main-screen-filters-container">
        <SearchFilters onFilterChange={handleFilterChange} />
      </div>
    </div>
  </div>

      {selectedSong && (
        <SongInfo 
          song={selectedSong} 
          show={showViewSongModal} 
          onHide={handleCloseSongInfoModal} 
        />
      )}
    </div>
  );
};

export default SearchPage;
