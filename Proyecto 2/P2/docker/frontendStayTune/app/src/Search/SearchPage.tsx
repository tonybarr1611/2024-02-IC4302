import { useEffect, useState } from "react";
import Header from "../Components/Header";
import { Table, Button } from "react-bootstrap";
import { FaEye } from "react-icons/fa";
import { MdOutlineLyrics } from "react-icons/md";
import SongInfo from "./SongInfo";
import LyricsSection from "../Components/LyricsSection";
import SearchFilters from "../Components/SearchFilters";
import React from "react";
import { Artist, getFilters, getSongs, HSong } from "../Commons/Requests";

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
  searchEngine: "postgresql" | "mongodb";
}

const SearchPage: React.FC<SearchPageProps> = ({ searchEngine }) => {
  const [expandedSongId, setExpandedSongId] = useState<string | null>(null);
  const [searchTerm, setSearchTerm] = useState("");
  const [showViewSongModal, setViewSongModal] = useState(false);
  const [selectedSong, setSelectedSong] = useState<Song | null>(null);
  const [filters, setFilters] = useState({
    language: "",
    genres: "",
    popularity: 50,
  });
  const [nonFilteredSongs, setNonFilteredSongs] = useState<HSong[]>([]);
  const [nonFilteredArtists, setNonFilteredArtists] = useState<Artist[]>([]);

  const [songs, setSongs] = useState<Song[]>([]);
  const [artists, setArtists] = useState<Artist[]>([]);

  useEffect(() => {
    const fetchData = async () => {
      const response = await getFilters(searchEngine === "postgresql" ? 1 : 2);
      setNonFilteredArtists(response.artists);
      console.log("Filters", response);
    };
    fetchData();
  }, []);

  useEffect(() => {
    setArtists(
      nonFilteredArtists.filter(
        (artist) =>
          artist.popularity >= filters.popularity &&
          (!filters.genres ||
            !artist.genres ||
            filters.genres === "" ||
            filters.genres
              .split(",")
              .some((genre) => artist.genres.includes(genre.trim())))
      )
    );
  }, [nonFilteredSongs]);

  useEffect(() => {
    // Assuming nonFilteredSongs and nonFilteredArtists are available
    const mergedSongs = nonFilteredSongs.map((song) => {
      const artist = nonFilteredArtists.find(
        (artist) => artist.link === song.artistLink
      );
      return {
        ...song,
        artist: artist ? artist.name : "Unknown Artist", // Fallback if no artist found
        popularity: artist ? artist.popularity : 0, // You might want to show artist's popularity here
        id: Math.random().toString(36).substr(2, 9), // Generate a random id
        genres: artist ? artist.genres : "",
        artistSongs: artist ? artist.songs.toString() : "",
        lyrics: song.lyric,
      };
    });

    setSongs(
      mergedSongs.filter(
        (song) =>
          song.artistLink ===
            artists.find((artist) => artist.name === song.artist)?.link &&
          (!filters.language ||
            !song.language ||
            filters.language === "" ||
            song.language.includes(filters.language))
      )
    );
  }, [artists]);

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

  const handleSelectVerse = (verses: string[]) => {
    console.log(`Selected verses: "${verses.join(", ")}"`);
  };

  const handleFilterChange = (newFilters: any) => {
    setFilters(newFilters);
  };

  const handleSearch = async () => {
    const response = await getSongs(
      searchTerm,
      searchEngine === "postgresql" ? 1 : 2
    );
    setNonFilteredSongs(response);
    console.log("Filters", response);
  };

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
                  <button
                    className="btn btn-primary ml-2"
                    type="button"
                    onClick={handleSearch}
                  >
                    {" "}
                    Search{" "}
                  </button>
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
                {songs.map((song) => (
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
                        </Button>{" "}
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
                          <LyricsSection
                            lyrics={song.lyrics}
                            onSelectVerse={handleSelectVerse}
                          />
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
