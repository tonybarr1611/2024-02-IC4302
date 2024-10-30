
import { useEffect, useState } from 'react';
import { Form, Button, Modal } from 'react-bootstrap';

interface Apartment {
  name: string;
  description: string;
  reviews: string[];
  summary: string;
}

interface ApartmentInfoProps {
  apartment: Apartment;
  show: boolean;
  onHide: () => void;
}

const ApartmentInfo: React.FC<ApartmentInfoProps> = ({ apartment, show, onHide }) => {
  const [reviews, setReviews] = useState<string[]>([]);

  useEffect(() => {
    if (show) {
      setReviews(apartment.reviews);
    }
  }, [apartment, show]);

  const handleClose = () => {
    setReviews([]); 
    onHide();
  };

  return (
    <Modal show={show} onHide={handleClose} centered className='modal'>
      <Modal.Header>
        <Modal.Title>APARTMENT INFORMATION</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <Form className="modal-form">
          <Form.Group controlId="apartmentName" className="h6">
            <Form.Label>Name</Form.Label>
            <Form.Control
              type="text"
              value={apartment.name}
              readOnly
              style={{ cursor: 'default' }}
            />
          </Form.Group>

          <Form.Group controlId="apartmentDescription" className="h6">
            <Form.Label>Description</Form.Label>
            <Form.Control
              as="textarea"
              value={apartment.description}
              readOnly
              rows={4}
              style={{
                cursor: 'default',
                overflowY: 'auto',
                maxHeight: '150px'
              }}
            />
          </Form.Group>

          <Form.Group controlId="apartmentSummary" className="h6">
            <Form.Label>Summary</Form.Label>
            <Form.Control
              as="textarea"
              value={apartment.summary}
              readOnly
              rows={4}
              style={{
                cursor: 'default',
                overflowY: 'auto',
                maxHeight: '150px'
              }}
            />
          </Form.Group>

          <Form.Group controlId="apartmentReviews" className="h6">
            <Form.Label>Reviews</Form.Label>
            <Form.Control
              as="textarea"
              value={reviews.join('\n\n')}
              readOnly
              rows={6}
              style={{
                cursor: 'default',
                overflowY: 'auto',
                maxHeight: '200px'
              }}
            />
          </Form.Group>
        </Form>
      </Modal.Body>

      <Modal.Footer className="modal-footer" style={{ justifyContent: 'flex-end' }}>
        <Button
          variant="outline-success"
          type="button"
          onClick={handleClose}
        >
          ACCEPT
        </Button>
      </Modal.Footer>
    </Modal>
  );
};

export default ApartmentInfo;
