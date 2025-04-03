// src/RelationshipsPage.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

function RelationshipsPage() {
  const navigate = useNavigate();
  const [relationships, setRelationships] = useState([]);
  
  // Existing form fields
  const [contactName, setContactName] = useState('');
  const [contactEmail, setContactEmail] = useState('');
  const [relationshipType, setRelationshipType] = useState('friend');
  const [favorite, setFavorite] = useState(false);
  
  // New field for reminder frequency
  const [reminderFrequency, setReminderFrequency] = useState('weekly');

  useEffect(() => {
    const isAuth = localStorage.getItem('isAuth');
    if (!isAuth) {
      navigate('/login');
      return;
    }

    axios.get('http://127.0.0.1:8000/relationships/', {
      withCredentials: true
    })
    .then(response => {
      setRelationships(response.data);
    })
    .catch(error => {
      console.error('Error fetching relationships:', error);
    });
  }, [navigate]);

  const handleAddRelationship = (e) => {
    e.preventDefault();
    const newRel = {
      contact_name: contactName,
      contact_email: contactEmail,
      relationship_type: relationshipType,
      favorite: favorite,
      
      // Include the new reminder_frequency
      reminder_frequency: reminderFrequency
    };

    axios.post('http://127.0.0.1:8000/relationships/', newRel, {
      withCredentials: true
    })
    .then(response => {
      // Add the new contact to local state
      setRelationships([...relationships, response.data]);
      // Reset form fields
      setContactName('');
      setContactEmail('');
      setRelationshipType('friend');
      setFavorite(false);
      setReminderFrequency('weekly'); // back to default
    })
    .catch(error => {
      console.error('Error adding relationship:', error);
    });
  };

  return (
    <div style={{ padding: '20px' }}>
      <h2>Manage Relationships</h2>
      <form onSubmit={handleAddRelationship}>
        <div>
          <label>Contact Name:</label>
          <input
            type="text"
            value={contactName}
            onChange={e => setContactName(e.target.value)}
            required
          />
        </div>
        <div>
          <label>Contact Email:</label>
          <input
            type="email"
            value={contactEmail}
            onChange={e => setContactEmail(e.target.value)}
          />
        </div>
        <div>
          <label>Type:</label>
          <select
            value={relationshipType}
            onChange={e => setRelationshipType(e.target.value)}
          >
            <option value="friend">Friend</option>
            <option value="family">Family</option>
            <option value="coworker">Coworker</option>
            <option value="other">Other</option>
          </select>
        </div>
        <div>
          <label>Favorite:</label>
          <input
            type="checkbox"
            checked={favorite}
            onChange={e => setFavorite(e.target.checked)}
          />
        </div>

        {/* New field for reminder frequency */}
        <div>
          <label>Reminder Frequency:</label>
          <select
            value={reminderFrequency}
            onChange={e => setReminderFrequency(e.target.value)}
          >
            <option value="daily">Daily</option>
            <option value="weekly">Weekly</option>
            <option value="monthly">Monthly</option>
          </select>
        </div>

        <button type="submit">Add Relationship</button>
      </form>

      <h3>Existing Relationships</h3>
      <ul>
        {relationships.map(rel => (
          <li key={rel.id}>
            {rel.contact_name} ({rel.relationship_type}) - {rel.contact_email}{' '}
            {rel.favorite ? '★' : ''} | {rel.reminder_frequency}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default RelationshipsPage;
