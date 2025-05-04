// src/RelationshipsPage.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

function RelationshipsPage() {
  const navigate = useNavigate();
  const [relationships, setRelationships] = useState([]);

  // form state for add/edit
  const [contactName, setContactName]             = useState('');
  const [contactEmail, setContactEmail]           = useState('');
  const [relationshipType, setRelationshipType]   = useState('friend');
  const [favorite, setFavorite]                   = useState(false);
  const [reminderFrequency, setReminderFrequency] = useState('weekly');

  // track editing & deleting
  const [editingId, setEditingId] = useState(null);
  const [deletingId, setDeletingId] = useState(null);

  useEffect(() => {
    if (!localStorage.getItem('isAuth')) {
      navigate('/login');
      return;
    }
    axios.get('/api/relationships/', { withCredentials: true })
      .then(({ data }) => setRelationships(data))
      .catch(err => {
        if ([401,403].includes(err.response?.status)) {
          localStorage.removeItem('isAuth');
          navigate('/login');
        } else {
          console.error(err);
        }
      });
  }, [navigate]);

  const resetForm = () => {
    setContactName('');
    setContactEmail('');
    setRelationshipType('friend');
    setFavorite(false);
    setReminderFrequency('weekly');
    setEditingId(null);
  };

  const handleSubmit = e => {
    e.preventDefault();
    const payload = {
      contact_name:       contactName,
      contact_email:      contactEmail,
      relationship_type:  relationshipType,
      favorite,
      reminder_frequency: reminderFrequency,
    };
    const req = editingId
      ? axios.put(`/api/relationships/${editingId}/`, payload, { withCredentials: true })
      : axios.post('/api/relationships/', payload, { withCredentials: true });

    req.then(({ data }) => {
      if (editingId) {
        setRelationships(prev =>
          prev.map(r => (r.id === editingId ? data : r))
        );
      } else {
        setRelationships(prev => [...prev, data]);
      }
      resetForm();
    })
    .catch(err => {
      console.error('Error saving relationship:', err);
      if ([401,403].includes(err.response?.status)) {
        localStorage.removeItem('isAuth');
        navigate('/login');
      }
    });
  };

  const handleDelete = id => {
    if (!window.confirm('Are you sure you want to delete this relationship?')) {
      return;
    }
    setDeletingId(id);
    axios.delete(`/api/relationships/${id}/`, { withCredentials: true })
      .then(() => {
        setRelationships(prev => prev.filter(r => r.id !== id));
        if (editingId === id) resetForm();
      })
      .catch(err => {
        if (err.response?.status !== 404) console.error('Delete failed', err);
      })
      .finally(() => setDeletingId(null));
  };

  const startEdit = r => {
    setEditingId(r.id);
    setContactName(r.contact_name);
    setContactEmail(r.contact_email);
    setRelationshipType(r.relationship_type);
    setFavorite(r.favorite);
    setReminderFrequency(r.reminder_frequency);
  };

  const handleTestEmail = id => {
    if (!window.confirm('Send a test email for this relationship?')) return;
    axios.post(`/api/send-test-email/${id}/`, {}, { withCredentials: true })
      .then(({ data }) => alert(data.detail))
      .catch(err => {
        console.error('Test email failed', err);
        alert(err.response?.data?.detail || 'Error sending test email');
        if ([401,403].includes(err.response?.status)) {
          localStorage.removeItem('isAuth');
          navigate('/login');
        }
      });
  };

  return (
    <div style={{ padding: 20 }}>
      <h2>Manage Relationships</h2>

      <form onSubmit={handleSubmit}>
        <h3>{editingId ? 'Edit Relationship' : 'Add Relationship'}</h3>

        <div>
          <label>Contact Name:</label><br/>
          <input
            type="text"
            value={contactName}
            onChange={e => setContactName(e.target.value)}
            required
          />
        </div>

        <div>
          <label>Contact Email:</label><br/>
          <input
            type="email"
            value={contactEmail}
            onChange={e => setContactEmail(e.target.value)}
          />
        </div>

        <div>
          <label>Type:</label><br/>
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

        <div>
          <label>Reminder Frequency:</label><br/>
          <select
            value={reminderFrequency}
            onChange={e => setReminderFrequency(e.target.value)}
          >
            <option value="daily">Daily</option>
            <option value="weekly">Weekly</option>
            <option value="monthly">Monthly</option>
          </select>
        </div>

        <button type="submit">
          {editingId ? 'Save Changes' : 'Add Relationship'}
        </button>
        {editingId && (
          <button type="button" onClick={resetForm} style={{ marginLeft: 8 }}>
            Cancel
          </button>
        )}
      </form>

      <h3>Existing Relationships</h3>
      <ul>
        {relationships.map(r => (
          <li key={r.id} style={{ marginBottom: 8 }}>
            <strong>{r.contact_name}</strong> ({r.relationship_type}) — {r.contact_email}{' '}
            {r.favorite && '★'} | {r.reminder_frequency}
            {' '}
            <button onClick={() => startEdit(r)}>✏️ Edit</button>{' '}
            <button
              onClick={() => handleDelete(r.id)}
              disabled={deletingId === r.id}
              style={{ marginLeft: 8 }}
            >
              🗑 Delete
            </button>{' '}
            <button onClick={() => handleTestEmail(r.id)}>📧 Send Test Email</button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default RelationshipsPage;
