import axios from "axios";

const API_URL = "http://localhost:31000";

export type HSong = {
  artistLink: string;
  name: string;
  link: string;
  lyric: string;
  language: string;
};

export type Artist = {
  name: string;
  genres: string;
  songs: number;
  popularity: number;
  link: string;
};

export type Apartment = {
  name: string;
  description: string;
  summary: string;
  reviews: string;
};

// CREATE TABLE IF NOT EXISTS Song (
//     ArtistLink VARCHAR(255),
//     Name VARCHAR(255),
//     Link VARCHAR(255),
//     Lyric TEXT,
//     Language VARCHAR(255)
// )

export async function getSongs(query: string, db_id: number): Promise<HSong[]> {
  const params = {
    query: query,
  };
  const songs = await axios.post(`${API_URL}/song/${db_id}`, params);
  return songs.data.map((song: any) => ({
    artistLink: song.ArtistLink,
    name: song.Name,
    link: song.Link,
    lyric: song.Lyric,
    language: song.Language,
  }));
}

export async function getFilters(db_id: number): Promise<{
  artists: Artist[];
}> {
  const filters = await axios.get(`${API_URL}/filters/${db_id}`);
  return {
    artists: filters.data.artists.map((artist: any) => ({
      name: artist.Name,
      genres: artist.Genres,
      songs: artist.Songs,
      popularity: artist.Popularity,
      link: artist.Link,
    })),
  };
}

export async function getApartments(
  selected_text: string
): Promise<Apartment[]> {
  const response = await axios.post(`${API_URL}/lyrics-to-apartments`, {
    selected_text,
  });
  return response.data.map((apartment: any) => ({
    name: apartment.name,
    description: apartment.description,
    summary: apartment.summary,
    reviews: apartment.reviews.map((review: any) => review.comments).join("\n"),
  }));
}
