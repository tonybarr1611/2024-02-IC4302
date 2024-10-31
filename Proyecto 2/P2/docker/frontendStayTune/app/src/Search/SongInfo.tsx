import { useState, useEffect } from 'react';
import { Form, Button, Modal } from 'react-bootstrap';

interface Song {
  name: string;
  language: string;
  link: string; 
  artist: string;
  genres: string; 
  popularity: number;
  artistSongs: string; 
  artistLink: string; 
}

interface SongInfoProps {
  song: Song; 
  show: boolean;
  onHide: () => void;
}

const SongInfo: React.FC<SongInfoProps> = ({ song, show, onHide }) => {
  const [artistSongs, setArtistSongs] = useState('');

  useEffect(() => {
    if (show) {
      setArtistSongs(song.artistSongs);
    }
  }, [song, show]);

  const handleClose = () => {
    setArtistSongs('');
    onHide();
  };

  return (
    <Modal show={show} onHide={handleClose} centered className='modal'>
      <Modal.Header>
        <Modal.Title>SONG INFORMATION</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <Form className="modal-form">
          <Form.Group controlId="songName" className="h6">
            <Form.Label>Song Name</Form.Label>
            <Form.Control
              type="text"
              value={song.name}
              readOnly
              style={{ cursor: 'default' }}
            
            />
          </Form.Group>

          <Form.Group controlId="language" className="h6">
            <Form.Label>Language</Form.Label>
            <Form.Control
              type="text"
              value={song.language}
              readOnly
              style={{ cursor: 'default' }}
              
            />
          </Form.Group>

          <Form.Group controlId="songLink" className="h6">
            <Form.Label>Song Link</Form.Label>
            <Form.Control
              type="text"
              value={song.link}
              readOnly
              style={{ cursor: 'default' }}
              
            />
          </Form.Group>

          <Form.Group controlId="artistName" className="h6">
            <Form.Label>Artist Name</Form.Label>
            <Form.Control
              type="text"
              value={song.artist}
              readOnly
              style={{ cursor: 'default' }}
              
            />
          </Form.Group>

          <Form.Group controlId="artistGenres" className="h6">
            <Form.Label>Artist Genres</Form.Label>
            <Form.Control
              type="text"
              value={song.genres}
              readOnly
              style={{ cursor: 'default' }}
            
            />
          </Form.Group>

          <Form.Group controlId="artistPopularity" className="h6">
            <Form.Label>Artist Popularity</Form.Label>
            <Form.Control
              type="number"
              value={song.popularity}
              readOnly
              style={{ cursor: 'default' }}
              
            />
          </Form.Group>

          <Form.Group controlId="artistSongs" className="h6">
            <Form.Label>Artist's Songs</Form.Label>
            <Form.Control
              as="textarea"
              value={artistSongs}
              readOnly
              rows={3}
              style={{ cursor: 'default' }}
            
            />
          </Form.Group>

          <Form.Group controlId="artistLink" className="h6">
            <Form.Label>Artist Link</Form.Label>
            <Form.Control
              type="text"
              value={song.artistLink}
              readOnly
              style={{ cursor: 'default' }}
              
            />
          </Form.Group>
        </Form>
      </Modal.Body>

      <Modal.Footer className="modal-footer" style={{ justifyContent: 'flex-end' }}>
        <Button
          variant="outline-success" 
          type="button" 
          onClick={handleClose}>
          ACCEPT
        </Button>
      </Modal.Footer>
    </Modal>
  );
};

export default SongInfo;
